import unittest
from unittest import mock
from unittest.mock import Mock, MagicMock

from sensors.wind_measurement_sensor import WindMeasurementSensor


class TestWindMeasurementSensor(unittest.TestCase):
    test_port_number = 55

    @mock.patch('sensors.wind_measurement_sensor.Sensor.__init__')
    @mock.patch('sensors.wind_measurement_sensor.Anemometer')
    @mock.patch('sensors.wind_measurement_sensor.Vane')
    def setUp(self, mock_vane, mock_anemometer, mock_super):
        mock_vane_device = Mock()
        mock_vane.return_value = mock_vane_device

        self.test_sensor = WindMeasurementSensor(anemometer_port_number=self.test_port_number)

        mock_anemometer.assert_called_once_with(anemometer_port_number=self.test_port_number)
        mock_vane.assert_called_once()
        mock_super.assert_called_once()

    def test_when_getting_readings_given_some_samples_expected_values_should_be_returned(self):
        # arrange
        test_direction_angle = 100
        self.test_sensor.vane.get_reading.return_value = test_direction_angle

        # act
        self.assertEqual(self.test_sensor.get_reading(), test_direction_angle)

    def test_when_getting_averages_expected_calls_should_be_done_and_expected_values_returned(self):
        # arrange
        test_speed = 58
        test_direction_average = 'N-NW'

        self.test_sensor.vane.get_direction_average = MagicMock(return_value=test_direction_average)
        self.test_sensor.anemometer.get_speed = MagicMock(return_value=test_speed)

        # act
        self.test_sensor.readings = [10, 15, 15, 30, 30]
        self.assertEqual(self.test_sensor.get_average(), [test_direction_average, test_speed])

        # assert
        self.test_sensor.vane.get_direction_average.assert_called_once_with(angles=self.test_sensor.readings)
        self.test_sensor.anemometer.get_speed.assert_called_once()


if __name__ == '__main__':
    unittest.main()
