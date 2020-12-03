# Weather Station Sensors Reader
Repository with the Weather Station Sensors Reader solution.

It is a dockerized Python application developed for [Raspberry Pi](https://www.raspberrypi.org/) and based on the open project "[Build your own weather station](https://projects.raspberrypi.org/en/projects/build-your-own-weather-station)". It uses the set of sensors described there to take some environment measurements and stores the information in the database described in the repository [Weather Station Database](https://github.com/davidleonm/weather-station-database).

The solution has been dockerized to ease its deployment and usage, but it can be executed in a Rasperry Pi natively with Python 3 installed.

## Solution overview
![Overview](https://github.com/davidleonm/weather-station-sensors-reader/raw/master/overview.png)

The rest of the solutions can be found in the other repositories in my [Github account](https://github.com/davidleonm).

## Components used and where to find them
As commented previously, the same components described in the project "[Build your own weather station](https://projects.raspberrypi.org/en/projects/build-your-own-weather-station)" have been used. Here is a list and where to find them (At least from Spain).

* **Bme280** - Temperature, atmosphere pressure and air humidty sensor. +- 5€ [Ebay](https://www.ebay.es/itm/BME280-Temperatur-Sensor-Luftdruck-Feuchtigkeit-I2C-5V-Barometer-Arduino-Digital/253107395109?ssPageName=STRK%3AMEBIDX%3AIT&_trksid=p2057872.m2749.l2649)
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
The app runs a listener on the port 9999. Using curl, any browser or a rest client, you can get the result.
Being Python 3 previously installed, just execute:
```bash
python hello_world.py
```
And to query the API:
```bash
curl http://127.0.0.1:9999/helloworld
```

## Changelog
* **First release** - First version with ambient temperature, air humidity and atmosphere pressure sensors.

## License
Use this code as you wish! Totally free to be copied/pasted.