import unittest
from unittest import mock
from unittest.mock import MagicMock

from exceptions.sensor_exception import SensorException
from sensors.sensor import Sensor


class TestSensor(unittest.TestCase):
    def setUp(self):
        Sensor.__abstractmethods__ = set()
        self.sensor = Sensor()

    @mock.patch('sensors.sensor.sleep')
    @mock.patch('sensors.sensor.logging')
    @mock.patch('sensors.sensor.register_success_for_class_into_health_check_file')
    def test_when_getting_one_read_expected_averages_should_be_returned(self, mock_register, mock_logging, mock_sleep):
        # arrange
        test_values = [[10], [70], [5], [5], [10]]
        test_expected_averages = [20]
        self.sensor.read_values = MagicMock(side_effect=test_values)
        self.sensor.get_averages = MagicMock(return_value=test_expected_averages)

        # act
        result = self.sensor.get_read_averages()

        # assert
        self.assertEqual(test_expected_averages[0], result[0])

        for n in range(0, self.sensor.NUMBER_OF_READS):
            mock_logging.debug.assert_any_call(
                msg=f'Obtained "{test_values[n]}" from the sensor "{self.sensor.__class__.__name__}". Attempt {n + 1}.')
            mock_sleep.assert_any_call(self.sensor.SECONDS_BETWEEN_READS)

        mock_logging.exception.assert_not_called()
        self.sensor.get_averages.assert_called_once_with(reads=test_values)
        mock_logging.debug.assert_called_with(msg=f'Average "{test_expected_averages}" from the sensor "{self.sensor.__class__.__name__}".')
        mock_register.assert_called_once_with(class_name='Sensor')

    @mock.patch('sensors.sensor.sleep')
    @mock.patch('sensors.sensor.logging')
    @mock.patch('sensors.sensor.register_success_for_class_into_health_check_file')
    def test_when_getting_one_read_one_failure_expected_averages_should_be_returned(self, mock_register, mock_logging, mock_sleep):
        # arrange
        test_values = [[10], [70], [5], [5], Exception('test')]
        test_expected_averages = [40]
        self.sensor.read_values = MagicMock(side_effect=test_values)
        self.sensor.get_averages = MagicMock(return_value=test_expected_averages)

        # act
        result = self.sensor.get_read_averages()

        # assert
        self.assertEqual(test_expected_averages[0], result[0])

        for n in range(0, self.sensor.NUMBER_OF_READS - 1):
            mock_logging.debug.assert_any_call(
                msg=f'Obtained "{test_values[n]}" from the sensor "{self.sensor.__class__.__name__}". Attempt {n + 1}.')
            mock_sleep.assert_any_call(self.sensor.SECONDS_BETWEEN_READS)

        mock_logging.exception.assert_called_once_with(f'Error while reading from sensor "{self.sensor.__class__.__name__}". Attempt 5.')
        self.sensor.get_averages.assert_called_once_with(reads=test_values[0:4])
        mock_logging.debug.assert_called_with(msg=f'Average "{test_expected_averages}" from the sensor "{self.sensor.__class__.__name__}".')
        mock_register.assert_called_once_with(class_name='Sensor')

    @mock.patch('sensors.sensor.sleep')
    @mock.patch('sensors.sensor.logging')
    @mock.patch('sensors.sensor.register_success_for_class_into_health_check_file')
    def test_when_getting_averages_given_all_failures_expected_errors_should_be_thrown(self, mock_register, mock_logging, mock_sleep):
        # arrange
        self.sensor.read_values = MagicMock(side_effect=Exception('test'))

        # act
        with self.assertRaises(SensorException):
            self.sensor.get_read_averages()

        # assert
        for n in range(0, self.sensor.NUMBER_OF_READS):
            mock_logging.exception.assert_any_call(f'Error while reading from sensor "{self.sensor.__class__.__name__}". Attempt {n + 1}.')
            mock_sleep.assert_any_call(self.sensor.SECONDS_BETWEEN_READS)

        mock_logging.debug.assert_not_called()
        mock_register.assert_not_called()

    def test_when_calling_read_values_method_error_should_be_thrown(self):
        sensor = Sensor()

        with self.assertRaises(NotImplementedError):
            sensor.read_values()

    def test_when_getting_averages_expected_values_should_be_returned(self):
        # arrange
        test_values = [[10, 55, 10, 1],
                       [70, 2, 3, 1],
                       [5, 35, 5, 1],
                       [5, 96, 97, 1],
                       [10, 35, 5, 1]]
        test_expected_averages = [20, 44.6, 24, 1]

        # act
        result = self.sensor.get_averages(reads=test_values)

        # assert
        for i in range(len(test_expected_averages)):
            self.assertEqual(test_expected_averages[i], result[i])


if __name__ == '__main__':
    unittest.main()
