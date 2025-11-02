# System Configuration

Guide for system-wide configuration including IP address, hostname, and network settings.

---

## Auto-Detection

The dashboard automatically detects system configuration at startup:

- **Local IP Address**: Detected from network interfaces
- **Hostname**: Retrieved from system
- **FQDN**: Fully qualified domain name

### Current Configuration

Your Raspberry Pi is configured with:
- **IP Address**: `192.168.68.65`
- **Hostname**: `rpi`

---

## Accessing System Config

### In Python Code

```python
from flask import current_app

# Get local IP
local_ip = current_app.config['LOCAL_IP']

# Get hostname
hostname = current_app.config['HOSTNAME']

# Get full config
system_config = current_app.config['SYSTEM_CONFIG']
```

### In Templates

System config is automatically available in all Jinja2 templates:

```html
<!-- Local IP -->
{{ LOCAL_IP }}

<!-- Hostname -->
{{ HOSTNAME }}

<!-- Full config -->
{{ SYSTEM_CONFIG.local_ip }}
{{ SYSTEM_CONFIG.hostname }}
{{ SYSTEM_CONFIG.fqdn }}
```

### Via API

Get system configuration via REST API:

```bash
curl http://localhost:5050/api/system/config
```

Response:
```json
{
  "success": true,
  "config": {
    "local_ip": "192.168.68.65",
    "hostname": "rpi",
    "system_config": {
      "local_ip": "192.168.68.65",
      "hostname": "rpi",
      "fqdn": "rpi"
    }
  }
}
```

---

## Manual Override

If you need to override the auto-detected values, set environment variables:

```bash
# Set in environment
export LOCAL_IP=192.168.68.65
export HOSTNAME=custom-hostname
```

Or add to `.env` file (based on `deploy/environment.example`):

```bash
# System Configuration
LOCAL_IP=192.168.68.65
HOSTNAME=raspberrypi
```

---

## Configuration Files

### `configs/system_config.json`

Optional static configuration file:

```json
{
  "network": {
    "local_ip": "192.168.68.65",
    "hostname": "rpi",
    "domain": "local",
    "description": "Raspberry Pi 3B network configuration"
  },
  "system": {
    "model": "Raspberry Pi 3B",
    "description": "Home dashboard and GPIO controller"
  }
}
```

**Note**: Currently for reference only. The system uses runtime auto-detection.

---

## How It Works

### Startup Flow

1. Flask app starts (`app/__init__.py`)
2. `app/system_info.py` module imports
3. Auto-detection runs:
   - Gets local IP via socket detection
   - Gets hostname from system
   - Caches results
4. Values stored in Flask config
5. Made available to all templates via context processor

### IP Detection Method

The system tries multiple methods to get the local IP:

1. **Hostname lookup**: Resolves hostname to IP
2. **Socket method**: Creates UDP socket to determine default route IP
3. **Fallback**: Returns `127.0.0.1` if detection fails

```python
def get_local_ip():
    hostname = socket.gethostname()
    local_ip = socket.gethostbyname(hostname)
    
    if local_ip.startswith('127.'):
        # Try socket method
        s = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
        s.connect(('8.8.8.8', 80))
        local_ip = s.getsockname()[0]
        s.close()
    
    return local_ip
```

---

## Usage Examples

### Display IP in Template

Add to any template:

```html
<div class="info-box">
  <p>Dashboard IP: {{ LOCAL_IP }}</p>
  <p>Hostname: {{ HOSTNAME }}</p>
</div>
```

### Use in API Response

```python
from flask import current_app, jsonify

@app.route('/api/info')
def info():
    return jsonify({
        'ip': current_app.config['LOCAL_IP'],
        'hostname': current_app.config['HOSTNAME']
    })
```

### JavaScript Access

System config is available via API:

```javascript
async function getSystemConfig() {
    const response = await fetch('/api/system/config');
    const data = await response.json();
    
    console.log('IP:', data.config.local_ip);
    console.log('Hostname:', data.config.hostname);
}
```

---

## Network Configuration

### Static IP Setup (Reference)

Your Pi has a static IP configured. To verify or modify:

```bash
# Check current IP
hostname -I

# View network configuration
ip addr show

# Check DHCP client configuration
cat /etc/dhcpcd.conf
```

For static IP configuration, see your router or system network configuration.

---

## Logging

System configuration detection is logged:

```bash
# View logs
tail -f logs/app.log | grep "System configured"

# Output:
# 2025-11-02 08:15:27 [INFO] app: System configured - IP: 192.168.68.65, Hostname: rpi
```

---

## API Endpoints

### Get System Config
```bash
GET /api/system/config
```

Returns:
- `local_ip`: Local IP address
- `hostname`: System hostname
- `system_config`: Full configuration object

### Get Network Interfaces
```bash
GET /api/system/network/interfaces
```

Returns all network interfaces with IP addresses and status.

---

## Environment Variables

Optional environment variables:

```bash
# Override auto-detected IP
LOCAL_IP=192.168.68.65

# Override hostname
HOSTNAME=my-raspberry-pi

# Set log level
LOG_LEVEL=INFO
```

---

## Troubleshooting

### IP Shows as 127.0.0.1

Auto-detection failed. Possible solutions:

1. Set `LOCAL_IP` environment variable
2. Check network interfaces: `ip addr show`
3. Verify hostname resolves: `hostname -I`

### Wrong IP Detected

If the wrong interface IP is detected:

1. Set explicit `LOCAL_IP` environment variable
2. Check routing: `ip route show default`
3. Verify network configuration: `cat /etc/dhcpcd.conf`

### IP Not Available in Templates

1. Check Flask context processor is registered
2. Verify `app.config['LOCAL_IP']` is set
3. Check logs for initialization errors

---

## Related Documentation

- **[GETTING_STARTED.md](GETTING_STARTED.md)** - General setup
- **[API.md](API.md)** - API reference
- **[DEPLOYMENT.md](DEPLOYMENT.md)** - Production deployment

---

**System configuration is automatically detected and available throughout the application!** ✓

