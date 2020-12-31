import time
import unittest
from statistics import mean
from unittest import mock
from unittest.mock import Mock, MagicMock

from sensors.wind_measurement_sensor import WindMeasurementSensor


class TestWindMeasurementSensor(unittest.TestCase):
    def setUp(self):
        self.test_sensor = WindMeasurementSensor()

    @mock.patch('sensors.wind_measurement_sensor.logging')
    def test_when_calling_constructor_new_mock_should_be_initialized(self, mock_logging):
        self.assertIsNotNone(WindMeasurementSensor())

        mock_logging.debug.assert_called_once_with(msg=f'Started anemometer on port "{self.test_sensor.GPIO_PORT_NUMBER}"'
                                                       f' in the sensor "{self.test_sensor.__class__.__name__}".')

    def test_when_reading_values_given_some_samples_expected_values_should_be_returned(self):
        # arrange
        test_values = [10, 20, 40, 30]
        self.test_sensor.get_samples = Mock(return_value=test_values)

        # act
        self.assertEqual(self.test_sensor.read_values(), [-1, mean(data=test_values), max(test_values)])

        # assert
        self.test_sensor.get_samples.assert_called_once()

    @mock.patch('sensors.wind_measurement_sensor.Button')
    @mock.patch('sensors.wind_measurement_sensor.logging')
    def test_when_getting_samples_expected_methods_should_be_called_and_expected_values_returned(self, mock_logging, mock_button):
        # arrange
        test_samples = [10, 20, 30, 40, 50]
        self.test_sensor.get_sample_speed = MagicMock(side_effect=test_samples)

        # act
        self.assertEqual(self.test_sensor.get_samples(), test_samples)

        # assert
        mock_button.assert_called_once_with(pin=self.test_sensor.GPIO_PORT_NUMBER)
        self.test_sensor.get_sample_speed.assert_called()
        for n in range(0, self.test_sensor.SAMPLES_COUNT):
            mock_logging.debug.assert_any_call(msg=f'Sample speed obtained "{test_samples[n]}" km/h. Attempt {n + 1}.')

    @mock.patch('sensors.wind_measurement_sensor.logging')
    def test_when_spinning_count_should_be_incremented_and_logged(self, mock_logging):
        current_signals_count = self.test_sensor.signals_count

        self.assertIsNone(self.test_sensor.spin())

        self.assertEqual(self.test_sensor.signals_count, current_signals_count + 1)
        mock_logging.debug.assert_called_once_with(msg=f'Signals count {self.test_sensor.signals_count}.')

    @mock.patch('sensors.wind_measurement_sensor.time', autospec=True)
    def test_when_getting_sample_speed_expected_calls_should_be_done(self, mock_time):
        # arrange
        test_start_time = time.time()
        test_finish_time = time.time()
        mock_time.time = MagicMock(side_effect=[test_start_time, test_finish_time])

        test_speed = 50
        self.test_sensor.get_speed = Mock(return_value=test_speed)

        # act
        self.assertEqual(self.test_sensor.get_sample_speed(), test_speed)

        # assert
        mock_time.time.assert_any_call()
        mock_time.sleep.assert_called_once_with(self.test_sensor.SECONDS_BETWEEN_SAMPLES)
        self.test_sensor.get_speed.assert_called_once_with(current_signals_count=0, elapsed_seconds=test_finish_time - test_start_time)

    def test_when_getting_speed_expected_result_should_be_returned(self):
        self.assertAlmostEqual(first=self.test_sensor.get_speed(current_signals_count=2, elapsed_seconds=1),
                               second=2.4,
                               delta=0.1)


if __name__ == '__main__':
    unittest.main()
