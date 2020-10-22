import logging


class Controller(object):
    """Base class for controllers"""

    def __init__(self, dao, sensor):
        self.dao = dao
        self.sensor = sensor

        logging.debug(msg=f'Started controller "{self.__class__.__name__}" with '
                      f'Sensor "{self.sensor.__class__.__name__}" and DAO "{self.dao.__class__.__name__}".')

    def execute(self):
        read_result = self.sensor.read()
        logging.info(msg=f'Obtained "{read_result}" from the sensor "{self.sensor.__class__.__name__}".')

        self.dao.insert(values=read_result)
        logging.info(msg=f'{read_result} inserted correctly.')
