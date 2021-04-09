import logging

from w1thermsensor import W1ThermSensor

from sensors.sensor import Sensor


class GroundTemperatureSensor(Sensor):
    """Represents the sensor which measures ground temperature"""

    def __init__(self):
        self.sensor = W1ThermSensor()
        logging.debug(msg=f'[{self.__class__.__name__}] Started W1ThermSensor with id "{self.sensor.id}".')

        super().__init__()

    def get_reading(self):
        return [self.sensor.get_temperature()]
