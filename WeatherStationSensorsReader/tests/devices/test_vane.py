import unittest
from unittest import mock
from unittest.mock import MagicMock

from devices.vane import Vane


class TestVane(unittest.TestCase):
    @mock.patch('devices.vane.MCP3008')
    def setUp(self, mock_mcp):
        self.test_vane = Vane()

    @mock.patch('devices.vane.MCP3008')
    @mock.patch('devices.vane.logging')
    def test_when_calling_constructor_expected_values_should_be_returned(self, mock_logging, mock_mcp):
        # act
        self.assertIsNotNone(Vane())

        # assert
        mock_mcp.assert_called_once_with(channel=self.test_vane.CHANNEL)
        mock_logging.debug.assert_called_once_with(msg=f'[Vane] Started on the channel "{self.test_vane.CHANNEL}".')

    @mock.patch('devices.vane.logging')
    def test_when_getting_reading_given_wrong_voltage_null_should_be_returned(self, mock_logging):
        # arrange
        test_value = 50
        test_gpio_value = round(test_value * self.test_vane.VOLTAGE_IN, 1)

        mcp_mock = MagicMock()
        mcp_mock.value = test_value
        self.test_vane.mcp_chip = mcp_mock

        # act
        self.assertIsNone(self.test_vane.get_reading())

        # assert
        mock_logging.debug.assert_any_call(msg=f'[Vane] MCP reading "{test_value}", GPIO value "{test_gpio_value}".')
        mock_logging.warning.assert_any_call(msg=f'[Vane] Cannot determine wind direction for MCP reading "{test_value}" and GPIO value "{test_gpio_value}".')

    @mock.patch('devices.vane.logging')
    def test_when_getting_reading_given_correct_voltage_expected_angle_should_be_returned(self, mock_logging):
        # arrange
        test_value = 0.87878787878787
        test_gpio_value = round(test_value * self.test_vane.VOLTAGE_IN, 1)
        test_expected_value = 112.5

        mcp_mock = MagicMock()
        mcp_mock.value = test_value
        self.test_vane.mcp_chip = mcp_mock

        # act
        self.assertEqual(self.test_vane.get_reading(), test_expected_value)

        # assert
        mock_logging.debug.assert_called_once_with(msg=f'[Vane] MCP reading "{test_value}", GPIO value "{test_gpio_value}".')
        mock_logging.warning.assert_not_called()

    def test_when_getting_direction_average_given_angle_expected_value_should_be_returned(self):
        # arrange
        test_direction_angles = [1, 2]
        test_angle_average = 1
        test_direction = 2
        self.test_vane.get_angles_average = MagicMock(return_value=test_angle_average)
        self.test_vane.get_direction_by_angle = MagicMock(return_value=test_direction)

        # act
        self.assertEqual(self.test_vane.get_direction_average(angles=test_direction_angles),
                         test_direction)

        # assert
        self.test_vane.get_angles_average.assert_called_once_with(angles=test_direction_angles)
        self.test_vane.get_direction_by_angle.assert_called_once_with(angle=test_angle_average)

    def test_when_getting_angles_average_given_no_angles_unknown_should_be_returned(self):
        self.assertIsNone(self.test_vane.get_angles_average(angles=[]))
        self.assertIsNone(self.test_vane.get_angles_average(angles=[None, None]))

    def test_when_getting_angles_average_given_angles_expected_values_should_be_returned(self):
        # arrange
        test_angles = {(0.0, 180.0): 0,
                       (45.0, 90.0): 67.5,
                       (225.0, 270.0): 247.5,
                       (337.5, 22.5): 6.88e-15,
                       (135.0, 202.5): 168.75,
                       (135.0, None, None, None, 202.5): 168.75}

        # act & assert
        for angles in test_angles:
            self.assertAlmostEqual(first=self.test_vane.get_angles_average(angles=angles),
                                   second=test_angles[angles],
                                   delta=0.1)

    def test_when_getting_directions_by_direction_angle_expected_value_should_be_returned(self):
        test_direction_angles = {None: self.test_vane.UNKNOWN_WIND_DIRECTION,
                                 0.0: 'N',
                                 45.0: 'N-E',
                                 170.7: 'S-SE',
                                 320: 'N-W',
                                 360: self.test_vane.UNKNOWN_WIND_DIRECTION}

        # act & assert
        for direction_angle in test_direction_angles:
            self.assertEqual(self.test_vane.get_direction_by_angle(angle=direction_angle),
                             test_direction_angles[direction_angle])


if __name__ == '__main__':
    unittest.main()
