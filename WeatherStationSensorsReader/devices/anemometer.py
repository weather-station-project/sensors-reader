import logging
import math
import time

from gpiozero import Button

from devices.samples_during_time_device import SamplesDuringTimeDevice


class Anemometer(SamplesDuringTimeDevice):
    """Represents the device which measures wind speed and wind gust"""

    SENSOR_RADIUS_CM = 9.0
    SENSOR_CIRCUMFERENCE_LONG_KM = (2 * math.pi) * SENSOR_RADIUS_CM / 100000.0

    SENSOR_ADJUSTMENT = 1.18

    def __init__(self, anemometer_port_number):
        self.signals_count = 0
        self.button = Button(pin=anemometer_port_number)
        self.button.when_pressed = self.spin

        logging.debug(msg=f'Started anemometer on port "{anemometer_port_number}" in the sensor "{self.__class__.__name__}".')

    def spin(self):
        self.signals_count = self.signals_count + 1

        logging.debug(msg=f'Signals count {self.signals_count}.')

    def get_sample(self):
        self.signals_count = 0
        start_time = time.time()
        time.sleep(self.SAMPLES_DURATION_IN_SECONDS)

        current_count = self.signals_count
        elapsed_seconds = time.time() - start_time

        speed = self.calculate_speed(current_signals_count=current_count, elapsed_seconds=elapsed_seconds)
        logging.debug(msg=f'Speed sample obtained "{speed}" km/h.')

        return speed

    def calculate_speed(self, current_signals_count, elapsed_seconds):
        rotations = current_signals_count / 2.0
        speed_per_hour = ((self.SENSOR_CIRCUMFERENCE_LONG_KM * rotations) / elapsed_seconds) * 3600
        return speed_per_hour * self.SENSOR_ADJUSTMENT

    def health_check(self):
        pass
