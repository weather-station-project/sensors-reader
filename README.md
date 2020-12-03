# Weather Station Sensors Reader
Repository with the Weather Station Sensors Reader solution.

It is a dockerized Python application developed for [Raspberry Pi](https://www.raspberrypi.org/) and based on the open project "[Build your own weather station](https://projects.raspberrypi.org/en/projects/build-your-own-weather-station)". It uses the set of sensors described there to take some environment measurements and stores the information in the database described in the repository [Weather Station Database](https://github.com/davidleonm/weather-station-database).

The solution has been dockerized to ease its deployment and usage, but it can be executed in a Rasperry Pi natively with Python 3 installed.


## Solution overview
![Overview](https://github.com/davidleonm/weather-station-sensors-reader/raw/master/overview.png)

The rest of the solutions can be found in the other repositories in my [Github account](https://github.com/davidleonm).


## Components used and where to find them
As commented previously, the same components described in the project "[Build your own weather station](https://projects.raspberrypi.org/en/projects/build-your-own-weather-station)" have been used. Here is a list and where to find them (At least from Spain).

* **Bme280** - Ambient temperature, atmosphere pressure and air humidty sensor. +- 5€ [Ebay](https://www.ebay.es/itm/BME280-Temperatur-Sensor-Luftdruck-Feuchtigkeit-I2C-5V-Barometer-Arduino-Digital/253107395109?ssPageName=STRK%3AMEBIDX%3AIT&_trksid=p2057872.m2749.l2649)
* **Cables jumper Male - Female** - To join the sensors with the Raspberry Pi. +- 3€ [Ebay](https://www.ebay.es/itm/40-cables-jumper-protoboard-de-30cm-Macho-Hembra-cable-jumpers-Arduino-Elect/322771656278?ssPageName=STRK%3AMEBIDX%3AIT&_trksid=p2057872.m2749.l2649)
* **Cables jumper Female - Female** - To enlarge the cables if desired. +- 3€ [Ebay](https://www.ebay.es/itm/40-Cables-30cm-Hembra-Hembra-jumper-dupont-2-54-arduino-protoboar-cable-jumpers/322148283107?ssPageName=STRK%3AMEBIDX%3AIT&_trksid=p2057872.m2749.l2649)


## Composition
* **WeatherStationSensorsReader** - Folder with the solution and its unit tests.
* **Dockerfile** - Dockerfile to build the solution. Note that it is dockerized based on an ARMv6 Python image.
* **docker-compose.yml** - Example of compose file to run the solution from a Docker host. Note that the container must be launched with privileged mode enabled to be allowed to read information from the ic2 component.
* **Jenkins files** - Files with Jenkins pipelines, separating branches from master branch. They are using this [shared library](https://github.com/davidleonm/shared-library) project.
* **LICENSE** - File with the license, basically it says that you can use the code as you wish.
* **README.md** - This file!
* **sonar-project.properties** - File with configuration to execute Sonarqube analysis during master build.
* **VERSION** - Plain/text file with the version of the solution. It is used to tag the image once it is deployed.


## Usage
The solution is intended to take measurements from the environment and also to store the obtained values in a database passed as parameters. There are some parameters to define the behavior of the solution or just to limit some aspects of its execution, they are described below.

* **LOGGING_LEVEL** - Possible values are CRITICAL, ERROR, WARNING, INFO and DEBUG. It defines the level of loggin traces to register.
* **MINUTES_BETWEEN_READS** - By default, the app waits 5 minutes between measurements, with this parameter you can change the waiting time.
* **FAKE_SENSOR_ENABLED** - true / false. Just for testing purposes, instead of getting values from the sensors, random values are obtained. No values are inserted in the database but only showed in the log traces. It is useful for checking if the application runs correctly and it has access to the database configured. In case of configuring a fake sensor, the rest of the possible sensors defined are skipped.
* **BME_280_SENSOR_ENABLED** - true / false. In case of being enabled, the application will perform ambient temperatures, air humidity and atmosphere pressure measurements.
* **SERVER** - Database server. Measurements retrieved will not be stored anywhere, just showed in the log traces with INFO level.
* **DATABASE** - Database name
* **USER** - Database name
* **PASSWORD** - Database name

> :warning: There are more parameters defined in the code related to other sensors but they are not used yet.

A docker-compose example is provided with the solution code, but it can be launched via command-line. Either way, the container must be created with privileged permissions to be able to access to Raspberry Pi hardware.


### Example of an execution with all the sensors and database access available
```YAML
version: '3.5'
services:
  sensors-reader:
    container_name: sensors-reader
    image: davidleonm/weather-station-sensors-reader
    privileged: true
    restart: unless-stopped
    environment:
      - LOGGING_LEVEL: ERROR
      - BME_280_SENSOR_ENABLED: true
      - SERVER: <Type your value>
      - DATABASE: <Type your value>
      - USER: <Type your value>
      - PASSWORD: <Type your value>
    volumes:
    - '/etc/timezone:/etc/timezone:ro'
    - '/etc/localtime:/etc/localtime:ro'
```
```bash
docker run --rm -d --name=sensors-reader -e LOGGING_LEVEL=ERROR -e BME_280_SENSOR_ENABLED=true -e SERVER=xx -e DATABASE=xx -e USER=xx -e PASSWORD=xx -v /etc/timezone:/etc/timezone:ro -v /etc/localtime:/etc/localtime:ro davidleonm/weather-station-sensors-reader
```

### Example of an execution with only the fake sensor and without database
```YAML
version: '3.5'
services:
  sensors-reader:
    container_name: sensors-reader
    image: davidleonm/weather-station-sensors-reader
    restart: unless-stopped
    environment:
      - LOGGING_LEVEL: ERROR
      - FAKE_SENSOR_ENABLED: true
    volumes:
    - '/etc/timezone:/etc/timezone:ro'
    - '/etc/localtime:/etc/localtime:ro'
```
```bash
docker run --rm -d --name=sensors-reader -e LOGGING_LEVEL=ERROR -e FAKE_SENSOR_ENABLED=true -v /etc/timezone:/etc/timezone:ro -v /etc/localtime:/etc/localtime:ro davidleonm/weather-station-sensors-reader
```


## Changelog
* **First release** - First version with ambient temperature, air humidity and atmosphere pressure sensors.


## License
Use this code as you wish! Totally free to be copied/pasted.