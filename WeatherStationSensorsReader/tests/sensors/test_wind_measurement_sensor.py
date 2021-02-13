import unittest
from unittest import mock
from unittest.mock import Mock

from sensors.wind_measurement_sensor import WindMeasurementSensor


class TestWindMeasurementSensor(unittest.TestCase):
    test_port_number = 55

    @mock.patch('sensors.wind_measurement_sensor.Anemometer')
    @mock.patch('sensors.wind_measurement_sensor.Vane')
    def test_when_calling_constructor_new_mock_should_be_initialized(self, mock_vane, mock_anemometer):
        self.assertIsNotNone(WindMeasurementSensor(anemometer_port_number=self.test_port_number))

        mock_anemometer.assert_called_once_with(anemometer_port_number=self.test_port_number)
        mock_vane.assert_called_once()

    @mock.patch('sensors.wind_measurement_sensor.Anemometer')
    @mock.patch('sensors.wind_measurement_sensor.Vane')
    def test_when_reading_values_given_some_samples_expected_values_should_be_returned(self, mock_vane, mock_anemometer):
        # arrange
        test_sample = 10
        test_direction_angle = 100

        mock_sensor = Mock()
        mock_sensor.get_sample.return_value = test_sample
        mock_anemometer.return_value = mock_sensor

        mock_sensor = Mock()
        mock_sensor.get_sample.return_value = test_direction_angle
        mock_vane.return_value = mock_sensor

        mock_anemometer.get_samples.return_value = test_sample
        mock_vane.get_wind_direction_angle.return_value = test_direction_angle

        # act
        sensor = WindMeasurementSensor(anemometer_port_number=self.test_port_number)
        self.assertEqual(sensor.read_values(), [test_direction_angle, test_sample])

        # assert
        mock_anemometer.assert_called_once_with(anemometer_port_number=self.test_port_number)
        mock_vane.assert_called_once()


if __name__ == '__main__':
    unittest.main()
