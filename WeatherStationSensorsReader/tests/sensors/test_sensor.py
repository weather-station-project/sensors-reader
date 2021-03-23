import unittest
from unittest import mock
from unittest.mock import MagicMock

from exceptions.sensor_exception import SensorException
from sensors.sensor import Sensor


class TestSensor(unittest.TestCase):
    @mock.patch('sensors.sensor.Thread')
    def setUp(self, mock_thread):
        Sensor.__abstractmethods__ = set()

        self.test_sensor = Sensor()

        self.assertIsNotNone(self.test_sensor)
        mock_thread.assert_called_once_with(target=self.test_sensor.add_value_to_readings)

    @mock.patch('sensors.sensor.sleep')
    @mock.patch('sensors.sensor.logging')
    def test_when_adding_value_to_readings_expected_actions_should_be_performed(self, mock_logging, mock_sleep):
        # arrange
        test_value = 20

        self.test_sensor.get_reading = MagicMock(return_value=test_value)
        self.test_sensor.get_true = MagicMock(side_effect=[True, False])

        # act
        self.assertIsNone(self.test_sensor.add_value_to_readings())

        # assert
        self.assertEqual(self.test_sensor.readings, [test_value])

        mock_logging.debug.assert_called_once_with(msg=f'Obtained "{test_value}" from "{self.test_sensor.__class__.__name__}".')
        mock_logging.exception.assert_not_called()
        mock_sleep.assert_called_once_with(self.test_sensor.SECONDS_BETWEEN_READINGS)

    @mock.patch('sensors.sensor.sleep')
    @mock.patch('sensors.sensor.logging')
    def test_when_adding_value_to_readings_given_getting_readings_true_expected_actions_should_be_performed(self, mock_logging, mock_sleep):
        # arrange
        self.test_sensor.get_reading = MagicMock()
        self.test_sensor.get_true = MagicMock(side_effect=[True, False])
        self.test_sensor.getting_readings = True

        # act
        self.assertIsNone(self.test_sensor.add_value_to_readings())

        # assert
        self.assertEqual(len(self.test_sensor.readings), 0)

        mock_logging.debug.assert_not_called()
        mock_logging.exception.assert_not_called()
        mock_sleep.assert_called_once_with(self.test_sensor.SECONDS_BETWEEN_READINGS)

    @mock.patch('sensors.sensor.sleep')
    @mock.patch('sensors.sensor.logging')
    def test_when_adding_value_to_readings_given_error_expected_actions_should_be_performed(self, mock_logging, mock_sleep):
        # arrange
        self.test_sensor.get_reading = MagicMock(side_effect=Exception())
        self.test_sensor.get_true = MagicMock(side_effect=[True, False])

        # act
        self.assertIsNone(self.test_sensor.add_value_to_readings())

        # assert
        self.assertEqual(len(self.test_sensor.readings), 0)

        mock_logging.debug.assert_not_called()
        mock_logging.exception.assert_called_once_with(f'Error while reading from sensor "{self.test_sensor.__class__.__name__}".')
        mock_sleep.assert_called_once_with(self.test_sensor.SECONDS_BETWEEN_READINGS)

    def test_when_getting_true_true_value_should_be_returned(self):
        self.assertTrue(self.test_sensor.get_true())

    def test_when_calling_get_reading_method_error_should_be_thrown(self):
        with self.assertRaises(NotImplementedError):
            self.test_sensor.get_reading()

    @mock.patch('sensors.sensor.register_success_for_class_into_health_check_file')
    def test_when_getting_average_given_values_expected_average_should_be_returned(self, mock_register):
        # arrange
        test_expected_averages = [40]
        self.test_sensor.get_average = MagicMock(return_value=test_expected_averages)
        self.test_sensor.readings = [1, None, None, 2]

        # act
        self.assertEqual(test_expected_averages, self.test_sensor.get_readings_average())

        # assert
        self.assertEqual(len(self.test_sensor.readings), 0)
        self.test_sensor.get_average.assert_called_once()
        mock_register.assert_called_once_with(class_name='Sensor')

    @mock.patch('sensors.sensor.register_success_for_class_into_health_check_file')
    def test_when_getting_average_given_all_readings_null_expected_exception_should_be_thrown(self, mock_register):
        # arrange
        self.test_sensor.get_average = MagicMock()
        self.test_sensor.readings = [None, None]

        # act
        with self.assertRaises(SensorException):
            self.test_sensor.get_readings_average()

        # assert
        self.assertEqual(len(self.test_sensor.readings), 0)
        self.test_sensor.get_average.assert_not_called()
        mock_register.assert_not_called()

    @mock.patch('sensors.sensor.register_success_for_class_into_health_check_file')
    def test_when_getting_average_given_no_readings_expected_exception_should_be_thrown(self, mock_register):
        # arrange
        self.test_sensor.get_average = MagicMock()
        self.test_sensor.readings = []

        # act
        with self.assertRaises(SensorException):
            self.test_sensor.get_readings_average()

        # assert
        self.assertEqual(len(self.test_sensor.readings), 0)
        self.test_sensor.get_average.assert_not_called()
        mock_register.assert_not_called()

    @mock.patch('sensors.sensor.register_success_for_class_into_health_check_file')
    def test_when_getting_average_given_no_readings_null_expected_exception_should_be_thrown(self, mock_register):
        # arrange
        self.test_sensor.get_average = MagicMock()

        # act
        with self.assertRaises(SensorException):
            self.test_sensor.get_readings_average()

        # assert
        self.assertEqual(len(self.test_sensor.readings), 0)
        self.test_sensor.get_average.assert_not_called()
        mock_register.assert_not_called()

    def test_when_getting_averages_expected_values_should_be_returned(self):
        # arrange
        self.test_sensor.readings = [[10, 55, 10, 1],
                                     [70, 2, 3, 1],
                                     [5, 35, 5, 1],
                                     [5, 96, 97, 1],
                                     [10, 35, 5, 1]]
        test_expected_averages = [20, 44.6, 24, 1]

        # act
        result = self.test_sensor.get_average()

        # assert
        for i in range(len(test_expected_averages)):
            self.assertEqual(test_expected_averages[i], result[i])


if __name__ == '__main__':
    unittest.main()
