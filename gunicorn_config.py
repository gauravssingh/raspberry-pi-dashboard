"""
Gunicorn configuration for Raspberry Pi 3B (1GB RAM)
Optimized for low resource usage
"""
import multiprocessing

# Server socket
bind = "127.0.0.1:5050"
backlog = 64

# Worker processes - single worker for development and GPIO access
# Multiple workers cause GPIO resource conflicts
workers = 1
worker_class = "sync"
worker_connections = 50
max_requests = 1000  # Restart workers after 1000 requests to prevent memory leaks
max_requests_jitter = 50
timeout = 30
keepalive = 2

# Logging
accesslog = "./logs/gunicorn_access.log"
errorlog = "./logs/gunicorn_error.log"
loglevel = "info"
access_log_format = '%(h)s %(l)s %(u)s %(t)s "%(r)s" %(s)s %(b)s "%(f)s" "%(a)s"'

# Process naming
proc_name = "raspberry-pi-dashboard"

# Server mechanics
daemon = False
pidfile = None
umask = 0
user = None
group = None
tmp_upload_dir = None

# Memory optimization
# Disabled preload to avoid GPIO conflicts between workers
preload_app = False

