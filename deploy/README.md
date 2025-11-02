# Deployment Configuration Files

This directory contains all configuration files needed for deploying the Raspberry Pi Dashboard in production.

## 📁 Files Overview

| File | Purpose | Installation |
|------|---------|--------------|
| `dashboard.service` | Systemd service file | Copy to `/etc/systemd/system/` |
| `nginx.conf` | Basic nginx config (HTTP) | Copy to `/etc/nginx/sites-available/` |
| `nginx-ssl.conf` | Nginx config with HTTPS | Copy to `/etc/nginx/sites-available/` |
| `environment.example` | Environment variables template | Copy to `.env` in project root |

---

## 🚀 Quick Deployment

### 1. Install Systemd Service

```bash
# Copy service file
sudo cp deploy/dashboard.service /etc/systemd/system/dashboard.service
sudo chmod 644 /etc/systemd/system/dashboard.service

# Reload and enable
sudo systemctl daemon-reload
sudo systemctl enable dashboard
sudo systemctl start dashboard

# Check status
sudo systemctl status dashboard
```

### 2. Install Nginx (HTTP only)

```bash
# Copy nginx config
sudo cp deploy/nginx.conf /etc/nginx/sites-available/dashboard

# Enable site
sudo ln -s /etc/nginx/sites-available/dashboard /etc/nginx/sites-enabled/

# Test configuration
sudo nginx -t

# Restart nginx
sudo systemctl restart nginx
```

### 3. Install Nginx with SSL (HTTPS)

```bash
# First, get SSL certificate using certbot
sudo apt-get install certbot python3-certbot-nginx
sudo certbot --nginx -d yourdomain.com

# OR manually configure SSL in nginx-ssl.conf
sudo cp deploy/nginx-ssl.conf /etc/nginx/sites-available/dashboard

# Enable site
sudo ln -s /etc/nginx/sites-available/dashboard /etc/nginx/sites-enabled/

# Test and restart
sudo nginx -t
sudo systemctl restart nginx
```

---

## 📋 Configuration Details

### Systemd Service (`dashboard.service`)

**What it does:**
- Runs gunicorn with your Flask app
- Auto-starts on boot
- Auto-restarts on failure
- Limits resources (400MB RAM, 80% CPU)

**Configuration:**
- User: `gauravs`
- Working Directory: `/home/gauravs/dashboard`
- Port: `127.0.0.1:5050`
- Environment: Production

**Customize:**
Edit the file to change user, paths, or resource limits.

**Management:**
```bash
sudo systemctl start dashboard    # Start
sudo systemctl stop dashboard     # Stop
sudo systemctl restart dashboard  # Restart
sudo systemctl status dashboard   # Check status
sudo journalctl -u dashboard -f   # View logs
```

---

### Nginx Configuration (`nginx.conf`)

**What it does:**
- Proxies HTTP traffic to gunicorn (port 5050)
- Serves static files directly (faster)
- Adds security headers
- Enables gzip compression

**Configuration:**
- Listen: Port 80 (HTTP)
- Server names: `raspberrypi.local`, `localhost`
- Static files: `/home/gauravs/dashboard/app/static/`
- Proxy to: `http://127.0.0.1:5050`

**Customize:**
1. Update `server_name` with your hostname/domain
2. Update static files path if different
3. Adjust timeouts if needed

**Testing:**
```bash
sudo nginx -t                     # Test config
curl http://localhost/api/system/health  # Test endpoint
```

---

### Nginx SSL Configuration (`nginx-ssl.conf`)

**What it does:**
- Redirects HTTP to HTTPS
- Enables SSL/TLS encryption
- Enhanced security headers
- All features from basic nginx config

**Prerequisites:**
```bash
# Option 1: Use Let's Encrypt (recommended)
sudo apt-get install certbot python3-certbot-nginx
sudo certbot --nginx -d yourdomain.com

# Option 2: Self-signed certificate (testing only)
sudo openssl req -x509 -nodes -days 365 -newkey rsa:2048 \
  -keyout /etc/ssl/private/dashboard.key \
  -out /etc/ssl/certs/dashboard.crt
```

**Customize:**
1. Update `server_name` with your domain
2. Update SSL certificate paths
3. Adjust SSL protocols if needed

---

### Environment Variables (`environment.example`)

**What it does:**
- Template for environment-specific settings
- Keeps secrets out of code

