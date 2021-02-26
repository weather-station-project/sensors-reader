import logging
import math
from time import sleep

from gpiozero import MCP3008

from devices.samples_during_time_device import SamplesDuringTimeDevice


class Vane(SamplesDuringTimeDevice):
    CHANNEL = 0
    VOLTAGE_IN = 3.3
    NUMBER_OF_SAMPLES = 5
    UNKNOWN_WIND_ANGLE = -1
    VANE_ANGLES_AND_DIRECTIONS_TABLE = {-1: {'direction': '-', 'angle': UNKNOWN_WIND_ANGLE},
                                        0.4: {'direction': 'N', 'angle': 0.0},
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

        logging.debug(msg=f'Started vane on the channel "{self.CHANNEL}".')

    def get_sample(self):
        time_sleeping = self.SAMPLES_DURATION_IN_SECONDS / self.NUMBER_OF_SAMPLES
        samples = []

        for _ in range(0, self.NUMBER_OF_SAMPLES):
            sample = self.get_wind_direction_angle()

            if sample:
                samples.append(sample)
                logging.debug(msg=f'Wind sample obtained "{sample}" degrees.')

            sleep(time_sleeping)

        average = self.get_angles_average(angles=samples)
        return average

    def get_wind_direction_angle(self):
        mcp_value = self.mcp_chip.value
        gpio_value = round(mcp_value * self.VOLTAGE_IN, 1)

        if gpio_value not in self.VANE_ANGLES_AND_DIRECTIONS_TABLE:
            logging.debug(msg=f'Cannot determine wind direction for MCP reading "{mcp_value}".')
            return None

        return self.VANE_ANGLES_AND_DIRECTIONS_TABLE[gpio_value]['angle']

    def get_direction_average(self, direction_angles):
        direction_angles_average = self.get_angles_average(angles=direction_angles)
        return self.get_direction_by_direction_angle(direction_angle=direction_angles_average)

    def get_angles_average(self, angles):
        if not angles:
            return self.UNKNOWN_WIND_ANGLE

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

    def get_direction_by_direction_angle(self, direction_angle):
        current_direction = None

        for _, data in self.VANE_ANGLES_AND_DIRECTIONS_TABLE.items():
            if data['angle'] > direction_angle:
                return current_direction

            current_direction = data['direction']

        return None
