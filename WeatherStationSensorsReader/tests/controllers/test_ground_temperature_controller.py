import sys
import unittest
from unittest import mock
from unittest.mock import MagicMock

sys.modules['w1thermsensor'] = MagicMock()
from controllers.ground_temperature_controller import GroundTemperatureController
from dao.ground_temperature_dao import GroundTemperatureDao
from sensors.ground_temperature_sensor import GroundTemperatureSensor


class TestGroundTemperatureController(unittest.TestCase):
    @mock.patch('controllers.ground_temperature_controller.GroundTemperatureDao', autospec=True)
    @mock.patch('controllers.ground_temperature_controller.GroundTemperatureSensor', autospec=True)
    def test_when_constructor_called_expected_classes_should_be_initialized(self, mock_ground_temperature_sensor, mock_ground_temperature_dao):
        # arrange
        test_server = 'test_server'
        test_database = 'test_database'
        test_user = 'test_user'
        test_password = 'test_password'

        # act
        controller = GroundTemperatureController(server=test_server,
                                                 database=test_database,
                                                 user=test_user,
                                                 password=test_password)

        # assert
        self.assertIsInstance(controller, GroundTemperatureController)
        self.assertIsInstance(controller.sensor, GroundTemperatureSensor)
        self.assertIsInstance(controller.dao, GroundTemperatureDao)

        mock_ground_temperature_sensor.assert_called_once()
        mock_ground_temperature_dao.assert_called_once_with(server=test_server,
                                                            database=test_database,
                                                            user=test_user,
                                                            password=test_password)


if __name__ == '__main__':
    unittest.main()
