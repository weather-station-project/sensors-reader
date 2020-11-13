import logging
from statistics import mean
from time import sleep


class Sensor(object):
    """Base class for sensors"""

    NUMBER_OF_READS = 5
    SECONDS_BETWEEN_READS = 5

    def get_read_averages(self):
        reads = []
        sensor_name = self.__class__.__name__

        for n in range(0, self.NUMBER_OF_READS):
            try:
                values = self.read_values()
                logging.debug(msg=f'Obtained "{values}" from the sensor "{sensor_name}". Attempt {n + 1}.')

                reads.append(values)
            except Exception:
                logging.error(f'Error while reading from sensor "{sensor_name}". Attempt {n + 1}. ', exc_info=True)

            sleep(self.SECONDS_BETWEEN_READS)

        averages = [mean(data=row) for row in reads]
        logging.debug(msg=f'Average "{averages}" from the sensor "{sensor_name}".')

        return averages

    def read_values(self):
        raise NotImplementedError('A sub-class must be implemented.')
