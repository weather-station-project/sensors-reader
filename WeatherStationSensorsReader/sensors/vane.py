import logging
import math

import MCP342X


class Vane(object):
    ADC_CHANNEL = 0
    ADDRESS = 0x69
    VOLTAGE_IN = 3.268
    VOLTAGE_DIVIDER = 75000
    VANE_ANGLES_AND_DIRECTIONS_TABLE = [{'direction': 'N', 'angle': 0.0, 'ohms': 33000},
                                        {'direction': 'N-NE', 'angle': 22.5, 'ohms': 6570},
                                        {'direction': 'N-E', 'angle': 45.0, 'ohms': 8200},
                                        {'direction': 'E-NE', 'angle': 67.5, 'ohms': 891},
                                        {'direction': 'E', 'angle': 90.0, 'ohms': 1000},
                                        {'direction': 'E-SE', 'angle': 112.5, 'ohms': 688},
                                        {'direction': 'S-E', 'angle': 135.0, 'ohms': 2200},
                                        {'direction': 'S-SE', 'angle': 157.5, 'ohms': 1410},
                                        {'direction': 'S', 'angle': 180.0, 'ohms': 3900},
                                        {'direction': 'S-SW', 'angle': 202.5, 'ohms': 3140},
                                        {'direction': 'S-W', 'angle': 225.0, 'ohms': 16000},
                                        {'direction': 'W-SW', 'angle': 247.5, 'ohms': 14120},
                                        {'direction': 'W', 'angle': 270.0, 'ohms': 120000},
                                        {'direction': 'W-NW', 'angle': 292.5, 'ohms': 42120},
                                        {'direction': 'N-W', 'angle': 315.0, 'ohms': 64900},
                                        {'direction': 'N-NW', 'angle': 337.5, 'ohms': 21880}]

    def __init__(self):
        self.adc = MCP342X(address=self.ADDRESS)
        self.fill_adc_field()
        self.fill_min_max_adc()

        logging.debug(msg=f'Started vane on port "{self.ADDRESS}" in the sensor "{self.__class__.__name__}".')

    def fill_adc_field(self):
        for item in self.VANE_ANGLES_AND_DIRECTIONS_TABLE:
            voltage_out = self.calculate_voltage_out(r2=item['ohms'])
            item['adc'] = round(self.adc.max * (voltage_out / self.adc.vref))

    def calculate_voltage_out(self, r2):
        return (float(r2) / float(self.VOLTAGE_DIVIDER + r2)) * float(self.VOLTAGE_IN)

    def fill_min_max_adc(self):
        sorted_by_adc = sorted(self.VANE_ANGLES_AND_DIRECTIONS_TABLE, key=lambda x: x['adc'])
        last_index = len(sorted_by_adc) - 1

        for index, item in enumerate(sorted_by_adc):
            if index > 0:
                below = sorted_by_adc[index - 1]
                delta = (item['adc'] - below['adc']) / 2.0
                item['adc_min'] = item['adc'] - delta + 1
            else:
                item['adc_min'] = 1

            if index < last_index:
                above = sorted_by_adc[index + 1]
                delta = (above['adc'] - item['adc']) / 2.0
                item['adc_max'] = item['adc'] + delta
            else:
                item['adc_max'] = self.adc.max - 1

    def get_wind_direction_angle(self):
        adc_value = self.adc.read(self.ADC_CHANNEL)
        direction = self.get_direction_angle_by_adc(adc_value=adc_value)

        if direction is None:
            raise Exception(f'Cannot determine wind direction for ADC reading "{adc_value}".')

        return direction

    def get_direction_angle_by_adc(self, adc_value):
        for direction in self.VANE_ANGLES_AND_DIRECTIONS_TABLE:
            if 0 < adc_value <= direction['adc_max'] and direction['adc_min'] <= adc_value < self.adc.max:
                return direction['angle']

        return None

    def get_direction_average(self, direction_angles):
        direction_angles_average = self.get_angles_average(angles=direction_angles)
        return self.get_direction_by_direction_angle(direction_angle=direction_angles_average)

    @staticmethod
    def get_angles_average(angles):
        sin_sum = 0.0
        cos_sum = 0.0

        for angles in angles:
            r = math.radians(angles)
            sin_sum += math.sin(r)
            cos_sum += math.cos(r)

        float_length = float(len(angles))
        s = sin_sum / float_length
        c = cos_sum / float_length
        arc = math.degrees(math.atan(s / c))
        average = 0.0

        if s > 0 and c > 0:
            average = arc
        elif c < 0:
            average = arc + 180
        elif s < 0 and c > 0:
            average = arc + 360

        return 0.0 if average == 360 else average

    def get_direction_by_direction_angle(self, direction_angle):
        for item in self.VANE_ANGLES_AND_DIRECTIONS_TABLE:
            if item['angle'] == direction_angle:
                return item['direction']

        raise Exception(f'Cannot identify wind direction by the value "{direction_angle}".')
