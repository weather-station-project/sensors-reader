import sys
import unittest
from unittest import mock
from unittest.mock import MagicMock, Mock

sys.modules['w1thermsensor'] = MagicMock()
from sensors.ground_temperature_sensor import GroundTemperatureSensor


class TestGroundTemperatureSensor(unittest.TestCase):
    @mock.patch('sensors.ground_temperature_sensor.Sensor.__init__')
    @mock.patch('sensors.ground_temperature_sensor.logging')
    @mock.patch('sensors.ground_temperature_sensor.W1ThermSensor')
    def setUp(self, mock_sensor, mock_logging, mock_super):
        test_id = 'test_id'
        test_type = 'test_type'
        mock_sensor.return_value.id = test_id
        mock_sensor.return_value.type_name = test_type

        self.test_sensor = GroundTemperatureSensor()

        self.assertIsNotNone(self.test_sensor)
        mock_sensor.assert_called_once()
        mock_logging.debug.assert_called_once_with(msg=f'[{GroundTemperatureSensor.__name__}] Started W1ThermSensor with id "{test_id}".')
        mock_super.assert_called_once_with()

    def test_when_getting_readings_expected_method_should_be_called(self):
        test_temperature = 45

        mock_sensor = Mock()
        mock_sensor.get_temperature.return_value = test_temperature
        mock_sensor.DEGREES_C = 0x01
        self.test_sensor.sensor = mock_sensor

        self.assertEqual(self.test_sensor.get_reading(), [test_temperature])


if __name__ == '__main__':
    unittest.main()