**Usage:**
```bash
# Copy example file
cp deploy/environment.example .env

# Edit with your values
nano .env

# Load in systemd service (already configured)
```

---

## 🔐 Security Best Practices

### 1. Run as Non-Root User
✅ Service file already configured to run as `gauravs`

### 2. Use HTTPS
```bash
# Get free SSL certificate
sudo certbot --nginx -d yourdomain.com
```

### 3. Firewall Configuration
```bash
# Allow HTTP and HTTPS
sudo ufw allow 80/tcp
sudo ufw allow 443/tcp

# Block direct access to port 5050 (only nginx should access)
sudo ufw deny 5050/tcp
sudo ufw enable
```

### 4. Regular Updates
```bash
# Update system
sudo apt update && sudo apt upgrade -y

# Update Python packages
cd /home/gauravs/dashboard
source venv/bin/activate
pip install --upgrade -r requirements.txt
```

### 5. Change Secret Key
```bash
# Generate new secret key
python3 -c "import secrets; print(secrets.token_hex(32))"

# Add to .env file
echo "SECRET_KEY=your_generated_key" >> .env

# Update app/config.py to use it
```

---

## 🔍 Troubleshooting

### Service Won't Start

```bash
# Check logs
sudo journalctl -u dashboard -n 100

# Test manually
cd /home/gauravs/dashboard
source venv/bin/activate
gunicorn -c gunicorn_config.py wsgi:app
```

### Nginx 502 Bad Gateway

```bash
# Is gunicorn running?
sudo systemctl status dashboard

# Is it listening on port 5050?
sudo netstat -tlnp | grep 5050

# Check nginx error log
sudo tail -f /var/log/nginx/dashboard_error.log
```

### Permission Errors

```bash
# Fix ownership
sudo chown -R gauravs:gauravs /home/gauravs/dashboard

# Fix permissions
chmod -R 755 /home/gauravs/dashboard
chmod -R 644 /home/gauravs/dashboard/app/static/
```

### SSL Certificate Issues

```bash
# Renew certificate
sudo certbot renew

# Test SSL configuration
sudo nginx -t

# Check certificate expiry
sudo certbot certificates
```

---

## 📊 Monitoring

### Service Status
```bash
# Quick check
sudo systemctl is-active dashboard

# Detailed status
sudo systemctl status dashboard

# Resource usage
systemctl show dashboard | grep -E "Memory|CPU"
```

### Nginx Status
```bash
# Check if running
sudo systemctl status nginx

# Active connections
curl http://localhost/nginx_status  # (if configured)

# Log analysis
sudo tail -f /var/log/nginx/dashboard_access.log
```

### Application Logs
```bash
# Real-time logs
sudo journalctl -u dashboard -f

# Last 100 lines
sudo journalctl -u dashboard -n 100

# Errors only
sudo journalctl -u dashboard -p err
```

---

## 🔄 Updating the Application

### Standard Update Process

```bash
# 1. Stop service
sudo systemctl stop dashboard

# 2. Pull updates (if using git)
cd /home/gauravs/dashboard
git pull

# 3. Update dependencies
source venv/bin/activate
pip install -r requirements.txt --upgrade

# 4. Test
python run.py  # Ctrl+C after verifying

# 5. Restart service
sudo systemctl start dashboard

# 6. Check status
sudo systemctl status dashboard
sudo journalctl -u dashboard -f
```

### Zero-Downtime Update (Advanced)

```bash
# Reload gunicorn workers without dropping connections
sudo systemctl reload dashboard

# Or send HUP signal
sudo pkill -HUP -f gunicorn
```

---

## 📚 Additional Resources

- **Main Documentation**: `../docs/README.md`
- **Deployment Guide**: `../docs/DEPLOYMENT.md`
- **Systemd Service Guide**: `../docs/SYSTEMD_SERVICE.md`
- **Quick Start**: `../docs/QUICK_START.md`

---

## 🎯 Deployment Checklist

Before going live:

- [ ] Systemd service installed and running
- [ ] Nginx installed and configured
- [ ] SSL certificate installed (if using HTTPS)
- [ ] Firewall configured (ufw or iptables)
- [ ] Environment variables set (if needed)
- [ ] Secret key changed from default
- [ ] Regular backups configured
- [ ] Monitoring set up
- [ ] Tested all endpoints
- [ ] Tested from external network
- [ ] Documentation updated with your specifics

---

**Last Updated:** October 29, 2025

