# Dockerfile

# Use an official Python runtime as a base image
FROM python:3.11

# Set environment variables
COPY . /app
WORKDIR /app

RUN python3 -m venv /opt/venv
# Install system dependencies
RUN /opt/venv/bin/pip install pip --upgrade
RUN /opt/venv/bin/pip install -r requirements.txt
RUN chmod +x entrypoint.sh
# Install Python dependencies

CMD ["/app/entrypoint.sh"]

