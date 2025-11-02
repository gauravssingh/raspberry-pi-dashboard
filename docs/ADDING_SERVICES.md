# Adding New Services

Guide for integrating new IoT devices and services into the dashboard.

## Overview

The dashboard uses a modular architecture:

1. **Module** (`app/modules/`) - Contains the business logic
2. **Route** (`app/routes/services.py`) - Exposes HTTP endpoints
3. **Frontend** (`app/static/js/dashboard.js` + templates) - Displays the data

## Step-by-Step Guide

### Step 1: Create a Module

Create a new file in `app/modules/your_service.py`:

```python
"""Your Service integration module"""
import subprocess

def is_running():
    """Check if service is running"""
    try:
        result = subprocess.run(
            ['systemctl', 'is-active', 'your-service'],
            capture_output=True,
            text=True,
            timeout=2
        )
        return result.stdout.strip() == 'active'
    except:
        return False

def get_status():
    """Get detailed service status"""
    return {
        'running': is_running(),
        'name': 'Your Service',
        'status': 'active' if is_running() else 'inactive'
    }

def get_data():
    """Get service-specific data"""
    # Implement your data collection logic
    return {
        'some_metric': 42,
        'another_value': 'hello'
    }
```

### Step 2: Add Routes

Edit `app/routes/services.py` and add your endpoints:

```python
from app.modules import your_service

@services_bp.route('/your-service/status')
def your_service_status():
    """Get service status"""
    status = your_service.get_status()
    return jsonify(status)

@services_bp.route('/your-service/data')
def your_service_data():
    """Get service data"""
    data = your_service.get_data()
    return jsonify(data)
```

### Step 3: Update Service List

Update the `/api/services/list` endpoint in `app/routes/services.py`:

```python
@services_bp.route('/list')
def list_services():
    """List all available services"""
    services = [
        {
            'name': 'Raspotify',
            'id': 'raspotify',
            'description': 'Spotify Connect for Raspberry Pi',
            'endpoints': {
                'status': '/api/services/raspotify/status',
                'current': '/api/services/raspotify/current'
            }
        },
        {
            'name': 'Your Service',
            'id': 'your-service',
            'description': 'Description of your service',
            'endpoints': {
                'status': '/api/services/your-service/status',
                'data': '/api/services/your-service/data'
            }
        }
    ]
    
    return jsonify({'services': services})
```

### Step 4: Update Frontend (Optional)

Edit `app/static/js/dashboard.js` to display your service on the services page:

```javascript
async function loadServices() {
  const container = document.getElementById('services-container');
  if (!container) return;
  
  try {
    // Load existing services
    // ... (raspotify code)
    
    // Load your service
    const yourServiceRes = await fetch(`${API_BASE}/api/services/your-service/status`);
    const yourServiceData = await yourServiceRes.json();
    
    renderYourServiceCard(container, yourServiceData);
    
  } catch (error) {
    showError('Unable to load services.');
  }
}

function renderYourServiceCard(container, data) {
  const statusClass = data.running ? 'status-active' : 'status-inactive';
  const statusText = data.running ? 'Active' : 'Inactive';
  
  const card = `
    <div class="service-card">
      <div class="service-header">
        <div class="service-name">🔧 Your Service</div>
        <div class="status-badge ${statusClass}">${statusText}</div>
      </div>
      <div class="service-info">
        <strong>Status:</strong> ${data.status}<br>
        <!-- Add more info here -->
      </div>
    </div>
  `;
  
  container.innerHTML += card;
}
```

### Step 5: Test Your Integration

1. Restart the Flask server:
   ```bash
   python run.py
   ```

2. Test the API endpoint:
   ```bash
   curl http://localhost:5050/api/services/your-service/status
   ```

3. Visit the services page: `http://localhost:5050/services`

## Example Integrations

### Example 1: Home Assistant Integration

```python
# app/modules/homeassistant.py
import requests

HASS_URL = "http://homeassistant.local:8123"
HASS_TOKEN = "your_long_lived_token"

def get_status():
    try:
        headers = {
            "Authorization": f"Bearer {HASS_TOKEN}",
            "Content-Type": "application/json"
        }
        response = requests.get(
            f"{HASS_URL}/api/",
            headers=headers,
            timeout=5
        )
        return {
            'running': response.status_code == 200,
            'message': response.json().get('message', 'Running')
        }
    except:
        return {'running': False, 'error': 'Cannot connect'}

def get_entities():
    try:
        headers = {
            "Authorization": f"Bearer {HASS_TOKEN}",
            "Content-Type": "application/json"
        }
        response = requests.get(
            f"{HASS_URL}/api/states",
            headers=headers,
            timeout=5
        )
        return response.json()
    except:
        return []
```

