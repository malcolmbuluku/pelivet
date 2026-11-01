"""Gunicorn configuration for production.

Run with:  gunicorn --config gunicorn_config.py wsgi:app
"""
import multiprocessing

bind = "127.0.0.1:8000"
workers = multiprocessing.cpu_count() * 2 + 1
worker_class = "sync"
timeout = 60
keepalive = 5
accesslog = "-"      # stdout (captured by systemd/journald)
errorlog = "-"
loglevel = "info"
