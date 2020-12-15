import unittest
from unittest import mock

from controllers.ambient_temperature_controller import AmbientTemperatureController
from dao.ambient_temperature_dao import AmbientTemperatureDao
from sensors.ambient_temperature_sensor import AmbientTemperatureSensor


class TestAmbientTemperatureController(unittest.TestCase):
    @mock.patch('controllers.ambient_temperature_controller.AmbientTemperatureDao', autospec=True)
    @mock.patch('controllers.ambient_temperature_controller.AmbientTemperatureSensor', autospec=True)
    def test_when_constructor_called_expected_classes_should_be_initialized(self, mock_ambient_temperature_sensor, mock_ambient_temperature_dao):
        # arrange
        test_server = 'test_server'
        test_database = 'test_database'
        test_user = 'test_user'
        test_password = 'test_password'

        # act
        controller = AmbientTemperatureController(server=test_server,
                                                  database=test_database,
                                                  user=test_user,
                                                  password=test_password)

        # assert
        self.assertIsInstance(controller, AmbientTemperatureController)
        self.assertIsInstance(controller.sensor, AmbientTemperatureSensor)
        self.assertIsInstance(controller.dao, AmbientTemperatureDao)

        mock_ambient_temperature_sensor.assert_called_once()
        mock_ambient_temperature_dao.assert_called_once_with(server=test_server,
                                                             database=test_database,
                                                             user=test_user,
                                                             password=test_password)


if __name__ == '__main__':
    unittest.main()
