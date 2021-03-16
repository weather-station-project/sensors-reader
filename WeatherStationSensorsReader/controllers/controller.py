import logging
from abc import ABC


class Controller(ABC):
    """Base class for controllers"""

    def __init__(self, sensor, dao):
        self.sensor = sensor
        self.dao = dao

        logging.debug(msg=f'Started controller "{self.__class__.__name__}" with '
                          f'Sensor "{self.sensor.__class__.__name__}" and DAO "{self.dao.__class__.__name__}".')

    def execute(self):
        readings_average = self.sensor.get_readings_average()
        logging.info(msg=f'Obtained "{readings_average}" from the sensor "{self.sensor.__class__.__name__}".')

        self.dao.insert(values=readings_average)
        logging.info(msg=f'{readings_average} inserted correctly.')
