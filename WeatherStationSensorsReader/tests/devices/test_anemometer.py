import time
import unittest
from unittest import mock
from unittest.mock import MagicMock, Mock

from devices.anemometer import Anemometer


class TestAnemometer(unittest.TestCase):
    test_port_number = 55

    @mock.patch('devices.anemometer.Button')
    def setUp(self, mock_button):
        self.test_anemometer = Anemometer(anemometer_port_number=self.test_port_number)

    @mock.patch('devices.anemometer.Button')
    @mock.patch('devices.anemometer.logging')
    def test_when_calling_constructor_new_mock_should_be_initialized(self, mock_logging, mock_button):
        self.assertIsNotNone(Anemometer(anemometer_port_number=self.test_port_number))

        mock_logging.debug.assert_called_once_with(msg=f'Started anemometer on the port "{self.test_port_number}".')

        mock_button.assert_called_once_with(pin=self.test_port_number)

    @mock.patch('devices.anemometer.logging')
    def test_when_spinning_count_should_be_incremented_and_logged(self, mock_logging):
        current_signals_count = self.test_anemometer.spin_count

        self.assertIsNone(self.test_anemometer.spin())

        self.assertEqual(self.test_anemometer.spin_count, current_signals_count + 1)
        mock_logging.debug.assert_called_once_with(msg=f'Spin count {self.test_anemometer.spin_count}.')

    @mock.patch('devices.anemometer.time')
    def test_when_getting_speed_expected_calls_should_be_done(self, mock_time):
        # arrange
        test_speed = 50
        self.test_anemometer.calculate_speed = Mock(return_value=test_speed)

        # act
        self.assertEqual(self.test_anemometer.get_speed(), test_speed)

        # assert
        mock_time.time.assert_any_call()
        self.test_anemometer.calculate_speed.assert_called_once()

    def test_when_getting_speed_expected_result_should_be_returned(self):
        self.assertAlmostEqual(first=self.test_anemometer.calculate_speed(current_spin_count=2, elapsed_seconds=1),
                               second=2.4,
                               delta=0.1)
        self.assertAlmostEqual(first=self.test_anemometer.calculate_speed(current_spin_count=80, elapsed_seconds=1),
                               second=96,
                               delta=0.1)


if __name__ == '__main__':
    unittest.main()
