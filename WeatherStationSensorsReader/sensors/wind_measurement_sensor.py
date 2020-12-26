import logging
import math
from datetime import time
from statistics import mean
from time import sleep

from gpiozero import Button

from sensors.sensor import Sensor


class WindMeasurementSensor(Sensor):
    """Represents the sensor which measures wind speed, direction and gust"""

    GPIO_PORT_NUMBER = 5
    SAMPLES_COUNT = 5
    SECONDS_BETWEEN_SAMPLES = 5

    SENSOR_RADIUS_CM = 9.0
    SENSOR_CIRCUMFERENCE_LONG_KM = (2 * math.pi) * SENSOR_RADIUS_CM / 100000.0

    SENSOR_ADJUSTMENT = 1.18

    def __init__(self):
        self.signals_count = 0

        logging.debug(msg=f'Started anemometer on port "{self.GPIO_PORT_NUMBER}" in the sensor "{self.__class__.__name__}".')

    def read_values(self):
        wind_samples = self.get_samples()

        wind_speed = mean(data=wind_samples)
        gust_speed = max(wind_samples)
        direction = -1

        return [direction, wind_speed, gust_speed]

    def get_samples(self):
        samples = []
        wind_speed_sensor = Button(self.GPIO_PORT_NUMBER)
        wind_speed_sensor.when_pressed = self.spin

        for n in range(0, self.SAMPLES_COUNT):
            self.signals_count = 0
            start_time = time.time()
            sleep(self.SECONDS_BETWEEN_SAMPLES)

            current_count = self.signals_count
            elapsed_seconds = time.time() - start_time
            samples.append(self.get_speed(current_signals_count=current_count, elapsed_seconds=elapsed_seconds))

        return samples

    def spin(self):
        self.signals_count = self.signals_count + 1

        logging.debug(msg=f'Wind count {self.signals_count}.')

    def get_speed(self, current_signals_count, elapsed_seconds):
        rotations = current_signals_count / 2.0
        speed_per_hour = ((self.SENSOR_CIRCUMFERENCE_LONG_KM * rotations) / elapsed_seconds) * 3600
        return speed_per_hour * self.SENSOR_ADJUSTMENT
