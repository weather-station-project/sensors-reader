import sys
import unittest
from unittest import mock
from unittest.mock import MagicMock, Mock

sys.modules['bme280pi'] = MagicMock()
from sensors.ambient_temperature_sensor import AmbientTemperatureSensor


class TestAmbientTemperatureSensor(unittest.TestCase):
    @mock.patch('sensors.ambient_temperature_sensor.logging')
    @mock.patch('sensors.ambient_temperature_sensor.Bme280Sensor')
    def test_when_calling_constructor_new_mock_should_be_initialized(self, mock_sensor, mock_logging):
        test_chip_id = 'test_chip_id'
        test_chip_version = 'test_chip_version'

        mock_sensor.return_value.chip_id = test_chip_id
        mock_sensor.return_value.chip_version = test_chip_version
        self.assertIsNotNone(AmbientTemperatureSensor())

        mock_sensor.assert_called_once()
        mock_logging.debug.assert_called_once_with(msg=f'Started Bme280 with chip_id "{test_chip_id}" and '
                                                       f'chip_version "{test_chip_version}" in the sensor "{AmbientTemperatureSensor.__name__}".')

    @mock.patch('sensors.ambient_temperature_sensor.Bme280Sensor')
    def test_when_reading_values_expected_method_should_be_called(self, mock_bme280_sensor):
        test_temperature = 45

        mock_sensor = Mock()
        mock_sensor.get_temperature.return_value = test_temperature
        mock_bme280_sensor.return_value = mock_sensor

        self.assertEqual(AmbientTemperatureSensor().read_values(), [test_temperature])

        mock_sensor.get_temperature.assert_called_once_with(unit='C')


if __name__ == '__main__':
    unittest.main()
