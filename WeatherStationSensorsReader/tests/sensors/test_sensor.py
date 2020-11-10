import unittest
from unittest import mock
from unittest.mock import MagicMock

from sensors.sensor import Sensor


class TestSensor(unittest.TestCase):
    @mock.patch('sensors.sensor.sleep', autospec=True)
    @mock.patch('sensors.sensor.logging', autospec=True)
    def test_when_getting_averages_expected_averages_should_be_returned(self, mock_logging, mock_sleep):
        # arrange
        test_values = [[10, 70, 10],
                       [15, 2, 3, 0],
                       [80, 35, 5],
                       [10, 1, 1]]
        test_expected_averages = [30, 5, 40, 4]
        sensor = Sensor()
        sensor._read_values = MagicMock(side_effect=test_values)

        # act
        result = sensor.get_read_averages()

        # assert
        for i in range(len(test_expected_averages)):
            self.assertEqual(test_expected_averages[i], result[i])

        for n in range(1, sensor.NUMBER_OF_READS):
            mock_logging.debug.assert_any_call(msg=f'Obtained "{test_values[n - 1]}" from the sensor "{sensor.__class__.__name__}". Attempt {n}.')
            mock_sleep.assert_any_call(sensor.SECONDS_BETWEEN_READS)

        mock_logging.error.assert_not_called()
        mock_logging.debug.assert_called_with(msg=f'Average "{test_expected_averages}" from the sensor "{sensor.__class__.__name__}".')

    @mock.patch('sensors.sensor.sleep', autospec=True)
    @mock.patch('sensors.sensor.logging', autospec=True)
    def test_when_getting_averages_given_failures_expected_errors_should_be_logged_but_not_raised(self, mock_logging, mock_sleep):
        # arrange
        sensor = Sensor()
        sensor._read_values = MagicMock(side_effect=Exception('test'))

        # act
        result = sensor.get_read_averages()

        # assert
        self.assertEqual(len(result), 0)

        for n in range(1, sensor.NUMBER_OF_READS):
            mock_logging.error.assert_any_call(f'Error while reading from sensor "{sensor.__class__.__name__}". Attempt {n}. ',
                                               sensor._read_values.side_effect)
            mock_sleep.assert_any_call(sensor.SECONDS_BETWEEN_READS)

        mock_logging.debug.assert_called_with(msg=f'Average "[]" from the sensor "{sensor.__class__.__name__}".')

    def test_when_calling_read_values_method_error_should_be_thrown(self):
        sensor = Sensor()

        with self.assertRaises(NotImplementedError):
            sensor._read_values()


if __name__ == '__main__':
    unittest.main()
