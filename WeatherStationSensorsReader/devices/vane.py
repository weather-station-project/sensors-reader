import logging
import math

from gpiozero import MCP3008


class Vane(object):
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

        logging.debug(msg=f'Started vane on the channel "{self.CHANNEL}".')

    def get_reading(self):
        mcp_value = self.mcp_chip.value
        gpio_value = round(mcp_value * self.VOLTAGE_IN, 1)

        logging.debug(msg=f'MCP reading "{mcp_value}", GPIO value "{gpio_value}".')

        if gpio_value in self.VANE_ANGLES_AND_DIRECTIONS_TABLE:
            return self.VANE_ANGLES_AND_DIRECTIONS_TABLE[gpio_value]['angle']

        logging.warning(msg=f'Cannot determine wind direction for MCP reading "{mcp_value}" and GPIO value "{gpio_value}".')
        return None

    def get_direction_average(self, angles):
        angles_average = self.get_angles_average(angles=angles)
        return self.get_direction_by_angle(angle=angles_average)

    @staticmethod
    def get_angles_average(angles):
        sin_sum = 0.0
        cos_sum = 0.0
        valid_angles_count = 0.0

        for angle in angles:
            if angle is None:
                continue
            valid_angles_count = valid_angles_count + 1.0
            radians = math.radians(angle)
            sin_sum += math.sin(radians)
            cos_sum += math.cos(radians)

        if valid_angles_count == 0:
            return None

        s = sin_sum / valid_angles_count
        c = cos_sum / valid_angles_count
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
