import sys
import unittest
from random import random
from unittest import mock
from unittest.mock import MagicMock

sys.modules['MCP342X'] = MagicMock()
from sensors.vane import Vane


class TestVane(unittest.TestCase):
    @mock.patch('sensors.vane.MCP342X')
    @mock.patch('sensors.vane.Vane.fill_adc_field')
    @mock.patch('sensors.vane.Vane.fill_min_max_adc')
    def setUp(self, mock_fill_min_max_adc, mock_fill_adc_field, mock_mcp):
        self.test_vane = Vane()

        mock_adc = MagicMock()
        mock_adc.max = 1
        mock_adc.vref = 1
        mock_adc.read.return_value = 1

        self.test_vane.adc = mock_adc

    @mock.patch('sensors.vane.MCP342X')
    @mock.patch('sensors.vane.Vane.fill_adc_field')
    @mock.patch('sensors.vane.Vane.fill_min_max_adc')
    @mock.patch('sensors.vane.logging')
    def test_when_calling_constructor_expected_values_should_be_returned(self,
                                                                         mock_logging,
                                                                         mock_fill_min_max_adc,
                                                                         mock_fill_adc_field,
                                                                         mock_mcp):
        # act
        self.assertIsNotNone(Vane())

        # assert
        mock_fill_min_max_adc.assert_called_once()
        mock_fill_adc_field.assert_called_once()
        mock_mcp.assert_called_once()
        mock_logging.debug.assert_called_once_with(msg=f'Started vane on port "{self.test_vane.ADDRESS}"'
                                                       f' in the sensor "{self.test_vane.__class__.__name__}".')

    def test_when_filling_adc_fields_expected_values_should_be_returned(self):
        # arrange
        self.test_vane.calculate_voltage_out = MagicMock(return_value=1)

        # act
        self.assertIsNone(self.test_vane.fill_adc_field())

        # assert
        for item in self.test_vane.VANE_ANGLES_AND_DIRECTIONS_TABLE:
            self.test_vane.calculate_voltage_out.assert_any_call(r2=item['ohms'])
            self.assertEqual(item['adc'], 1)

    def test_when_calculating_voltage_out_expected_values_should_be_returned(self):
        # arrange
        test_values_and_results = {0: 0,
                                   10: 4.356752433008932e-4,
                                   525: 0.0227169811320755}

        # act
        for r in test_values_and_results:
            self.assertAlmostEqual(first=self.test_vane.calculate_voltage_out(r2=r),
                                   second=test_values_and_results[r],
                                   delta=0.0000000000000001)

    def test_when_filling_min_max_adc_expected_fields_should_be_filled(self):
        # arrange
        for item in self.test_vane.VANE_ANGLES_AND_DIRECTIONS_TABLE:
            item['adc'] = random()

        # act
        self.assertIsNone(self.test_vane.fill_min_max_adc())

        for item in self.test_vane.VANE_ANGLES_AND_DIRECTIONS_TABLE:
            self.assertIsNotNone(item['adc_min'])
            self.assertIsNotNone(item['adc_max'])

    def test_when_getting_wind_direction_angle_given_no_direction_exception_should_be_thrown(self):
        # arrange
        self.test_vane.get_direction_angle_by_adc = MagicMock(return_value=None)

        # act
        with self.assertRaises(Exception):
            self.test_vane.get_wind_direction_angle()

        # assert
        self.test_vane.adc.read.assert_called_once_with(self.test_vane.ADC_CHANNEL)
        self.test_vane.get_direction_angle_by_adc.assert_called_once_with(adc_value=self.test_vane.adc.read())

    def test_when_getting_wind_direction_angle_given_direction_it_should_be_returned(self):
        # arrange
        test_result = 5
        self.test_vane.get_direction_angle_by_adc = MagicMock(return_value=test_result)

        # act
        self.assertIsNotNone(self.test_vane.get_wind_direction_angle())

        # assert
        self.test_vane.adc.read.assert_called_once_with(self.test_vane.ADC_CHANNEL)
        self.test_vane.get_direction_angle_by_adc.assert_called_once_with(adc_value=self.test_vane.adc.read())

    def test_when_getting_direction_angle_by_adc_given_value_expected_angle_should_be_returned(self):
        # arrange
        self.test_vane.VANE_ANGLES_AND_DIRECTIONS_TABLE[1]['adc_min'] = 0.1
        self.test_vane.VANE_ANGLES_AND_DIRECTIONS_TABLE[1]['adc_max'] = 0.9

        # act
        self.assertEqual(self.test_vane.get_direction_angle_by_adc(adc_value=0.5),
                         self.test_vane.VANE_ANGLES_AND_DIRECTIONS_TABLE[1]['angle'])

    def test_when_getting_direction_angle_by_adc_given_wrong_values_none_should_be_returned(self):
        # arrange
        self.test_vane.VANE_ANGLES_AND_DIRECTIONS_TABLE[1]['adc_min'] = 0.1
        self.test_vane.VANE_ANGLES_AND_DIRECTIONS_TABLE[1]['adc_max'] = 0.9

        # act
        self.assertIsNone(self.test_vane.get_direction_angle_by_adc(adc_value=0))
        self.assertIsNone(self.test_vane.get_direction_angle_by_adc(adc_value=0.05))
        self.assertIsNone(self.test_vane.get_direction_angle_by_adc(adc_value=1))

    def test_when_getting_direction_average_given_angle_expected_value_should_be_returned(self):
        # arrange
        test_direction_angles = [1, 2]
        test_angle_average = 1
        test_direction = 2
        self.test_vane.get_angles_average = MagicMock(return_value=test_angle_average)
        self.test_vane.get_direction_by_direction_angle = MagicMock(return_value=test_direction)

        # act
        self.assertEqual(self.test_vane.get_direction_average(direction_angles=test_direction_angles),
                         test_direction)

        # assert
        self.test_vane.get_angles_average.assert_called_once_with(angles=test_direction_angles)
        self.test_vane.get_direction_by_direction_angle.assert_called_once_with(direction_angle=test_angle_average)

    def test_when_getting_angles_average_given_no_angles_0_should_be_returned(self):
        self.assertEqual(self.test_vane.get_angles_average(angles=[]), 0.0)
        self.assertEqual(self.test_vane.get_angles_average(angles=None), 0.0)

    def test_when_getting_angles_average_given_no_angles_0_should_be_returned(self):
        # arrange
        test_angles = {(0.0, 180.0): 0,
                       (45.0, 90.0): 67.5,
                       (225.0, 270.0): 247.5,
                       (337.5, 22.5): 6.88e-15,
                       (135.0, 202.5): 168.75}

        # act & assert
        for angles in test_angles:
            self.assertAlmostEqual(first=self.test_vane.get_angles_average(angles=angles),
                                   second=test_angles[angles],
                                   delta=0.1)

    def test_when_getting_directions_by_direction_angle_expected_value_should_be_returned(self):
        test_direction_angles = {0.0: 'N',
                                 45.0: 'N-E',
                                 170.7: 'S-SE',
                                 320: 'N-W',
                                 360: None}

        # act & assert
        for direction_angle in test_direction_angles:
            self.assertEqual(self.test_vane.get_direction_by_direction_angle(direction_angle=direction_angle),
                             test_direction_angles[direction_angle])


if __name__ == '__main__':
    unittest.main()
