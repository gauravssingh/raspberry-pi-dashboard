"""
WSGI entry point for production deployment with gunicorn
Usage: gunicorn -c gunicorn_config.py wsgi:app
"""
from app import create_app

app = create_app('production')

if __name__ == '__main__':
    app.run()

