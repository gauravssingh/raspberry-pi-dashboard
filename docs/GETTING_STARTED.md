# Getting Started with Raspberry Pi Dashboard

Get your dashboard up and running quickly!

---

## ⚡ Quick Start (1 Minute)

### Prerequisites
- Raspberry Pi 3B with Raspbian OS
- Python 3.7+ installed
- Internet connection

### Three Simple Commands

```bash
# 1. Navigate to project
cd /home/gauravs/dashboard

# 2. Activate virtual environment
source venv/bin/activate

# 3. Run the dashboard
python run.py
```

**Access:** Open browser to `http://localhost:5050` or `http://raspberrypi.local:5050`

That's it! Your dashboard is running. 🎉

---

## 📖 Detailed Setup Guide (5 Minutes)

For a more thorough setup or if you encounter issues.

### Step 1: Navigate to Project Directory

```bash
cd /home/gauravs/dashboard
```

### Step 2: Activate Virtual Environment

```bash
source venv/bin/activate
```

If virtual environment doesn't exist:
```bash
python3 -m venv venv
source venv/bin/activate
```

### Step 3: Install Dependencies

```bash
pip install -r requirements.txt
```

Expected packages:
- Flask 3.0.0
- flask-cors 4.0.0
- psutil 5.9.6
- requests 2.31.0
- gunicorn 21.2.0
- pytz 2023.3

### Step 4: Run the Application

**Development Mode** (with auto-reload):
```bash
python run.py
```

**Production Mode** (with gunicorn):
```bash
gunicorn -c gunicorn_config.py wsgi:app
```

---

## 🌐 Accessing the Dashboard

### From the Raspberry Pi

Open a browser and visit:
- `http://localhost:5050`

### From Another Device on Your Network

1. Find your Pi's IP address:
   ```bash
   hostname -I
   ```

2. Access from any device on your network:
   - `http://[your-pi-ip]:5050`
   - `http://raspberrypi.local:5050`

The dashboard is fully mobile-responsive! 📱

---

## 🎯 What You'll See

### Homepage (/)

Real-time system monitoring with:
- 📊 **System Uptime** - How long your Pi has been running
- 🔥 **CPU Temperature** - Current temperature (keep it under 80°C!)
- 💻 **CPU Usage** - Processor utilization percentage
- 💾 **Memory Usage** - RAM usage with visual progress bar
- 💿 **Disk Usage** - Storage usage with visual progress bar

**Auto-updates:** Stats refresh automatically every 5 seconds

### Services Page (/services)

Monitor connected services:
- 🎵 **Raspotify Status** - Spotify Connect availability
- 🎶 **Shairport Sync** - AirPlay receiver status
- **Currently Playing** - Track info (when available)

**Auto-updates:** Service status refreshes every 10 seconds

---

## 🔧 Configuration

### Change Server Port

Edit `run.py` for development:
```python
app.run(host='0.0.0.0', port=YOUR_PORT, debug=True)
```

Edit `gunicorn_config.py` for production:
```python
bind = "127.0.0.1:YOUR_PORT"
```

### Change Update Frequency

Edit `app/static/js/dashboard.js`:
```javascript
// Change from 5000ms (5 seconds) to your preference
setInterval(fetchStats, 5000);  // Change 5000 to desired milliseconds
```

### Set Flask Environment

```bash
# Development mode (verbose logging, auto-reload)
export FLASK_ENV=development
python run.py

# Production mode (optimized, no debug)
export FLASK_ENV=production
gunicorn -c gunicorn_config.py wsgi:app
```

### Customize Configuration

Edit `app/config.py` for advanced settings:
```python
class ProductionConfig(Config):
    DEBUG = False
    SECRET_KEY = 'your-secret-key-here'
    MAX_CONTENT_LENGTH = 16 * 1024 * 1024  # 16MB max
```

---

## 🆘 Troubleshooting

### "Cannot connect to backend" Error

**Symptoms:** Frontend displays error message

**Solutions:**
1. Check if Flask is running:
   ```bash
   ps aux | grep python
   ```

2. Restart the application:
   ```bash
   python run.py
   ```

3. Check for port conflicts:
   ```bash
   sudo netstat -tlnp | grep 5050
   ```

### Stats Not Updating

**Solutions:**
1. Refresh the page (Ctrl+R or Cmd+R)
2. Check browser console for errors (F12)
3. Test the API directly:
   ```bash
   curl http://localhost:5050/api/system/health
   # Should return: {"status": "ok", "service": "system"}
   ```

### High CPU/Memory Usage

**Symptoms:** Pi running slow, dashboard laggy

**Solutions:**
1. Use production mode instead of development:
   ```bash
   gunicorn -c gunicorn_config.py wsgi:app
   ```

2. Reduce update frequency (edit `dashboard.js`):
   ```javascript
   setInterval(fetchStats, 10000);  // Update every 10 seconds instead of 5
   ```

3. Check resource usage:
   ```bash
   htop  # or 'top' if htop not available
   ```

4. Reduce gunicorn workers in `gunicorn_config.py`:
   ```python
   workers = 1  # Reduce from 2 to 1
   ```

### Port 5050 Already in Use

**Solutions:**
1. Find what's using the port:
   ```bash
   sudo netstat -tlnp | grep 5050
   ```

2. Kill the process:
   ```bash
   sudo kill -9 <PID>
   ```

3. Or change to a different port (see Configuration section)

### Import Errors

**Symptoms:** `ModuleNotFoundError` or similar

