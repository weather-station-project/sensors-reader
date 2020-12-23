import logging
import os

if os.name != 'nt':
    from w1thermsensor import W1ThermSensor

from sensors.sensor import Sensor


class GroundTemperatureSensor(Sensor):
    """Represents the sensor which measures ground temperature"""

    def __init__(self):
        self.sensor = W1ThermSensor()
        logging.debug(msg=f'Started W1ThermSensor with id "{self.sensor.id}" and '
                          f'type "{self.sensor.type_name}" in the sensor "{self.__class__.__name__}".')

    def read_values(self):
        return [self.sensor.get_temperature(unit=self.sensor.DEGREES_C)]
