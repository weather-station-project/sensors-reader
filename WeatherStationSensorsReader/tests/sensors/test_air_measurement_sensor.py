import sys
import unittest
from unittest import mock
from unittest.mock import MagicMock, Mock

sys.modules['bme280pi'] = MagicMock()
from sensors.air_measurement_sensor import AirMeasurementSensor


class TestAirMeasurementSensor(unittest.TestCase):
    @mock.patch('sensors.air_measurement_sensor.Sensor.__init__')
    @mock.patch('sensors.air_measurement_sensor.logging')
    @mock.patch('sensors.air_measurement_sensor.Bme280Sensor')
    def setUp(self, mock_sensor, mock_logging, mock_super):
        test_chip_id = 'test_chip_id'
        test_chip_version = 'test_chip_version'
        mock_sensor.return_value.chip_id = test_chip_id
        mock_sensor.return_value.chip_version = test_chip_version

        self.test_sensor = AirMeasurementSensor()

        self.assertIsNotNone(self.test_sensor)
        mock_sensor.assert_called_once()
        mock_logging.debug.assert_called_once_with(msg=f'Started Bme280 with chip_id "{test_chip_id}" and '
                                                       f'chip_version "{test_chip_version}" in the sensor "{AirMeasurementSensor.__name__}".')
        mock_super.assert_called_once()

    def test_when_getting_readings_expected_method_should_be_called(self):
        test_pressure = 1024
        test_humidity = 67

        mock_sensor = Mock()
        mock_sensor.get_data.return_value = {'pressure': test_pressure, 'humidity': test_humidity}
        self.test_sensor.sensor = mock_sensor

        self.assertEqual(self.test_sensor.get_reading(), [test_pressure, test_humidity])

        mock_sensor.get_data.assert_called_once()


if __name__ == '__main__':
    unittest.main()
