# Project Structure

Complete reference for the Raspberry Pi Dashboard project structure.

## Directory Tree

```
/home/gauravs/dashboard/
│
├── app/                         # Main application package
│   ├── __init__.py              # Flask app factory, blueprint registration
│   ├── config.py                # Environment-based configuration
│   │
│   ├── routes/                  # HTTP route handlers (thin layer)
│   │   ├── __init__.py          
│   │   ├── main.py              # Page routes (/, /services)
│   │   ├── system.py            # System monitoring API (/api/system/*)
│   │   └── services.py          # Services management API (/api/services/*)
│   │
│   ├── modules/                 # Business logic modules (thick layer)
│   │   ├── __init__.py
│   │   ├── system_monitor.py   # System stats collection logic
│   │   └── raspotify.py         # Raspotify integration logic
│   │
│   ├── static/                  # Static assets
│   │   ├── css/
│   │   │   └── style.css        # Dashboard styles
│   │   ├── js/
│   │   │   └── dashboard.js     # Frontend JavaScript
│   │   └── img/
│   │       └── pi-mascot.png    # Raspberry Pi mascot
│   │
│   └── templates/               # Jinja2 HTML templates
│       ├── base.html            # Base template with common layout
│       ├── index.html           # Homepage (system stats)
│       └── services.html        # Services status page
│
├── docs/                        # Documentation
│   ├── 00_INDEX.md              # Documentation index
│   ├── README.md                # Full technical documentation
│   ├── GETTING_STARTED.md       # Complete setup guide
│   ├── API.md                   # Complete API reference
│   ├── DEPLOYMENT.md            # Production deployment guide
│   ├── ADDING_SERVICES.md       # Guide for adding new services
│   ├── STRUCTURE.md             # This file
│   └── PROJECT_HISTORY.md       # Migration guide and history
│
├── venv/                        # Python virtual environment (not tracked)
│
├── run.py                       # Development server entry point
├── wsgi.py                      # Production WSGI entry point
├── gunicorn_config.py           # Gunicorn server configuration
├── requirements.txt             # Python dependencies
├── .gitignore                   # Git ignore rules
├── README.md                    # Project README
│
├── dashboard.py                 # [OLD] Legacy monolithic app (keep for reference)
└── dashboard.html               # [OLD] Legacy HTML file (keep for reference)
```

## File Descriptions

### Root Level Files

#### `run.py`
Development server entry point. Use for local testing.
```bash
python run.py
```

#### `wsgi.py`
Production WSGI entry point for gunicorn.
```bash
gunicorn -c gunicorn_config.py wsgi:app
```

#### `gunicorn_config.py`
Gunicorn server configuration optimized for Raspberry Pi 3B (1GB RAM).
- 2 workers maximum
- Preload app to save memory
- Restart workers after 1000 requests

#### `requirements.txt`
Python dependencies with pinned versions.
- Flask 3.0.0
- flask-cors 4.0.0
- psutil 5.9.6
- gunicorn 21.2.0
- etc.

#### `.gitignore`
Git ignore rules for Python, virtual environment, IDE files, etc.

#### `README.md`
Main project README with quick start, features, and links to docs.

### `app/` Package

#### `app/__init__.py`
Flask application factory pattern.
- Creates and configures Flask app
- Registers blueprints
- Enables CORS

#### `app/config.py`
Configuration classes for different environments:
- `DevelopmentConfig`: Debug enabled
- `ProductionConfig`: Optimized for Pi 3B
- `TestingConfig`: For tests

### `app/routes/` Package

HTTP route handlers - thin layer that delegates to modules.

#### `app/routes/main.py`
**Blueprint:** `main`
**URL Prefix:** None

Routes:
- `GET /` - Homepage (system dashboard)
- `GET /services` - Services status page

#### `app/routes/system.py`
**Blueprint:** `system`
**URL Prefix:** `/api/system`

Routes:
- `GET /api/system/stats` - All system statistics
- `GET /api/system/world-clocks` - Time in multiple timezones
- `GET /api/system/health` - Health check

#### `app/routes/services.py`
**Blueprint:** `services`
**URL Prefix:** `/api/services`

Routes:
- `GET /api/services/list` - List all services
- `GET /api/services/raspotify/status` - Raspotify status
- `GET /api/services/raspotify/current` - Currently playing track
- `GET /api/services/health` - Health check

### `app/modules/` Package

Business logic modules - thick layer with actual functionality.

#### `app/modules/system_monitor.py`
System monitoring functions:
- `get_cpu_temp()` - CPU temperature
- `get_uptime()` - System uptime
- `get_pi_model()` - Raspberry Pi model
- `get_throttle_status()` - Throttling status
- `get_top_processes()` - Top 5 memory processes
- `get_partitions()` - Disk partitions
- `get_network_interfaces()` - Network info
- `get_wifi_signal()` - WiFi signal strength
- `get_public_ip()` - Public IP address
- `get_weather()` - Local weather
- `get_all_stats()` - Complete system stats

#### `app/modules/raspotify.py`
Raspotify integration functions:
- `is_running()` - Check if Raspotify is running
- `get_service_status()` - Detailed service status
- `get_current_track()` - Currently playing track info
- `get_raspotify_config()` - Read Raspotify config
- `get_device_name()` - Get Spotify device name

