import logging


class Controller(object):
    """Base class for controllers"""

    def __init__(self, sensor, dao):
        self.sensor = sensor
        self.dao = dao

        logging.debug(msg=f'Started controller "{self.__class__.__name__}" with '
                          f'Sensor "{self.sensor.__class__.__name__}" and DAO "{self.dao.__class__.__name__}".')

    def execute(self):
        read_result = self.sensor.get_read_averages()
        logging.info(msg=f'Obtained "{read_result}" from the sensor "{self.sensor.__class__.__name__}".')

        self.dao.insert(values=read_result)
        logging.info(msg=f'{read_result} inserted correctly.')

    def health_check(self):
        self.sensor.read_values()
        self.dao.health_check()
