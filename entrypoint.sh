#!/bin/bash

# Set the default value for the APP_PORT variable

# Change to the app directory
cd /app/

# Run Gunicorn with the application
/opt/venv/bin/gunicorn --worker-tmp-dir code2graph.wsgi:application --bind "0.0.0.0:8000"
