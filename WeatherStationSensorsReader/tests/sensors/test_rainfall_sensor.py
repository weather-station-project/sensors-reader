import unittest
from unittest import mock

from sensors.rainfall_sensor import RainfallSensor


class TestRainfallSensor(unittest.TestCase):
    @mock.patch('sensors.rainfall_sensor.Sensor.__init__')
    @mock.patch('sensors.rainfall_sensor.logging')
    @mock.patch('sensors.rainfall_sensor.Button')
    def setUp(self, mock_button, mock_logging, mock_super):
        test_rain_gauge_port_number = 51

        self.test_sensor = RainfallSensor(rain_gauge_port_number=test_rain_gauge_port_number)

        self.assertIsNotNone(self.test_sensor)
        mock_button.assert_called_once()
        mock_logging.debug.assert_called_once_with(msg=f'[RainfallSensor] Started on the port "{test_rain_gauge_port_number}".')
        mock_super.assert_called_once()

    def test_when_adding_values_nothing_should_be_returned(self):
        self.assertIsNone(self.test_sensor.add_value_to_readings())

    @mock.patch('sensors.rainfall_sensor.logging')
    def test_when_getting_readings_1_should_be_returned(self, mock_logging):
        self.assertEqual(self.test_sensor.get_reading(), [1])
        mock_logging.debug.assert_called_once_with(msg='[RainfallSensor] Pressed.')

    def test_when_getting_averages_given_1_reading_expected_result_should_be_returned(self):
        self.test_sensor.readings = [1]

        self.assertEqual(self.test_sensor.get_average(), self.test_sensor.BUCKET_SIZE_IN_MM)


if __name__ == '__main__':
    unittest.main()
