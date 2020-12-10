import sys
import unittest
from unittest import mock
from unittest.mock import MagicMock, Mock

sys.modules['bme280pi'] = MagicMock()
from sensors.air_measurement_sensor import AirMeasurementSensor


class TestAirMeasurementSensor(unittest.TestCase):
    @mock.patch('sensors.air_measurement_sensor.logging')
    @mock.patch('sensors.air_measurement_sensor.Bme280Sensor')
    def test_when_calling_constructor_new_mock_should_be_initialized(self, mock_sensor, mock_logging):
        test_chip_id = 'test_chip_id'
        test_chip_version = 'test_chip_version'

        mock_sensor.return_value.chip_id = test_chip_id
        mock_sensor.return_value.chip_version = test_chip_version
        self.assertIsNotNone(AirMeasurementSensor())

        mock_sensor.assert_called_once()
        mock_logging.debug.assert_called_once_with(msg=f'Started Bme280 with chip_id "{test_chip_id}" and '
                                                       f'chip_version "{test_chip_version}" in the sensor "{AirMeasurementSensor.__name__}".')

    @mock.patch('sensors.air_measurement_sensor.Bme280Sensor')
    def test_when_reading_values_expected_method_should_be_called(self, mock_bme280_sensor):
        test_pressure = 1024
        test_humidity = 67

        mock_sensor = Mock()
        mock_sensor.get_pressure.return_value = test_pressure
        mock_sensor.get_humidity.return_value = test_humidity
        mock_bme280_sensor.return_value = mock_sensor

        self.assertEqual(AirMeasurementSensor().read_values(), [test_pressure, test_humidity])

        mock_sensor.get_pressure.assert_called_once_with(unit='hPa')
        mock_sensor.get_humidity.assert_called_once_with(relative=True)


if __name__ == '__main__':
    unittest.main()
