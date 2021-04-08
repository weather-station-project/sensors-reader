import logging
from abc import ABC, abstractmethod
from statistics import mean
from threading import Thread
from time import sleep

from exceptions.sensor_exception import SensorException
from health_check.health_check_file_manager import register_success_for_class_into_health_check_file


class Sensor(ABC):
    """Base class for sensors"""

    SECONDS_BETWEEN_READINGS = 10

    def __init__(self):
        self.readings = []
        self.getting_readings = False

        thread = Thread(target=self.add_value_to_readings)
        thread.start()

    def add_value_to_readings(self):
        while self.get_true():
            try:
                sensor_name = self.__class__.__name__

                if self.getting_readings:
                    return

                reading = self.get_reading()
                self.readings.append(reading)
                logging.debug(msg=f'[{sensor_name}] Obtained "{reading}".')
            except Exception:
                logging.exception(f'[{sensor_name}] Error while reading.')
            finally:
                sleep(self.SECONDS_BETWEEN_READINGS)

    @staticmethod
    def get_true():
        # Stupid method for unit tests purposes to avoid infinite loop
        return True

    @abstractmethod
    def get_reading(self):
        raise NotImplementedError('A sub-class must be implemented.')

    def get_readings_average(self):
        try:
            self.getting_readings = True
            sensor_name = self.__class__.__name__

            if len(self.readings) == 0 or all(x is None for x in self.readings):
                raise SensorException(class_name=sensor_name, message=f'The sensor "{sensor_name}" did not report any read.')

            logging.debug(msg=f'Getting average from the values "{self.readings}"')
            average = self.get_average()
            register_success_for_class_into_health_check_file(class_name=sensor_name)

            return average
        finally:
            del self.readings[:]
            self.getting_readings = False

    def get_average(self):
        return [mean(data=row) for row in list(zip(*self.readings))]