**Solutions:**
1. Verify virtual environment is activated:
   ```bash
   which python  # Should show /home/gauravs/dashboard/venv/bin/python
   ```

2. Reinstall dependencies:
   ```bash
   pip install -r requirements.txt --force-reinstall
   ```

3. Test imports manually:
   ```bash
   python -c "from app import create_app; print('OK')"
   ```

---

## 🎵 Optional: Set Up Raspotify

If you want Spotify Connect functionality:

```bash
# Install Raspotify
curl -sL https://dtcooper.github.io/raspotify/install.sh | sh

# Start service
sudo systemctl start raspotify

# Enable on boot
sudo systemctl enable raspotify

# Check status
sudo systemctl status raspotify
```

The dashboard will automatically detect and display Raspotify status!

---

## 🧪 Testing Your Setup

### Quick Verification

Run this test:
```bash
python3 << 'EOF'
from app import create_app
app = create_app('production')
print("✅ Everything works!" if app else "❌ Problem detected")
EOF
```

Should output: `✅ Everything works!`

### API Endpoint Tests

Test all endpoints with curl:

```bash
# Health check
curl http://localhost:5050/api/system/health

# System stats
curl http://localhost:5050/api/system/stats | python -m json.tool

# System info
curl http://localhost:5050/api/system/system-info

# Services list
curl http://localhost:5050/api/services/list

# Weather (if configured)
curl http://localhost:5050/api/system/weather
```

---

## 📱 Access from Mobile/Tablet

1. Find your Pi's IP address:
   ```bash
   hostname -I
   ```

2. On your phone/tablet browser, navigate to:
   - `http://[your-pi-ip]:5050`
   - `http://raspberrypi.local:5050`

The UI is fully responsive and works beautifully on mobile devices!

---

## 🚀 Next Steps

### 1. Deploy to Production

For 24/7 operation with auto-start on boot:
- Read **[DEPLOYMENT.md](DEPLOYMENT.md)** for complete nginx + systemd setup
- Set up reverse proxy for port 80 access
- Configure automatic service management

### 2. Add More Services

Extend your dashboard with new IoT integrations:
- Read **[ADDING_SERVICES.md](ADDING_SERVICES.md)**
- Examples included: Home Assistant, Camera streams, MQTT
- Create custom modules for your hardware

### 3. Explore the API

Learn about available endpoints:
- Read **[API.md](API.md)** for complete API reference
- Fast endpoints for real-time data
- Cached endpoints for expensive operations

### 4. Customize the UI

Make it your own:
- Edit styles: `app/static/css/style.css`
- Edit templates: `app/templates/`
- Edit JavaScript: `app/static/js/dashboard.js`

---

## 💡 Pro Tips

1. **Auto-start on boot:** Set up systemd service (see [DEPLOYMENT.md](DEPLOYMENT.md))
2. **Remote access:** Set up port forwarding on your router (security considerations apply)
3. **Monitor logs:** Use `sudo journalctl -u dashboard -f` when running as service
4. **Resource monitoring:** Run `htop` to monitor Pi resources
5. **Keep it updated:** Regularly update dependencies with `pip install -r requirements.txt --upgrade`

---

## 📚 Useful Commands Reference

```bash
# Development
python run.py                              # Start dev server
curl http://localhost:5050/api/system/health  # Test API

# Production (after setup)
sudo systemctl start dashboard             # Start service
sudo systemctl stop dashboard              # Stop service
sudo systemctl restart dashboard           # Restart service
sudo systemctl status dashboard            # Check status
sudo journalctl -u dashboard -f            # View logs

# System monitoring
htop                                       # Resource monitor
free -h                                    # Memory usage
df -h                                      # Disk usage
vcgencmd measure_temp                      # CPU temperature

# Virtual environment
source venv/bin/activate                   # Activate
deactivate                                 # Deactivate
pip list                                   # Show installed packages
```

---

## 🎓 Learning Resources

- **Flask Documentation:** https://flask.palletsprojects.com/
- **Raspberry Pi Docs:** https://www.raspberrypi.org/documentation/
- **Raspotify:** https://github.com/dtcooper/raspotify
- **Shairport Sync:** https://github.com/mikebrady/shairport-sync
- **Gunicorn:** https://docs.gunicorn.org/

---

## ✅ Getting Started Checklist

Before moving forward, ensure you can:

- [ ] Run `python run.py` successfully
- [ ] Access `http://localhost:5050` in browser
- [ ] See system stats updating every 5 seconds
- [ ] Navigate to services page (`/services`)
- [ ] Test API with `curl http://localhost:5050/api/system/health`
- [ ] (Optional) Install and see Raspotify status

---

## 📞 Need More Help?

1. **Check the docs:**
   - [API.md](API.md) - Complete API documentation
   - [DEPLOYMENT.md](DEPLOYMENT.md) - Production setup
   - [ADDING_SERVICES.md](ADDING_SERVICES.md) - Extend functionality
   - [STRUCTURE.md](STRUCTURE.md) - Project organization

2. **Review logs:** 
   ```bash
   # If running directly
   Check terminal output
   
   # If running as service
   sudo journalctl -u dashboard -n 50
   ```

3. **Verify setup:**
   ```bash
   python -c "from app import create_app; app = create_app('production')"
   ```

---

## 🎉 You're Ready!

Your Raspberry Pi Dashboard is now running. Start with:

```bash
python run.py
```

Then visit **http://localhost:5050** and enjoy your beautiful monitoring dashboard!

**Happy monitoring! 🚀**

---

*Last updated: October 29, 2025*
