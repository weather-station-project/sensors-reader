import logging

from bme280pi import Sensor as Bme280Sensor

from sensors.sensor import Sensor


class AirMeasurementSensor(Sensor):
    """Represents the sensor which measures pressure and humidity"""

    def __init__(self):
        self.sensor = Bme280Sensor()
        logging.debug(msg=f'Started Bme280 with chip_id "{self.sensor.chip_id}" and '
                          f'chip_version "{self.sensor.chip_version}" in the sensor "{self.__class__.__name__}".')

        super().__init__()

    def get_reading(self):
        result = self.sensor.get_data()
        return [result['pressure'], result['humidity']]
