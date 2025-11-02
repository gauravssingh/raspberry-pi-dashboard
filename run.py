#!/usr/bin/env python3
"""
Development server entry point
For production, use wsgi.py with gunicorn
"""
import os
from app import create_app

# Get environment from ENV variable, default to development
env = os.environ.get('FLASK_ENV', 'development')
app = create_app(env)

if __name__ == '__main__':
    # Development server
    app.run(
        host='0.0.0.0',
        port=5050,
        debug=(env == 'development')
    )