### Example 2: Camera Stream

```python
# app/modules/camera.py
import subprocess

def is_streaming():
    try:
        # Check if motion or camera process is running
        result = subprocess.run(
            ['pgrep', '-f', 'raspivid'],
            capture_output=True
        )
        return result.returncode == 0
    except:
        return False

def get_stream_url():
    return "http://raspberrypi.local:8081"

def start_stream():
    try:
        subprocess.Popen([
            'raspivid', '-o', '-', '-t', '0', '-w', '640', '-h', '480',
            '-fps', '15', '|', 'cvlc', '-vvv', 'stream:///dev/stdin',
            '--sout', '#standard{access=http,mux=ts,dst=:8081}', ':demux=h264'
        ])
        return {'success': True}
    except Exception as e:
        return {'success': False, 'error': str(e)}
```

### Example 3: MQTT Broker Status

```python
# app/modules/mqtt.py
import subprocess

def get_mosquitto_status():
    try:
        result = subprocess.run(
            ['systemctl', 'is-active', 'mosquitto'],
            capture_output=True,
            text=True,
            timeout=2
        )
        running = result.stdout.strip() == 'active'
        
        return {
            'running': running,
            'service': 'mosquitto',
            'status': 'active' if running else 'inactive'
        }
    except:
        return {'running': False, 'error': 'Cannot check status'}

def get_broker_stats():
    # Parse mosquitto stats if available
    # This would require mosquitto_sub or similar
    pass
```

## Best Practices

### 1. Error Handling

Always wrap external calls in try-except blocks:

```python
def get_data():
    try:
        # Your logic here
        return {'success': True, 'data': result}
    except Exception as e:
        return {'success': False, 'error': str(e)}
```

### 2. Timeouts

Always set timeouts for network requests and subprocess calls:

```python
response = requests.get(url, timeout=5)
subprocess.run(cmd, timeout=2)
```

### 3. Caching (Optional)

For expensive operations, consider caching:

```python
from functools import lru_cache
from datetime import datetime, timedelta

_cache = {'data': None, 'timestamp': None}

def get_expensive_data():
    now = datetime.now()
    if _cache['data'] and _cache['timestamp']:
        if now - _cache['timestamp'] < timedelta(seconds=30):
            return _cache['data']
    
    # Fetch new data
    data = fetch_data()
    _cache['data'] = data
    _cache['timestamp'] = now
    return data
```

### 4. Resource Efficiency

Remember the Pi 3B has limited resources:

- Avoid polling too frequently
- Use async operations when possible
- Keep worker processes minimal
- Clean up resources after use

### 5. Security

- Never hardcode credentials (use environment variables)
- Validate all inputs
- Use HTTPS for external services
- Limit API rate to prevent abuse

## Template for New Service

Use this template as a starting point:

```python
# app/modules/template_service.py
"""
Template for new service integration
Replace 'template' with your service name
"""
import subprocess
import requests

SERVICE_NAME = "template"
SYSTEMD_SERVICE = "template.service"  # if using systemd

def is_running():
    """Check if service is running"""
    try:
        result = subprocess.run(
            ['systemctl', 'is-active', SYSTEMD_SERVICE],
            capture_output=True,
            text=True,
            timeout=2
        )
        return result.stdout.strip() == 'active'
    except:
        return False

def get_status():
    """Get service status"""
    return {
        'service': SERVICE_NAME,
        'running': is_running(),
        'status': 'active' if is_running() else 'inactive'
    }

def get_info():
    """Get service information"""
    # Implement your custom logic
    return {
        'name': SERVICE_NAME,
        'version': '1.0.0',
        'description': 'Service description'
    }

def get_metrics():
    """Get service metrics/data"""
    # Implement your data collection
    return {
        'metric1': 0,
        'metric2': 'value'
    }

# Add control functions if needed
def start():
    """Start the service"""
    try:
        subprocess.run(['sudo', 'systemctl', 'start', SYSTEMD_SERVICE], timeout=5)
        return {'success': True}
    except Exception as e:
        return {'success': False, 'error': str(e)}

def stop():
    """Stop the service"""
    try:
        subprocess.run(['sudo', 'systemctl', 'stop', SYSTEMD_SERVICE], timeout=5)
        return {'success': True}
    except Exception as e:
        return {'success': False, 'error': str(e)}
```

## Need Help?

- Check existing modules in `app/modules/` for examples
- Review [API.md](API.md) for API endpoint patterns
- Review [STRUCTURE.md](STRUCTURE.md) for project organization
- Review Flask documentation: https://flask.palletsprojects.com/
- Test your endpoints with curl or Postman before frontend integration

