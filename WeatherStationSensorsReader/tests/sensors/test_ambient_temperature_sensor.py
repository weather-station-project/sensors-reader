import sys
import unittest
from unittest import mock
from unittest.mock import MagicMock, Mock

sys.modules['bme280pi'] = MagicMock()
from sensors.ambient_temperature_sensor import AmbientTemperatureSensor


class TestAmbientTemperatureSensor(unittest.TestCase):
    @mock.patch('sensors.ambient_temperature_sensor.Sensor.__init__')
    @mock.patch('sensors.ambient_temperature_sensor.logging')
    @mock.patch('sensors.ambient_temperature_sensor.Bme280Sensor')
    def setUp(self, mock_sensor, mock_logging, mock_super):
        test_chip_id = 'test_chip_id'
        test_chip_version = 'test_chip_version'
        mock_sensor.return_value.chip_id = test_chip_id
        mock_sensor.return_value.chip_version = test_chip_version

        self.test_sensor = AmbientTemperatureSensor()

        self.assertIsNotNone(self.test_sensor)
        mock_sensor.assert_called_once()
        mock_logging.debug.assert_called_once_with(msg=f'Started Bme280 with chip_id "{test_chip_id}" and '
                                                       f'chip_version "{test_chip_version}" in the sensor "{AmbientTemperatureSensor.__name__}".')
        mock_super.assert_called_once()

    def test_when_getting_readings_expected_method_should_be_called(self):
        test_temperature = 45

        mock_sensor = Mock()
        mock_sensor.get_temperature.return_value = test_temperature
        self.test_sensor.sensor = mock_sensor

        self.assertEqual(self.test_sensor.get_reading(), [test_temperature])

        mock_sensor.get_temperature.assert_called_once_with(unit='C')


if __name__ == '__main__':
    unittest.main()
