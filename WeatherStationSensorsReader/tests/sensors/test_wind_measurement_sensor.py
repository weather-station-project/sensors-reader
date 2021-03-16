import unittest
from unittest import mock
from unittest.mock import Mock, MagicMock

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

        mock_anemometer_device = Mock()
        mock_anemometer_device.get_sample.return_value = test_sample
        mock_anemometer.return_value = mock_anemometer_device

        mock_vane_device = Mock()
        mock_vane_device.get_sample.return_value = test_direction_angle
        mock_vane.return_value = mock_vane_device

        # act
        sensor = WindMeasurementSensor(anemometer_port_number=self.test_port_number)
        self.assertEqual(sensor.read_values(), [test_direction_angle, test_sample])

        # assert
        mock_anemometer.assert_called_once_with(anemometer_port_number=self.test_port_number)
        mock_vane.assert_called_once()
        mock_anemometer_device.get_sample.assert_called_once()
        mock_vane_device.get_sample.assert_called_once()

    @mock.patch('sensors.wind_measurement_sensor.Anemometer')
    @mock.patch('sensors.wind_measurement_sensor.Vane')
    def test_when_getting_averages_expected_calls_should_be_done_and_expected_values_returned(self, mock_vane, mock_anemometer):
        # arrange
        test_reads = [[10, 1],
                      [15, 5],
                      [15, 2],
                      [30, 1],
                      [30, 1]]
        test_direction_average = 'N-NW'
        test_expected_values = [test_direction_average, 2, 5]

        mock_vane.return_value.get_direction_average = MagicMock(return_value=test_direction_average)

        # act
        sensor = WindMeasurementSensor(anemometer_port_number=self.test_port_number)
        self.assertEqual(sensor.get_average(reads=test_reads), test_expected_values)

        # arrange
        mock_vane.return_value.get_direction_average.assert_called_once_with(direction_angles=(10, 15, 15, 30, 30))


if __name__ == '__main__':
    unittest.main()
