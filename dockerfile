# Use an official Python runtime as a parent image
FROM python:3.10-slim

# Set the working directory in the container
WORKDIR /app

# Copy the current directory contents into the container at /app
COPY . /app

# Install any needed packages specified in requirements.txt
RUN pip install --no-cache-dir -r requirements.txt

# Install supervisor
RUN apt-get update && apt-get install -y supervisor

# Copy the supervisord configuration file
COPY supervisord.conf /etc/supervisor/conf.d/supervisord.conf

# Make the shell script executable
RUN chmod +x /app/start_celery.sh

# Expose the port uvicorn will run on
EXPOSE 8081

# Run supervisord
CMD ["supervisord", "-c", "/etc/supervisor/conf.d/supervisord.conf"]