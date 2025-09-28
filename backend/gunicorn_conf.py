import os

# Gunicorn config variables
bind = "0.0.0.0:" + os.environ.get("PORT", "8000")
workers = int(os.environ.get("WEB_CONCURRENCY", 2))
