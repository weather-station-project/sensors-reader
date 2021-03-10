import logging
import math
from threading import Thread
from time import sleep

from gpiozero import MCP3008

from devices.samples_during_time_device import SamplesDuringTimeDevice


class Vane(SamplesDuringTimeDevice):
    """Represents the device which measures wind direction"""

    CHANNEL = 0
    VOLTAGE_IN = 3.3

    SECONDS_BETWEEN_SAMPLES = 5

    UNKNOWN_WIND_DIRECTION = '-'
    VANE_ANGLES_AND_DIRECTIONS_TABLE = {0.4: {'direction': 'N', 'angle': 0.0},
                                        1.4: {'direction': 'N-NE', 'angle': 22.5},
                                        1.2: {'direction': 'N-E', 'angle': 45.0},
                                        2.8: {'direction': 'E-NE', 'angle': 67.5},
                                        2.7: {'direction': 'E', 'angle': 90.0},
                                        2.9: {'direction': 'E-SE', 'angle': 112.5},
                                        2.2: {'direction': 'S-E', 'angle': 135.0},
                                        2.5: {'direction': 'S-SE', 'angle': 157.5},
                                        1.8: {'direction': 'S', 'angle': 180.0},
                                        2.0: {'direction': 'S-SW', 'angle': 202.5},
                                        0.7: {'direction': 'S-W', 'angle': 225.0},
                                        0.8: {'direction': 'W-SW', 'angle': 247.5},
                                        0.1: {'direction': 'W', 'angle': 270.0},
                                        0.3: {'direction': 'W-NW', 'angle': 292.5},
                                        0.2: {'direction': 'N-W', 'angle': 315.0},
                                        0.6: {'direction': 'N-NW', 'angle': 337.5}}

    def __init__(self):
        self.mcp_chip = MCP3008(channel=self.CHANNEL)
        self.samples = []
        self.getting_sample = False
        thread = Thread(target=self.add_value_to_samples)
        thread.start()

        logging.debug(msg=f'Started vane on the channel "{self.CHANNEL}".')

    def add_value_to_samples(self):
        while self.get_true:
            try:
                if self.getting_sample:
                    return

                mcp_value = self.mcp_chip.value
                gpio_value = round(mcp_value * self.VOLTAGE_IN, 1)

                logging.debug(msg=f'MCP reading "{mcp_value}", GPIO value "{gpio_value}".')

                if gpio_value in self.VANE_ANGLES_AND_DIRECTIONS_TABLE:
                    sample = self.VANE_ANGLES_AND_DIRECTIONS_TABLE[gpio_value]['angle']
                    logging.debug(msg=f'Wind sample obtained "{sample}" degrees.')
                    self.samples.append(sample)
                else:
                    logging.debug(msg=f'Cannot determine wind direction for MCP reading "{mcp_value}" and GPIO value "{gpio_value}".')
            finally:
                sleep(self.SECONDS_BETWEEN_SAMPLES)

    @staticmethod
    def get_true():
        return True

    def get_sample(self):
        try:
            self.getting_sample = True

            average = self.get_angles_average()
            del self.samples[:]
            return average
        finally:
            self.getting_sample = False

    def get_direction_average(self, angles):
        angles_average = self.get_angles_average(angles=angles)
        return self.get_direction_by_angle(angle=angles_average)

    def get_angles_average(self, angles):
        if not angles:
            return None

        sin_sum = 0.0
        cos_sum = 0.0

        for angle in angles:
            radians = math.radians(angle)
            sin_sum += math.sin(radians)
            cos_sum += math.cos(radians)

        float_length = float(len(angles))
        s = sin_sum / float_length
        c = cos_sum / float_length
        arc = 0 if c == 0 else math.degrees(math.atan(s / c))

        average = 0.0
        if s > 0 and c > 0:
            average = arc
        elif c < 0:
            average = arc + 180
        elif s < 0 and c > 0:
            average = arc + 360

        return 0.0 if average == 360 else average

    def get_direction_by_angle(self, angle):
        if angle is None:
            return self.UNKNOWN_WIND_DIRECTION

        current_direction = None
        for _, data in self.VANE_ANGLES_AND_DIRECTIONS_TABLE.items():
            if data['angle'] > angle:
                return current_direction

            current_direction = data['direction']

        return self.UNKNOWN_WIND_DIRECTION
