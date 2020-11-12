FROM python:3.9.0-alpine3.12 # TODO MODIFY BY THE IMAGE FOR ARM
LABEL maintainer="David Leon <david.leon.m@gmail.com>"

# Copy the application
COPY WeatherStationSensorsReader /WeatherStationSensorsReader

# Install references
RUN pip install --upgrade pip
RUN pip install -r /WeatherStationSensorsReader/requirements.txt

# Configure the health check command
HEALTHCHECK CMD python -u /WeatherStationSensorsReader/health_check/health_check.py || exit 1

# Start the application
CMD ["python", "-u", "/WeatherStationSensorsReader/app/app.py"]