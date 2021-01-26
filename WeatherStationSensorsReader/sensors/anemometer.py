import logging
import math
import time

from gpiozero import Button


class Anemometer(object):
    """Represents the sensor which measures wind speed and wind gust"""

    GPIO_PORT_NUMBER = 5
    SAMPLES_COUNT = 5
    SECONDS_BETWEEN_SAMPLES = 5

    SENSOR_RADIUS_CM = 9.0
    SENSOR_CIRCUMFERENCE_LONG_KM = (2 * math.pi) * SENSOR_RADIUS_CM / 100000.0

    SENSOR_ADJUSTMENT = 1.18

    def __init__(self):
        self.signals_count = 0

        logging.debug(msg=f'Started anemometer on port "{self.GPIO_PORT_NUMBER}" in the sensor "{self.__class__.__name__}".')

    def get_wind_speed_samples(self):
        samples = []
        wind_speed_sensor = Button(pin=self.GPIO_PORT_NUMBER)
        wind_speed_sensor.when_pressed = self.spin

        for n in range(0, self.SAMPLES_COUNT):
            speed = self.get_speed_sample()
            samples.append(speed)

            logging.debug(msg=f'Speed sample obtained "{speed}" km/h. Attempt {n + 1}.')

        return samples

    def spin(self):
        self.signals_count = self.signals_count + 1

        logging.debug(msg=f'Signals count {self.signals_count}.')

    def get_speed_sample(self):
        self.signals_count = 0
        start_time = time.time()
        time.sleep(self.SECONDS_BETWEEN_SAMPLES)

        current_count = self.signals_count
        elapsed_seconds = time.time() - start_time
        return self.calculate_speed(current_signals_count=current_count, elapsed_seconds=elapsed_seconds)

    def calculate_speed(self, current_signals_count, elapsed_seconds):
        rotations = current_signals_count / 2.0
        speed_per_hour = ((self.SENSOR_CIRCUMFERENCE_LONG_KM * rotations) / elapsed_seconds) * 3600
        return speed_per_hour * self.SENSOR_ADJUSTMENT
