FROM arm32v6/python:3.9.0-alpine
LABEL maintainer="David Leon <david.leon.m@gmail.com>"

# Copy the application folder by folder because .gitignore does not work for me to skip unit tests
COPY WeatherStationSensorsReader/app /WeatherStationSensorsReader/app
COPY WeatherStationSensorsReader/controllers /WeatherStationSensorsReader/controllers
COPY WeatherStationSensorsReader/dao /WeatherStationSensorsReader/dao
COPY WeatherStationSensorsReader/exceptions /WeatherStationSensorsReader/exceptions
COPY WeatherStationSensorsReader/health_check /WeatherStationSensorsReader/health_check
COPY WeatherStationSensorsReader/main /WeatherStationSensorsReader/main
COPY WeatherStationSensorsReader/sensors /WeatherStationSensorsReader/sensors

# Install needed packages for Python libraries
RUN apk add --no-cache postgresql-dev \
                       gcc \
                       python3-dev \
                       musl-dev \
                       make \
                       build-base \
                       py3-smbus \
                       i2c-tools \
                       linux-headers

# Install Python references
RUN pip install --no-cache-dir --upgrade pip
RUN pip install --no-cache-dir --upgrade wheel
RUN pip install --no-cache-dir --upgrade setuptools
RUN pip install --no-cache-dir  psycopg2 bme280pi w1thermsensor

# Change working directory to the app binaries
WORKDIR /WeatherStationSensorsReader

# Configure the health check command
HEALTHCHECK CMD python -u -m health_check.health_check || exit 1

# Start the application
ENTRYPOINT ["python", "-u", "-m", "app.app"]