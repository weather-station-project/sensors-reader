# Weather Station Sensors Reader
Repository with the Weather Station Sensors Reader solution.

Based on the open project for Raspberry Pi "[Build your own weather station](https://projects.raspberrypi.org/en/projects/build-your-own-weather-station)".


## Release information
[![Coverage Status](https://coveralls.io/repos/github/weather-station-project/sensors-reader/badge.svg?branch=origin/master)](https://coveralls.io/github/weather-station-project/sensors-reader?branch=origin/master)
![Docker Image Version (latest by date)](https://img.shields.io/docker/v/weatherstationproject/sensors-reader)


## Components used and where to find them
As commented previously, the same components described in the project "[Build your own weather station](https://projects.raspberrypi.org/en/projects/build-your-own-weather-station)" have been used. Here is a list and where to find them (At least from Spain).

* **Raspberry Pi** - Actually I'm using the very old Raspberry Pi 1, hence high hardware requirements are not needed. You may have enough with a Raspberry Pi Zero W. ~ 30€ [Amazon](https://www.amazon.es/GeeekPi-Raspberry-interruptor-destornillador-transparente/dp/B08H16DP17/ref=sr_1_2?__mk_es_ES=%C3%85M%C3%85%C5%BD%C3%95%C3%91&crid=1VYNOJP47JN9G&dchild=1&keywords=raspberry%2Bpi%2Bzero&qid=1608051397&quartzVehicle=3443-1424&replacementKeywords=raspberry%2Bpi&sprefix=raspberry%2Bpi%2Bzero%2Caps%2C247&sr=8-2&th=1)
* **Micro SD** - I'm using a very old 4 GB SD card, so I guess it is enough with a 8GB micro SD card, but as they are cheap, you choose your desired capacity. ~ 6€ [Amazon](https://www.amazon.es/SanDisk-Ultra-Android-microSDHC-adaptador/dp/B073K14CVB/ref=sr_1_6?__mk_es_ES=%C3%85M%C3%85%C5%BD%C3%95%C3%91&dchild=1&keywords=micro+sd+8gb&qid=1608051936&sr=8-6)
* **Raspberry Pi OS** - Download it from the official [page](https://www.raspberrypi.org/software/operating-systems/)!
* **Bme280** - Ambient temperature, atmosphere pressure and air humidity sensor. ~ 5€ [Ebay](https://www.ebay.es/itm/BME280-Temperatur-Sensor-Luftdruck-Feuchtigkeit-I2C-5V-Barometer-Arduino-Digital/253107395109?ssPageName=STRK%3AMEBIDX%3AIT&_trksid=p2057872.m2749.l2649)
* **Cables jumper Male - Female** - To join the sensors with the Raspberry Pi. ~ 3€ [Ebay](https://www.ebay.es/itm/40-cables-jumper-protoboard-de-30cm-Macho-Hembra-cable-jumpers-Arduino-Elect/322771656278?ssPageName=STRK%3AMEBIDX%3AIT&_trksid=p2057872.m2749.l2649)
* **Cables jumper Female - Female** - To enlarge the cables if desired. ~ 3€ [Ebay](https://www.ebay.es/itm/40-Cables-30cm-Hembra-Hembra-jumper-dupont-2-54-arduino-protoboar-cable-jumpers/322148283107?ssPageName=STRK%3AMEBIDX%3AIT&_trksid=p2057872.m2749.l2649)
* **DS18B20 temperature sensor** - Ground temperature sensor, to measure the temperature on the ground as it may be colder above all in winter with snow. ~ 3.65€ [Ebay](https://www.ebay.es/itm/SONDA-TEMPERATURA-DS18B20-2-METROS-SENSOR-SUMERGIBLE-ARDUINO/254669776886?ssPageName=STRK%3AMEBIDX%3AIT&_trksid=p2060353.m2749.l2649)
* **4.7K Ohm Resistor** - Do not ask me why... my idea about circuits is really limited. ~ 1.39€ [Ebay](https://www.ebay.es/itm/50x-Resistencias-4-7-Kohm-4K7-OHM-5-1-4w-0-25w-carb%C3%B3n-film-pelicula/254289922617?ssPageName=STRK%3AMEBIDX%3AIT&_trksid=p2060353.m2749.l2649)
* **Breadboard** - To mount sensors and cables. ~ 1.30€ [Ebay](https://www.ebay.es/itm/Protoboard-400-puntos-con-lineas-contactos-breadboard-ARDUINO-prototipo-400p/322093153348?ssPageName=STRK%3AMEBIDX%3AIT&_trksid=p2060353.m2749.l2649)
* **5mm Terminals** - To join cables and electronic components on the breadboard. ~ 1.29€ [Ebay](https://www.ebay.es/itm/10x-Borna-2-pines-VERDE-Conexion-5mm-Clema-2p-PCB-enlazable-tornillo-terminal/221798044214?ssPageName=STRK%3AMEBIDX%3AIT&_trksid=p2060353.m2749.l2649)
* **Rigid cables** - To make bridges between different lines on the proto board. ~ 1€ [Ebay](https://www.ebay.es/itm/6-Metros-de-Cable-Rigido-a-COLOR-protoboard-arduino-electronica-puentes-proto/283452899154?ssPageName=STRK%3AMEBIDX%3AIT&_trksid=p2060353.m2749.l2649)
* **Digital-analogical converter** - To be able to analyze vane analogical signals. ~ 3.5€ [Ebay](https://www.ebay.es/itm/1x-MCP3008-DIP16-MCP3008-I-P-DIP-16-Convertidor-De-Analogico-A-Digital-Espa%C3%B1a/223996555390?ssPageName=STRK%3AMEBIDX%3AIT&_trksid=p2060353.m2749.l2649)
* **RJ11 breakout** - To join RJ11 devices with the proto board. ~ (8.39 * 2)€ [Amazon](https://www.amazon.es/gp/product/B00UJ8DRCG/ref=ppx_yo_dt_b_asin_title_o04_s00?ie=UTF8&psc=1)
* **Anemometer** - To measure wind speed and gust speed. ~ 32.9€ [Amazon](https://www.amazon.es/gp/product/B07BMVYBW9/ref=ppx_yo_dt_b_asin_title_o05_s00?ie=UTF8&psc=1)
* **Vane** - To measure wind direction. ~ 29.9€ [Amazon](https://www.amazon.es/gp/product/B07KYTKLTB/ref=ppx_yo_dt_b_asin_title_o05_s00?ie=UTF8&psc=1)
* **Rain gauge** - To measure amount of rain. ~ 33.90€ [Amazon](https://www.amazon.es/gp/product/B07KYSXCBZ/ref=ppx_yo_dt_b_asin_title_o05_s00?ie=UTF8&psc=1)


## Composition
* **WeatherStationSensorsReader** - Folder with the solution and its unit tests.
* **.coveragerc** - File with configuration for the coverage tests, to skip virtual environment folders.
* **Dockerfile** - Dockerfile to build the solution. Note that it is dockerized based on an ARMv6 Python image.
* **docker-compose.yml** - Example of compose file to run the solution from a Docker host. Note that the container must be launched with privileged mode enabled to be allowed to read information from the ic2 component.
* **Jenkins files** - Files with Jenkins pipelines, separating branches from master branch. They are using this [shared library](https://github.com/davidleonm/shared-library) project.
* **LICENSE** - File with the license, basically it says that you can use the code as you wish.
* **README.md** - This file!
* **sonar-project.properties** - File with configuration to execute Sonarqube analysis during master build.
* **VERSION** - Plain/text file with the version of the solution. It is used to tag the image once it is deployed.


## Usage
### Pre-requisites
* All the components must be connected to the Raspberry Pi follow the link about the project to know how to do it.
* The device needs a LAN connection, either Wi-Fi or wired.
* I2C interface must be enabled. Follow this [tutorial](https://www.raspberrypi-spy.co.uk/2014/11/enabling-the-i2c-interface-on-the-raspberry-pi/).
* 1-wire interface must be enabled. Follow this [tutorial](https://www.raspberrypi-spy.co.uk/2018/02/enable-1-wire-interface-raspberry-pi/).


### Execution parameters
The solution is intended to take measurements from the environment and also to store the obtained values in a database passed as parameters. There are some parameters to define the behavior of the solution or just to limit some aspects of its execution, they are described below.

* **LOGGING_LEVEL** - Possible values are CRITICAL, ERROR, WARNING, INFO and DEBUG. It defines the level of logging traces to register.
* **MINUTES_BETWEEN_READS** - By default, the app waits 5 minutes between measurements, with this parameter you can change the waiting time.
* **FAKE_SENSOR_ENABLED** - true / false. Just for testing purposes, instead of getting values from the sensors, random values are obtained. No values are inserted in the database but only showed in the log traces. It is useful for checking if the application runs correctly and it has access to the database configured. In case of configuring a fake sensor, the rest of the possible sensors defined are skipped.
* **BME_280_SENSOR_ENABLED** - true / false. In case of being enabled, the application will perform ambient temperatures, air humidity and atmosphere pressure measurements.
* **GROUND_SENSOR_ENABLED** - true / false. In case of being enabled, the application will perform ground temperature measurements.
* **WIND_SENSOR_ENABLED** - true / false. In case of being enabled, the application will perform wind measurements such as wind speed, gust speed and wind direction.
* **RAINFALL_SENSOR_ENABLED** - true / false. In case of being enabled, the application will perform amount of rain measurements.
* **ANEMOMETER_PORT_NUMBER** - The GPIO port number where the anemometer device is connected to.
* **RAIN_GAUGE_PORT_NUMBER** - The GPIO port number where the rain gauge device is connected to.
* **SERVER** - Database server. In case of it is empty, measurements retrieved will not be stored anywhere, just showed in the log traces with INFO level.
* **DATABASE** - Database name
* **USER** - Database name
* **PASSWORD** - Database name

A docker-compose example is provided with the solution code, but it can be launched via command-line. Either way, the container must be created with privileged permissions to be able to access to Raspberry Pi hardware.


### Example of an execution with all the sensors and database access available
```YAML
version: '3.5'
services:
  sensors-reader:
    container_name: sensors-reader
    image: weatherstationproject/sensors-reader
    privileged: true
    restart: unless-stopped
    environment:
      - LOGGING_LEVEL=ERROR
      - BME_280_SENSOR_ENABLED=true
      - GROUND_SENSOR_ENABLED=true
      - WIND_SENSOR_ENABLED=true
      - RAINFALL_SENSOR_ENABLED=true
      - ANEMOMETER_PORT_NUMBER=22
      - RAIN_GAUGE_PORT_NUMBER=25
      - SERVER=127.0.0.1
      - DATABASE=my_db
      - USER=my_user
      - PASSWORD=my_password
    volumes:
    - '/etc/timezone:/etc/timezone:ro'
    - '/etc/localtime:/etc/localtime:ro'
```
```bash
docker run --rm -d --name=sensors-reader --privileged -e LOGGING_LEVEL=ERROR -e BME_280_SENSOR_ENABLED=true -e GROUND_SENSOR_ENABLED=true -e WIND_SENSOR_ENABLED=true -e RAINFALL_SENSOR_ENABLED=true -e ANEMOMETER_PORT_NUMBER=22 -e RAIN_GAUGE_PORT_NUMBER=25 -e SERVER=127.0.0.1 -e DATABASE=my_db -e USER=my_user -e PASSWORD=my_password -v /etc/timezone:/etc/timezone:ro -v /etc/localtime:/etc/localtime:ro davidleonm/weather-station-sensors-reader
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
      - LOGGING_LEVEL=ERROR
      - FAKE_SENSOR_ENABLED=true
    volumes:
    - '/etc/timezone:/etc/timezone:ro'
    - '/etc/localtime:/etc/localtime:ro'
```
```bash
docker run --rm -d --name=sensors-reader -e LOGGING_LEVEL=ERROR -e FAKE_SENSOR_ENABLED=true -v /etc/timezone:/etc/timezone:ro -v /etc/localtime:/etc/localtime:ro davidleonm/weather-station-sensors-reader
```


## Change-log
* **1.3.0** - Added rain gauge device to measure amount of rain. Improved the way to gather measurements.
* **1.2.0** - Added wind sensors such as the anemometer and the vane. Restructuring of Jenkins files. Improved the health check.
* **1.1.0** - Added ground temperature sensor, fixed some code smells and documentation.
* **1.0.0** - First version with ambient temperature, air humidity and atmosphere pressure sensors.


## License
Use this code as you wish! Totally free to be copied/pasted.


## Donation
If you liked the repository, you found it useful and you are willing to contribute, don't hesitate! I will be very grateful! :-)

[![paypal](https://www.paypalobjects.com/en_US/i/btn/btn_donateCC_LG.gif)](https://www.paypal.com/cgi-bin/webscr?cmd=_donations&business=4TFR2PQ2J3KLA&item_name=If+you+liked+the+project+and+you+are+willing+to+contribute%2C+don%27t+hesitate%21+I+will+be+very+grateful%21+%3A-%29&currency_code=EUR)
