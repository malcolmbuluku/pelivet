"""WSGI entry point for Gunicorn: `gunicorn --config gunicorn_config.py wsgi:app`."""
from app import create_app

app = create_app()