### `app/static/` Directory

Static assets served by Flask/nginx.

#### `app/static/css/style.css`
Dashboard styles:
- CSS variables for theming
- Glassmorphism design
- Responsive grid layouts
- Mobile-first approach
- Animations and transitions

#### `app/static/js/dashboard.js`
Frontend JavaScript:
- API calls to backend
- Real-time stats updates
- Error handling
- Service status rendering

#### `app/static/img/pi-mascot.png`
Raspberry Pi mascot logo.

### `app/templates/` Directory

Jinja2 HTML templates.

#### `app/templates/base.html`
Base template with:
- HTML head (meta tags, CSS)
- Logo/mascot
- Content block
- Footer
- JavaScript includes

#### `app/templates/index.html`
Extends `base.html`. Homepage with:
- System stats cards (uptime, CPU, memory, disk)
- Quick links navigation
- Real-time updates via JavaScript

#### `app/templates/services.html`
Extends `base.html`. Services page with:
- Service status cards
- Real-time service monitoring
- Navigation links

### `docs/` Directory

Comprehensive documentation.

#### `docs/README.md`
Full documentation covering:
- Features
- Installation
- API endpoints
- Configuration
- Troubleshooting

#### `docs/GETTING_STARTED.md`
Complete setup guide:
- Quick start (1 minute)
- Detailed setup (5 minutes)
- Configuration options
- Troubleshooting

#### `docs/DEPLOYMENT.md`
Production deployment guide:
- System dependencies
- Gunicorn setup
- Nginx configuration
- Systemd service
- Monitoring and logs
- Security recommendations

#### `docs/ADDING_SERVICES.md`
Guide for integrating new IoT services:
- Module creation
- Route handler setup
- Frontend integration
- Examples (Home Assistant, Camera, MQTT)
- Best practices

#### `docs/API.md`
Complete API reference:
- Quick reference tables
- Fast endpoints (~10ms)
- Cached endpoints with TTL
- Performance improvements
- Usage examples
- Best practices

#### `docs/PROJECT_HISTORY.md`
Project evolution and migration:
- Migration from old structure
- What changed
- Breaking changes
- Implementation summary
- Plan vs implementation

#### `docs/STRUCTURE.md`
This file - complete project structure reference.

## Architecture Patterns

### Application Factory Pattern
`app/__init__.py` uses factory pattern to create Flask app instances with different configurations.

### Blueprint Pattern
Routes organized into blueprints for modular structure:
- **main**: Page routes
- **system**: System API
- **services**: Services API

### Separation of Concerns
- **Routes**: Handle HTTP requests/responses
- **Modules**: Contain business logic
- **Templates**: Render HTML
- **Static**: Serve assets

### Resource Optimization
Optimized for Raspberry Pi 3B (1GB RAM):
- Minimal dependencies
- Gunicorn worker limits
- Efficient caching
- Lazy loading where possible

## Adding New Components

### Adding a New Module
```
app/modules/your_service.py
```

### Adding New Routes
Add to appropriate blueprint:
- System monitoring → `app/routes/system.py`
- Service management → `app/routes/services.py`
- New pages → `app/routes/main.py` or create new blueprint

### Adding New Pages
```
app/templates/your_page.html
```

Register route in `app/routes/main.py`:
```python
@main_bp.route('/your-page')
def your_page():
    return render_template('your_page.html')
```

### Adding Static Assets
- CSS → `app/static/css/`
- JavaScript → `app/static/js/`
- Images → `app/static/img/`

## File Naming Conventions

- **Python files**: `snake_case.py`
- **Templates**: `lowercase.html`
- **CSS/JS**: `lowercase.css`, `lowercase.js`
- **Documentation**: `UPPERCASE.md`

## Import Patterns

### Importing from modules
```python
from app.modules import system_monitor
from app.modules import raspotify
```

### Importing Flask app
```python
from app import create_app
app = create_app('production')
```

### Importing blueprints
```python
from app.routes.main import main_bp
from app.routes.system import system_bp
from app.routes.services import services_bp
```

## Environment Variables

Supported environment variables:

```bash
FLASK_ENV=development|production|testing
SECRET_KEY=your-secret-key
```

## Dependencies

Core dependencies:
- **Flask**: Web framework
- **flask-cors**: CORS support
- **psutil**: System monitoring
- **requests**: HTTP requests
- **pytz**: Timezone support
- **gunicorn**: WSGI server

## URLs Reference

### Development URLs (port 5050)
- Homepage: `http://localhost:5050/`
- Services: `http://localhost:5050/services`
- API: `http://localhost:5050/api/system/stats`

### Production URLs (behind nginx, port 80)
- Homepage: `http://raspberrypi.local/`
- Services: `http://raspberrypi.local/services`
- API: `http://raspberrypi.local/api/system/stats`

## Related Documentation

- [README.md](README.md) - Full technical documentation
- [GETTING_STARTED.md](GETTING_STARTED.md) - Complete setup guide
- [API.md](API.md) - Complete API reference
- [DEPLOYMENT.md](DEPLOYMENT.md) - Production setup
- [ADDING_SERVICES.md](ADDING_SERVICES.md) - Extend functionality
- [PROJECT_HISTORY.md](PROJECT_HISTORY.md) - Migration guide and history

