import logging

from bme280pi import Sensor as Bme280Sensor

from sensors.sensor import Sensor


class AmbientTemperatureSensor(Sensor):
    """Represents the sensor which measures ambient temperature"""

    def __init__(self):
        self.sensor = Bme280Sensor()
        logging.debug(msg=f'[{self.__class__.__name__}] Started Bme280 with chip_id "{self.sensor.chip_id}" and '
                          f'chip_version "{self.sensor.chip_version}".')

        super().__init__()

    def get_reading(self):
        return [self.sensor.get_temperature(unit='C')]
