# Raspberry Pi Dashboard

> A modern, feature-rich web dashboard for monitoring and controlling your Raspberry Pi with GPIO support

![Raspberry Pi](https://img.shields.io/badge/Raspberry%20Pi-A22846?style=for-the-badge&logo=Raspberry%20Pi&logoColor=white)
![Flask](https://img.shields.io/badge/Flask-000000?style=for-the-badge&logo=flask&logoColor=white)
![Python](https://img.shields.io/badge/Python-3.7+-3776AB?style=for-the-badge&logo=python&logoColor=white)

## ✨ Features

- 📊 **Real-time System Monitoring** - CPU, memory, disk, network, temperature
- ⚡ **GPIO Control** - Control GPIO pins via web interface with breadboard wiring guides
- 🎵 **Service Management** - Monitor and control Raspotify, Shairport-Sync
- 🌤️ **Weather Integration** - Local weather and world clocks
- 📱 **Mobile-Friendly** - Responsive glassmorphism UI
- 🔧 **Extensible** - Easy to add new services and integrations
- 📋 **Log Viewer** - Real-time system and service logs
- ⚡ **Optimized** - Resource-efficient for Pi 3B (1GB RAM)

## 🚀 Quick Start

```bash
# Clone the repository
git clone https://github.com/YOUR_USERNAME/raspberry-pi-dashboard.git
cd raspberry-pi-dashboard

# Create virtual environment
python3 -m venv venv
source venv/bin/activate

# Install dependencies
pip install -r requirements.txt

# Run development server
python run.py
```

Access at: **http://localhost:5050**

For detailed setup, see **[docs/GETTING_STARTED.md](docs/GETTING_STARTED.md)**

## 📸 Screenshots

<img width="1554" height="1014" alt="Screenshot 2025-11-02 at 6 50 03 PM" src="https://github.com/user-attachments/assets/38bc3444-1336-4526-b8b9-eaec407b1744" />

## 🎯 GPIO Control

Control Raspberry Pi GPIO pins through a beautiful web interface:

- **Dynamic Configuration** - Edit `configs/gpio_config.json` to add/remove pins
- **Visual Wiring Guide** - Step-by-step breadboard setup with diagrams
- **REST API** - Full API for automation
- **Real-time Updates** - Live pin state monitoring
- **Supports**: LEDs, Relays, and custom GPIO devices

See **[docs/GPIO.md](docs/GPIO.md)** for complete GPIO documentation.

## 📁 Project Structure

```
raspberry-pi-dashboard/
├── app/
│   ├── routes/             # API endpoints and page routes
│   ├── modules/            # Business logic (GPIO, system monitoring)
│   ├── static/             # CSS, JavaScript, images
│   └── templates/          # HTML templates
├── configs/                # JSON configuration files
│   ├── gpio_config.json    # GPIO pin configuration
│   └── system_config.json  # System settings
├── docs/                   # Complete documentation
├── deploy/                 # Production deployment files
├── logs/                   # Application logs (gitignored)
├── requirements.txt        # Python dependencies
├── run.py                  # Development server
└── wsgi.py                 # Production WSGI entry
```

## 🌐 API Endpoints

### System Monitoring
- `GET /api/system/stats` - Quick system stats (~10ms)
- `GET /api/system/info` - Detailed system information
- `GET /api/system/weather` - Weather data
- `GET /api/system/world-clocks` - World time zones

### GPIO Control
- `GET /api/gpio/pins` - List all configured pins
- `POST /api/gpio/pin/<id>/set` - Set pin state
- `POST /api/gpio/pin/<id>/toggle` - Toggle pin state
- `GET /api/gpio/config` - GPIO configuration

### Services
- `GET /api/services/list` - Available services
- `GET /api/services/raspotify/status` - Raspotify status
- `GET /api/services/shairport-sync/status` - Shairport status

See **[docs/API.md](docs/API.md)** for complete API documentation.

## 🔧 Configuration

### GPIO Setup

Edit `configs/gpio_config.json`:

```json
{
  "pins": [
    {
      "id": "gpio_17",
      "gpio_number": 17,
      "name": "LED 1",
      "type": "led",
      "direction": "output",
      "initial_state": "low",
      "group": "LEDs"
    }
  ]
}
```

### Environment Variables

Copy `deploy/environment.example` to `.env` and customize:

```bash
SECRET_KEY=your-secret-key-here
LOG_LEVEL=INFO
```

## 🛠️ Technology Stack

- **Backend**: Flask 3.0, Python 3.7+
- **GPIO**: libgpiod (modern GPIO interface)
- **Server**: Gunicorn + Nginx
- **Monitoring**: psutil
- **Frontend**: Vanilla JavaScript, CSS3 (no frameworks)
- **OS**: Raspberry Pi OS (Debian-based)

## 🚢 Production Deployment

Deploy with systemd and nginx:

```bash
# Copy systemd service
sudo cp deploy/dashboard.service /etc/systemd/system/
sudo systemctl enable dashboard
sudo systemctl start dashboard

# Configure nginx
sudo cp deploy/nginx.conf /etc/nginx/sites-available/dashboard
sudo ln -s /etc/nginx/sites-available/dashboard /etc/nginx/sites-enabled/
sudo systemctl restart nginx
```

See **[docs/DEPLOYMENT.md](docs/DEPLOYMENT.md)** for complete deployment guide.

## 📖 Documentation

### Quick Start
- **[Documentation Index](docs/00_INDEX.md)** - Complete documentation guide
- **[Getting Started](docs/GETTING_STARTED.md)** - Setup guide

### GPIO & Hardware
- **[GPIO Guide](docs/GPIO.md)** - GPIO control and configuration
- **[GPIO Wiring Guide](docs/GPIO_WIRING_GUIDE.md)** - Visual breadboard setup
- **[GPIO Pin Reference](docs/GPIO_PIN_REFERENCE.md)** - Complete pinout

### Development
- **[API Reference](docs/API.md)** - Complete API documentation
- **[Adding Services](docs/ADDING_SERVICES.md)** - Extend functionality
- **[Project Structure](docs/STRUCTURE.md)** - Code organization

### Deployment & GitHub
- **[Deployment Guide](docs/DEPLOYMENT.md)** - Production setup
- **[GitHub Setup](docs/GIT_SETUP_GUIDE.md)** - Git best practices
- **[Security Audit](docs/SECURITY_AUDIT.md)** - Security scan report

## 🔒 Security

⚠️ **Important Security Notice**

This dashboard is designed for **personal use on a trusted local network**.

### Security Considerations

- ❌ **No authentication by default** - Add nginx basic auth if exposing to internet
- ❌ **Command execution requires sudo** - Whitelist-protected but be cautious
- ❌ **GPIO control has no auth** - Ensure network is secure
- ✅ **Designed for internal/home network only**

### For Production/Public Network

If exposing to the internet:

1. **Add Authentication**
   ```bash
   # Nginx basic auth
   sudo htpasswd -c /etc/nginx/.htpasswd admin
   ```

2. **Enable HTTPS**
   - Use Let's Encrypt or self-signed certificates
   - See `deploy/nginx-ssl.conf`

3. **Set Strong SECRET_KEY**
   ```bash
   export SECRET_KEY=$(python -c 'import secrets; print(secrets.token_hex(32))')
   ```

4. **Review Command Whitelist**
   - Check `app/routes/tools.py` for allowed commands
   - Disable terminal execution if not needed

5. **Firewall Rules**
   ```bash
   sudo ufw allow from 192.168.1.0/24 to any port 5050
   ```

## 🎯 Use Cases

- Monitor Raspberry Pi system health
- Control GPIO-connected devices (LEDs, relays, sensors)
- Manage music streaming services
- View logs and diagnostics
- Central dashboard for home automation
- IoT device hub

## 🧪 Testing

Test GPIO setup:
```bash
python test_gpio.py
```

Test API endpoints:
```bash
./scripts/test_new_endpoints.sh
```

## 📋 Requirements

- **Hardware**: Raspberry Pi 3B or newer (1GB+ RAM)
- **OS**: Raspberry Pi OS (Debian-based)
- **Python**: 3.7 or higher
- **Optional**: LEDs, relay modules, breadboard for GPIO testing

## 🤝 Contributing

This is a personal hobby project, but contributions are welcome!

1. Fork the repository
2. Create a feature branch
3. Make your changes
4. Test thoroughly
5. Submit a pull request

## 🐛 Troubleshooting

**Dashboard not loading?**
```bash
# Check if running
ps aux | grep gunicorn

# Check logs
tail -f logs/app.log
```

**GPIO in simulation mode?**
```bash
# Run with sudo for GPIO access
sudo venv/bin/python run.py

# Or configure udev rules (see docs/GPIO.md)
```

**API not responding?**
```bash
curl http://localhost:5050/api/system/health
```

See **[docs/GPIO.md](docs/GPIO.md#troubleshooting)** for more solutions.

## 📜 License

MIT License - See [LICENSE](LICENSE) for details

## 🙏 Acknowledgments

- Built with ❤️ for Raspberry Pi enthusiasts
- Inspired by home automation and maker communities
- Uses libgpiod for modern GPIO control

## ⚠️ Disclaimer

This software is provided "as-is" for educational and personal use. Use at your own risk, especially when controlling hardware or running system commands. Always follow electrical safety guidelines when working with GPIO pins.

---

**Made with ❤️ for Raspberry Pi** • Star ⭐ this repo if you find it useful!

## 📞 Support

- **Documentation**: [docs/00_INDEX.md](docs/00_INDEX.md)
- **Issues**: Use GitHub Issues for bugs and feature requests
- **Discussions**: Use GitHub Discussions for questions

---

*Optimized for Raspberry Pi 3B • Tested on Raspberry Pi OS*
