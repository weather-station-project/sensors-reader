import logging
import math
import time

from gpiozero import Button


class Anemometer(object):
    """Represents the device which measures wind speed"""

    SENSOR_RADIUS_CM = 9.0
    SENSOR_CIRCUMFERENCE_LONG_KM = (2 * math.pi) * SENSOR_RADIUS_CM / 100000.0
    SENSOR_ADJUSTMENT = 1.18

    def __init__(self, anemometer_port_number):
        self.spin_count = 0
        self.start_time = time.time()
        self.button = Button(pin=anemometer_port_number)
        self.button.when_pressed = self.spin

        logging.debug(msg=f'Started anemometer on the port "{anemometer_port_number}".')

    def spin(self):
        self.spin_count = self.spin_count + 1
        logging.debug(msg=f'Spin count {self.spin_count}.')

    def get_speed(self):
        try:
            current_count = self.spin_count
            elapsed_seconds = time.time() - self.start_time

            return self.calculate_speed(current_spin_count=current_count, elapsed_seconds=elapsed_seconds)
        finally:
            self.spin_count = 0
            self.start_time = time.time()

    def calculate_speed(self, current_spin_count, elapsed_seconds):
        rotations = current_spin_count / 2.0
        speed_per_hour = ((self.SENSOR_CIRCUMFERENCE_LONG_KM * rotations) / elapsed_seconds) * 3600
        return speed_per_hour * self.SENSOR_ADJUSTMENT
