import time
import unittest
from unittest import mock
from unittest.mock import MagicMock, Mock

from sensors.anemometer import Anemometer


class TestAnemometer(unittest.TestCase):
    test_port_number = 55

    def setUp(self):
        self.test_anemometer = Anemometer(anemometer_port_number=self.test_port_number)

    @mock.patch('sensors.anemometer.logging')
    def test_when_calling_constructor_new_mock_should_be_initialized(self, mock_logging):
        self.assertIsNotNone(Anemometer(anemometer_port_number=self.test_port_number))

        mock_logging.debug.assert_called_once_with(msg=f'Started anemometer on port "{self.test_anemometer.anemometer_port_number}"'
                                                       f' in the sensor "{self.test_anemometer.__class__.__name__}".')

    @mock.patch('sensors.anemometer.Button')
    @mock.patch('sensors.anemometer.logging')
    def test_when_getting_samples_expected_methods_should_be_called_and_expected_values_returned(self, mock_logging, mock_button):
        # arrange
        test_samples = [10, 20, 30]
        self.test_anemometer.get_speed_sample = MagicMock(side_effect=test_samples)

        # act
        self.assertEqual(self.test_anemometer.get_wind_speed_samples(), test_samples)

        # assert
        mock_button.assert_called_once_with(pin=self.test_anemometer.anemometer_port_number)
        self.test_anemometer.get_speed_sample.assert_called()
        for n in range(0, self.test_anemometer.SAMPLES_COUNT):
            mock_logging.debug.assert_any_call(msg=f'Speed sample obtained "{test_samples[n]}" km/h. Attempt {n + 1}.')

    @mock.patch('sensors.anemometer.logging')
    def test_when_spinning_count_should_be_incremented_and_logged(self, mock_logging):
        current_signals_count = self.test_anemometer.signals_count

        self.assertIsNone(self.test_anemometer.spin())

        self.assertEqual(self.test_anemometer.signals_count, current_signals_count + 1)
        mock_logging.debug.assert_called_once_with(msg=f'Signals count {self.test_anemometer.signals_count}.')

    @mock.patch('sensors.anemometer.time', autospec=True)
    def test_when_getting_sample_speed_expected_calls_should_be_done(self, mock_time):
        # arrange
        test_start_time = time.time()
        test_finish_time = time.time()
        mock_time.time = MagicMock(side_effect=[test_start_time, test_finish_time])

        test_speed = 50
        self.test_anemometer.calculate_speed = Mock(return_value=test_speed)

        # act
        self.assertEqual(self.test_anemometer.get_speed_sample(), test_speed)

        # assert
        mock_time.time.assert_any_call()
        mock_time.sleep.assert_called_once_with(self.test_anemometer.SECONDS_BETWEEN_SAMPLES)
        self.test_anemometer.calculate_speed.assert_called_once_with(current_signals_count=0, elapsed_seconds=test_finish_time - test_start_time)

    def test_when_getting_speed_expected_result_should_be_returned(self):
        self.assertAlmostEqual(first=self.test_anemometer.calculate_speed(current_signals_count=2, elapsed_seconds=1),
                               second=2.4,
                               delta=0.1)
        self.assertAlmostEqual(first=self.test_anemometer.calculate_speed(current_signals_count=80, elapsed_seconds=1),
                               second=96,
                               delta=0.1)


if __name__ == '__main__':
    unittest.main()
