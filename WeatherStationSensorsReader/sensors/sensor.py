import logging
from abc import ABC, abstractmethod
from statistics import mean
from time import sleep

from exceptions.sensor_exception import SensorException
from health_check.health_check_file_manager import register_success_for_class_into_health_check_file


class Sensor(ABC):
    """Base class for sensors"""

    NUMBER_OF_READS = 5
    SECONDS_BETWEEN_READS = 10

    def get_read_averages(self):
        reads = []
        sensor_name = self.__class__.__name__

        for n in range(0, self.NUMBER_OF_READS):
            try:
                values = self.read_values()
                logging.debug(msg=f'Obtained "{values}" from the sensor "{sensor_name}". Attempt {n + 1}.')

                reads.append(values)
            except Exception:
                logging.exception(f'Error while reading from sensor "{sensor_name}". Attempt {n + 1}.')

            sleep(self.SECONDS_BETWEEN_READS)

        if len(reads) == 0:
            raise SensorException(class_name=sensor_name, message=f'The sensor "{sensor_name}" did not report any read.')

        averages = self.get_averages(reads=reads)
        logging.debug(msg=f'Average "{averages}" from the sensor "{sensor_name}".')
        register_success_for_class_into_health_check_file(class_name=sensor_name)

        return averages

    @abstractmethod
    def read_values(self):
        raise NotImplementedError('A sub-class must be implemented.')

    def get_averages(self, reads):
        return [mean(data=row) for row in list(zip(*reads))]
