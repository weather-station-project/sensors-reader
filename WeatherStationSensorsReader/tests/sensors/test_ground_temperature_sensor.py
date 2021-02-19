import sys
import unittest
from unittest import mock
from unittest.mock import MagicMock, Mock

sys.modules['w1thermsensor'] = MagicMock()
from sensors.ground_temperature_sensor import GroundTemperatureSensor


class TestGroundTemperatureSensor(unittest.TestCase):
    @mock.patch('sensors.ground_temperature_sensor.logging')
    @mock.patch('sensors.ground_temperature_sensor.W1ThermSensor')
    def test_when_calling_constructor_new_mock_should_be_initialized(self, mock_sensor, mock_logging):
        test_id = 'test_id'
        test_type = 'test_type'

        mock_sensor.return_value.id = test_id
        mock_sensor.return_value.type_name = test_type
        self.assertIsNotNone(GroundTemperatureSensor())

        mock_sensor.assert_called_once()
        mock_logging.debug.assert_called_once_with(msg=f'Started W1ThermSensor with id "{test_id}" and '
                                                       f'type "{test_type}" in the sensor "{GroundTemperatureSensor.__name__}".')

    @mock.patch('sensors.ground_temperature_sensor.W1ThermSensor')
    def test_when_reading_values_expected_method_should_be_called(self, mock_w1thermsensor_sensor):
        test_temperature = 45

        mock_sensor = Mock()
        mock_sensor.get_temperature.return_value = test_temperature
        mock_sensor.DEGREES_C = 0x01
        mock_w1thermsensor_sensor.return_value = mock_sensor

        self.assertEqual(GroundTemperatureSensor().read_values(), [test_temperature])

        mock_sensor.get_temperature.assert_called_once_with(unit=mock_sensor.DEGREES_C)

    @mock.patch('sensors.ground_temperature_sensor.W1ThermSensor')
    def test_when_executing_health_check_nothing_should_be_returned_and_expected_methods_should_be_called(self, mock_w1thermsensor_sensor):
        mock_sensor = Mock()
        mock_sensor.get_temperature.return_value = 50
        mock_sensor.DEGREES_C = 0x01
        mock_w1thermsensor_sensor.return_value = mock_sensor

        self.assertIsNone(GroundTemperatureSensor().health_check())

        mock_sensor.get_temperature.assert_called_once_with(unit=mock_sensor.DEGREES_C)


if __name__ == '__main__':
    unittest.main()
