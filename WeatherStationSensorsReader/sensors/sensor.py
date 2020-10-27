import logging
from statistics import mean
from time import sleep


class Sensor(object):
    """Base class for sensors"""

    NUMBER_OF_READS = 10
    SECONDS_BETWEEN_READS = 2

    def read(self):
        reads = []
        sensor_name = self.__class__.__name__

        for n in range(1, self.NUMBER_OF_READS):
            try:
                # TODO Validate with a matrix of values because some sensors will return several of them
                value = self._read_values()
                logging.debug(msg=f'Obtained "{value}" from the sensor "{sensor_name}". Attempt {n}.')

                reads.append(value)

                sleep(self.SECONDS_BETWEEN_READS)
            except Exception as e:
                logging.error(f'Error while reading from sensor "{sensor_name}". Attempt {n}. ', e)

        avg = mean(data=reads)
        logging.debug(msg=f'Average "{avg}" from the sensor "{sensor_name}".')

        return avg

    def _read_values(self):
        raise NotImplementedError('A sub-class must be implemented.')
