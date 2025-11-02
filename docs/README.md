# Raspberry Pi Dashboard

A modern, mobile-friendly web dashboard for monitoring and controlling your Raspberry Pi 3B and connected services.

## Features

- **System Monitoring**: Real-time CPU, memory, disk, and network statistics
- **Service Management**: Monitor and control services like Raspotify
- **Mobile-Friendly**: Responsive design optimized for all screen sizes
- **Extensible**: Easy-to-add modules for new IoT devices and services
- **Resource-Efficient**: Optimized for Raspberry Pi 3B (1GB RAM)

## Project Structure

```
dashboard/
├── app/
│   ├── __init__.py           # Flask application factory
│   ├── config.py             # Configuration settings
│   ├── routes/               # HTTP route handlers
│   │   ├── main.py           # Page routes
│   │   ├── system.py         # System monitoring API
│   │   └── services.py       # Service management API
│   ├── modules/              # Business logic modules
│   │   ├── system_monitor.py # System stats collection
│   │   └── raspotify.py      # Raspotify integration
│   ├── static/               # CSS, JS, images
│   └── templates/            # HTML templates
├── docs/                     # Documentation
├── run.py                    # Development server
├── wsgi.py                   # Production WSGI entry
├── gunicorn_config.py        # Gunicorn configuration
└── requirements.txt          # Python dependencies
```

## Installation

### 1. Clone/Navigate to Project

```bash
cd /home/gauravs/dashboard
```

### 2. Install Dependencies

```bash
# Activate virtual environment (if not already active)
source venv/bin/activate

# Install requirements
pip install -r requirements.txt
```

### 3. Run Development Server

```bash
python run.py
```

Access at: `http://localhost:5050`

## Production Deployment

See [DEPLOYMENT.md](DEPLOYMENT.md) for detailed nginx, gunicorn, and systemd setup.

### Quick Start

```bash
# Run with gunicorn
gunicorn -c gunicorn_config.py wsgi:app
```

## API Endpoints

### System Monitoring (Fast - Real-time)

- `GET /api/system/stats` - Essential system stats (~10ms) ⚡
- `GET /api/system/system-info` - Static system info (<5ms) ⚡
- `GET /api/system/health` - Health check (<1ms) ⚡
- `GET /api/system/world-clocks` - Time in multiple timezones

### System Monitoring (Cached - Expensive Operations)

- `GET /api/system/weather` - Local weather (cached 10min)
- `GET /api/system/network` - Network info (cached 30s)
- `GET /api/system/network/public-ip` - Public IP (cached 5min)
- `GET /api/system/network/wifi` - WiFi signal (cached 30s)
- `GET /api/system/audio` - Audio devices (cached 1min)
- `GET /api/system/stats/detailed` - All stats (cached 5s)

### Services

- `GET /api/services/list` - List all available services
- `GET /api/services/raspotify/status` - Get Raspotify status
- `GET /api/services/raspotify/current` - Get currently playing track

📚 **See [API.md](API.md) for complete API documentation**

## Adding New Services

1. Create a new module in `app/modules/your_service.py`
2. Add route handlers in `app/routes/services.py`
3. Update the frontend in `app/static/js/dashboard.js`

Example module structure:

```python
# app/modules/your_service.py

def get_status():
    """Return service status"""
    return {
        'running': True,
        'status': 'active'
    }
```

See [ADDING_SERVICES.md](ADDING_SERVICES.md) for detailed guide.

## Configuration

Edit `app/config.py` to modify settings:

- `SECRET_KEY`: Change in production
- `MAX_CONTENT_LENGTH`: Request size limit
- Environment-specific settings (development/production)

## Resource Optimization

Optimized for Raspberry Pi 3B (1GB RAM):

- Gunicorn configured with 2 workers maximum
- Worker restart after 1000 requests
- Minimal dependencies
- Efficient caching strategies

## Troubleshooting

### Dashboard not loading stats

1. Check if Flask server is running: `ps aux | grep python`
2. Check logs: `journalctl -u dashboard -n 50`
3. Verify nginx is proxying correctly

### Raspotify not showing

1. Check if service is installed: `systemctl status raspotify`
2. Ensure user has permissions to check systemctl

## License

MIT License - Feel free to modify and distribute

## Contributing

This is a personal project, but feel free to fork and adapt for your needs!

