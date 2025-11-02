# Production Deployment Guide

Complete guide for deploying the Raspberry Pi Dashboard with nginx, gunicorn, and systemd.

---

## 📋 Table of Contents

- [Prerequisites](#prerequisites)
- [Installation Steps](#installation-steps)
- [Systemd Service Setup](#systemd-service-setup)
- [Nginx Configuration](#nginx-configuration)
- [Monitoring and Logs](#monitoring-and-logs)
- [Maintenance](#maintenance)
- [Troubleshooting](#troubleshooting)
- [Security](#security-recommendations)
- [Performance Tuning](#performance-tuning)
- [Backup](#backup)

---

## Prerequisites

- Raspberry Pi 3B running Raspbian OS
- Python 3.7 or higher
- nginx installed
- Virtual environment set up
- Basic Linux command line knowledge

---

## Installation Steps

### Step 1: Install System Dependencies

```bash
sudo apt-get update
sudo apt-get install -y python3-pip python3-venv nginx
```

### Step 2: Set Up Application

```bash
cd /home/gauravs/dashboard

# Create virtual environment (if not exists)
python3 -m venv venv

# Activate virtual environment
source venv/bin/activate

# Install dependencies
pip install -r requirements.txt
```

### Step 3: Test Gunicorn

The project includes `gunicorn_config.py` optimized for Pi 3B.

Test gunicorn:

```bash
gunicorn -c gunicorn_config.py wsgi:app
```

You should see:
```
[INFO] Starting gunicorn ...
[INFO] Listening at: http://127.0.0.1:5050
```

Press Ctrl+C to stop.

---

## Systemd Service Setup

Running the dashboard as a systemd service provides:
- ✅ Auto-start on boot
- ✅ Automatic restart on failure
- ✅ Easy start/stop/restart commands
- ✅ Centralized logging with journalctl
- ✅ Resource management

### Create the Service File

```bash
sudo nano /etc/systemd/system/dashboard.service
```

Add the following content:

```ini
[Unit]
Description=Raspberry Pi Dashboard
After=network.target

[Service]
Type=notify
User=gauravs
Group=gauravs
WorkingDirectory=/home/gauravs/dashboard
Environment="PATH=/home/gauravs/dashboard/venv/bin"
ExecStart=/home/gauravs/dashboard/venv/bin/gunicorn -c gunicorn_config.py wsgi:app
Restart=always
RestartSec=10

# Resource limits for Pi 3B
MemoryMax=400M
CPUQuota=80%

[Install]
WantedBy=multi-user.target
```

### Service File Explanation

**[Unit] Section:**
- `Description`: What the service does
- `After=network.target`: Wait for network before starting

**[Service] Section:**
- `Type=notify`: Gunicorn will notify systemd when ready
- `User/Group`: Run as your user (not root for security)
- `WorkingDirectory`: Project directory
- `Environment`: Use virtual environment Python
- `ExecStart`: Command to start the application
- `Restart=always`: Auto-restart on failure
- `RestartSec=10`: Wait 10 seconds before restart
- `MemoryMax=400M`: Limit to 400MB RAM (safe for Pi 3B)
- `CPUQuota=80%`: Limit to 80% CPU usage

**[Install] Section:**
- `WantedBy=multi-user.target`: Start service in multi-user mode (normal boot)

### Enable and Start the Service

```bash
# Reload systemd to recognize the new service
sudo systemctl daemon-reload

# Enable service to start on boot
sudo systemctl enable dashboard

# Start the service now
sudo systemctl start dashboard

# Check status
sudo systemctl status dashboard
```

You should see:
```
● dashboard.service - Raspberry Pi Dashboard
     Loaded: loaded (/etc/systemd/system/dashboard.service; enabled)
     Active: active (running) since ...
```

### Service Management Commands

```bash
# Start the service
sudo systemctl start dashboard

# Stop the service
sudo systemctl stop dashboard

# Restart the service
sudo systemctl restart dashboard

# Check status
sudo systemctl status dashboard

# Enable auto-start on boot
sudo systemctl enable dashboard

# Disable auto-start on boot
sudo systemctl disable dashboard
```

### Customizing the Service

#### Change User

If your username is different from `gauravs`, edit the service file:

```bash
sudo nano /etc/systemd/system/dashboard.service
```

Change these lines:
```ini
User=YOUR_USERNAME
Group=YOUR_USERNAME
WorkingDirectory=/home/YOUR_USERNAME/dashboard
Environment="PATH=/home/YOUR_USERNAME/dashboard/venv/bin"
ExecStart=/home/YOUR_USERNAME/dashboard/venv/bin/gunicorn -c gunicorn_config.py wsgi:app
```

Then reload:
```bash
sudo systemctl daemon-reload
sudo systemctl restart dashboard
```

#### Change Resource Limits

Edit resource limits based on your needs:

```ini
# More restrictive (if running many services)
MemoryMax=300M
CPUQuota=60%

# Less restrictive (if dashboard is primary service)
MemoryMax=500M
CPUQuota=100%
```

#### Add Environment Variables

Add custom environment variables:

```ini
[Service]
Environment="SECRET_KEY=your-secret-key-here"
Environment="FLASK_ENV=production"
Environment="CUSTOM_VAR=value"
```

---

## Nginx Configuration

### Create Nginx Configuration

```bash
sudo nano /etc/nginx/sites-available/dashboard
```

Add the following configuration:

```nginx
server {
    listen 80;
    server_name raspberrypi.local localhost;

    # Security headers
    add_header X-Frame-Options "SAMEORIGIN" always;
    add_header X-Content-Type-Options "nosniff" always;
    add_header X-XSS-Protection "1; mode=block" always;

    # Logging
    access_log /var/log/nginx/dashboard_access.log;
    error_log /var/log/nginx/dashboard_error.log;

    # Static files
    location /static/ {
        alias /home/gauravs/dashboard/app/static/;
        expires 5m;
        add_header Cache-Control "public, must-revalidate, proxy-revalidate";
    }

    # API and page routes
    location / {
        proxy_pass http://127.0.0.1:5050;
        proxy_set_header Host $host;
        proxy_set_header X-Real-IP $remote_addr;
        proxy_set_header X-Forwarded-For $proxy_add_x_forwarded_for;
        proxy_set_header X-Forwarded-Proto $scheme;
        
        # Timeouts
        proxy_connect_timeout 30s;
        proxy_send_timeout 30s;
        proxy_read_timeout 30s;
        
        # Buffering
        proxy_buffering on;
        proxy_buffer_size 4k;
        proxy_buffers 8 4k;
    }

    # Health check endpoint (don't log)
    location /api/system/health {
        proxy_pass http://127.0.0.1:5050;
        access_log off;
    }
}
```

### Enable the Site

```bash
# Create symbolic link to enable site
sudo ln -s /etc/nginx/sites-available/dashboard /etc/nginx/sites-enabled/

# Test nginx configuration
sudo nginx -t

# Restart nginx
sudo systemctl restart nginx
```

### Service Flow

```
Internet → Nginx (port 80) → Gunicorn (port 5050) → Flask App
```

---

## Monitoring and Logs

### View Application Logs

```bash
# Real-time logs
sudo journalctl -u dashboard -f

# Last 100 lines
sudo journalctl -u dashboard -n 100

# Logs since today
sudo journalctl -u dashboard --since today

# Logs from last hour
sudo journalctl -u dashboard --since "1 hour ago"
```

### View Nginx Logs

```bash
# Access logs
sudo tail -f /var/log/nginx/dashboard_access.log

# Error logs
sudo tail -f /var/log/nginx/dashboard_error.log
```

### Check Resource Usage

```bash
# Service status with memory
sudo systemctl status dashboard

# Detailed resource info
systemctl show dashboard | grep -E "Memory|CPU|Tasks"

# Using htop
htop -p $(pgrep -f gunicorn)

# Memory usage
free -h

# CPU usage
top

# Dashboard process
ps aux | grep gunicorn
```

### Continuous Monitoring

```bash
# Watch logs
watch -n 1 'sudo journalctl -u dashboard -n 10'

# Monitor with systemctl
watch -n 2 'sudo systemctl status dashboard'
```

---

## Maintenance

### Restart the Application

```bash
sudo systemctl restart dashboard
```

### Update the Application

```bash
cd /home/gauravs/dashboard

# Pull updates (if using git)
git pull

# Activate virtual environment
source venv/bin/activate

# Update dependencies if needed
pip install -r requirements.txt --upgrade

# Restart service
sudo systemctl restart dashboard

# Check status
sudo systemctl status dashboard

# Monitor logs
sudo journalctl -u dashboard -f
```

### Verify Deployment

1. **Check gunicorn is running:**
   ```bash
   sudo systemctl status dashboard
   ```

2. **Check nginx is running:**
   ```bash
   sudo systemctl status nginx
   ```

3. **Test the dashboard:**
   ```bash
   curl http://localhost/api/system/health
   ```

4. **Open in browser:** 
   - `http://raspberrypi.local`
   - `http://[your-pi-ip]`

---

## Troubleshooting

### Service Won't Start

**Check logs:**
```bash
sudo journalctl -u dashboard -n 50
```

**Common issues:**

1. **Virtual environment not found**
   ```bash
   # Verify venv exists
   ls /home/gauravs/dashboard/venv/bin/gunicorn
   ```

2. **Permission issues**
   ```bash
   # Check file ownership
   ls -la /home/gauravs/dashboard
   
   # Fix if needed
   sudo chown -R gauravs:gauravs /home/gauravs/dashboard
   ```

3. **Port already in use**
   ```bash
   # Check what's using port 5050
   sudo netstat -tlnp | grep 5050
   
   # Kill if needed
   sudo kill <PID>
   ```

4. **Python dependencies missing**
   ```bash
   # Reinstall dependencies
   source /home/gauravs/dashboard/venv/bin/activate
   pip install -r requirements.txt
   ```

### Service Crashes Immediately

Check the logs:
```bash
sudo journalctl -u dashboard -n 100
```

Test manually:
```bash
cd /home/gauravs/dashboard
source venv/bin/activate
gunicorn -c gunicorn_config.py wsgi:app
```

If manual start works but service doesn't:
- Check User/Group in service file
- Check WorkingDirectory path
- Check Environment PATH

### Dashboard Returns 502 Bad Gateway

**Causes:**
- Gunicorn not running
- Port mismatch between nginx and gunicorn
- Firewall blocking connection

**Solutions:**
- Check if gunicorn is running: `sudo systemctl status dashboard`
- Check gunicorn logs: `sudo journalctl -u dashboard -n 50`
- Verify port 5050 is listening: `sudo netstat -tlnp | grep 5050`
- Test direct connection: `curl http://127.0.0.1:5050/api/system/health`

### Service Running But Can't Access

1. **Check service is running:**
   ```bash
   sudo systemctl status dashboard
   ```

2. **Check if listening on correct port:**
   ```bash
   sudo netstat -tlnp | grep 5050
   ```

3. **Test directly:**
   ```bash
   curl http://127.0.0.1:5050/api/system/health
   ```

4. **Check nginx is proxying:**
   ```bash
   sudo systemctl status nginx
   curl http://localhost/api/system/health
   ```

### High Memory Usage

**Solutions:**
- Reduce gunicorn workers in `gunicorn_config.py`
- Check for memory leaks in logs
- Restart service: `sudo systemctl restart dashboard`
- Adjust MemoryMax in service file

### Static Files Not Loading

**Solutions:**
- Check nginx configuration
- Verify file permissions: `ls -la /home/gauravs/dashboard/app/static/`
- Check nginx error logs
- Test direct static file access

### Cannot Connect to External APIs (Weather, Public IP)

**Solutions:**
- Check internet connectivity: `ping 8.8.8.8`
- Verify DNS: `nslookup google.com`
- Check firewall rules
- Review application logs for specific errors

---

## Security Recommendations

### 1. Change Secret Key

Edit `app/config.py`:
```python
class ProductionConfig(Config):
    SECRET_KEY = 'your-strong-random-secret-key-here'
```

Generate a secure key:
```bash
python -c "import secrets; print(secrets.token_hex(32))"
```

### 2. Enable HTTPS

Install Let's Encrypt certificate:
```bash
sudo apt-get install certbot python3-certbot-nginx
sudo certbot --nginx -d your-domain.com
```

### 3. Restrict Access by IP (Optional)

Add to nginx configuration:
```nginx
location / {
    allow 192.168.1.0/24;  # Your local network
    deny all;
    
    proxy_pass http://127.0.0.1:5050;
    # ... rest of config
}
```

### 4. Enable Firewall

```bash
# Enable firewall
sudo ufw enable

# Allow SSH
sudo ufw allow 22/tcp

# Allow HTTP/HTTPS
sudo ufw allow 80/tcp
sudo ufw allow 443/tcp

# Reload
sudo ufw reload
```

### 5. Regular Updates

```bash
# Update system
sudo apt-get update && sudo apt-get upgrade -y

# Update Python packages
source venv/bin/activate
pip install -r requirements.txt --upgrade
```

### 6. Security Hardening

Add to systemd service file:
```ini
[Service]
NoNewPrivileges=true
PrivateTmp=true
ProtectSystem=strict
ProtectHome=read-only
ReadWritePaths=/home/gauravs/dashboard
```

---

## Performance Tuning

### For Raspberry Pi 3B

**Optimize Gunicorn** (`gunicorn_config.py`):
```python
# Start with 2 workers, reduce to 1 if memory constrained
workers = 1

# Restart workers after handling requests
max_requests = 1000
max_requests_jitter = 50

# Timeout settings
timeout = 30
keepalive = 2

# Preload application to save memory
preload_app = True
```

### Enable Nginx Caching

Add to nginx config:
```nginx
# Add to server block
proxy_cache_path /var/cache/nginx levels=1:2 keys_zone=dashboard_cache:10m max_size=100m;

# Add to location /
location / {
    proxy_cache dashboard_cache;
    proxy_cache_valid 200 1m;
    add_header X-Cache-Status $upstream_cache_status;
    
    # ... existing proxy settings
}
```

### Monitoring Tips

1. Monitor resource usage regularly
2. Set up alerts for high CPU/memory
3. Use `htop` to identify resource hogs
4. Check logs for errors and warnings
5. Test after configuration changes

---

## Backup

### Backup Important Files

```bash
# Create backup directory
mkdir -p ~/backups

# Backup application
tar -czf ~/backups/dashboard-$(date +%Y%m%d).tar.gz /home/gauravs/dashboard

# Backup nginx config
sudo cp /etc/nginx/sites-available/dashboard ~/backups/

# Backup systemd service
sudo cp /etc/systemd/system/dashboard.service ~/backups/
```

### Automated Backup Script

Create `backup.sh`:
```bash
#!/bin/bash
BACKUP_DIR="$HOME/backups"
DATE=$(date +%Y%m%d-%H%M%S)

mkdir -p "$BACKUP_DIR"
tar -czf "$BACKUP_DIR/dashboard-$DATE.tar.gz" \
  /home/gauravs/dashboard \
  --exclude='venv' \
  --exclude='*.pyc' \
  --exclude='__pycache__'

# Keep only last 7 backups
ls -t "$BACKUP_DIR"/dashboard-*.tar.gz | tail -n +8 | xargs -r rm

echo "Backup completed: dashboard-$DATE.tar.gz"
```

Make executable:
```bash
chmod +x backup.sh
```

Schedule with cron:
```bash
crontab -e

# Add line: Run daily at 2 AM
0 2 * * * /home/gauravs/backup.sh
```

### Restore from Backup

```bash
# Stop service
sudo systemctl stop dashboard

# Extract backup
tar -xzf ~/backups/dashboard-YYYYMMDD.tar.gz -C /

# Restart service
sudo systemctl start dashboard
```

---

## Testing the Deployment

### Full Test Procedure

```bash
# 1. Stop any running instances
sudo systemctl stop dashboard
pkill -f "python run.py"

# 2. Test manual start
cd /home/gauravs/dashboard
source venv/bin/activate
gunicorn -c gunicorn_config.py wsgi:app
# Ctrl+C to stop

# 3. Start with systemd
sudo systemctl start dashboard

# 4. Check status
sudo systemctl status dashboard

# 5. Test API
curl http://127.0.0.1:5050/api/system/health

# 6. Test through nginx
curl http://localhost/api/system/health

# 7. Check logs
sudo journalctl -u dashboard -n 20

# 8. Test restart
sudo systemctl restart dashboard

# 9. Test auto-restart (optional)
sudo systemctl kill -s KILL dashboard
sleep 12
sudo systemctl status dashboard  # Should be running again

# 10. Open in browser
# Visit: http://raspberrypi.local
```

---

## Quick Reference

```bash
# Setup
sudo cp dashboard.service /etc/systemd/system/
sudo systemctl daemon-reload
sudo systemctl enable dashboard
sudo systemctl start dashboard

# Daily operations
sudo systemctl restart dashboard     # Restart
sudo systemctl status dashboard      # Check status
sudo journalctl -u dashboard -f      # Watch logs

# Nginx
sudo systemctl restart nginx         # Restart nginx
sudo nginx -t                        # Test config
sudo tail -f /var/log/nginx/dashboard_error.log

# Troubleshooting
sudo journalctl -u dashboard -n 100  # View logs
systemctl show dashboard             # Show all properties
curl http://127.0.0.1:5050/api/system/health  # Test directly
```

---

## Uninstalling

To remove the service:

```bash
# Stop and disable service
sudo systemctl stop dashboard
sudo systemctl disable dashboard

# Remove service file
sudo rm /etc/systemd/system/dashboard.service

# Remove nginx config
sudo rm /etc/nginx/sites-enabled/dashboard
sudo rm /etc/nginx/sites-available/dashboard

# Reload
sudo systemctl daemon-reload
sudo systemctl restart nginx
```

---

## See Also

- [GETTING_STARTED.md](GETTING_STARTED.md) - Getting started guide
- [API.md](API.md) - Complete API documentation
- [ADDING_SERVICES.md](ADDING_SERVICES.md) - Adding new services

---

**Last Updated:** October 29, 2025
