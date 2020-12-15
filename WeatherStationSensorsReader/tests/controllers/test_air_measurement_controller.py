import unittest
from unittest import mock

from controllers.air_measurement_controller import AirMeasurementController
from dao.air_measurement_dao import AirMeasurementDao
from sensors.air_measurement_sensor import AirMeasurementSensor


class TestAirMeasurementController(unittest.TestCase):
    @mock.patch('controllers.air_measurement_controller.AirMeasurementDao', autospec=True)
    @mock.patch('controllers.air_measurement_controller.AirMeasurementSensor', autospec=True)
    def test_when_constructor_called_expected_classes_should_be_initialized(self, mock_air_measurement_sensor, mock_air_measurement_dao):
        # arrange
        test_server = 'test_server'
        test_database = 'test_database'
        test_user = 'test_user'
        test_password = 'test_password'

        # act
        controller = AirMeasurementController(server=test_server,
                                              database=test_database,
                                              user=test_user,
                                              password=test_password)

        # assert
        self.assertIsInstance(controller, AirMeasurementController)
        self.assertIsInstance(controller.sensor, AirMeasurementSensor)
        self.assertIsInstance(controller.dao, AirMeasurementDao)

        mock_air_measurement_sensor.assert_called_once()
        mock_air_measurement_dao.assert_called_once_with(server=test_server,
                                                         database=test_database,
                                                         user=test_user,
                                                         password=test_password)


if __name__ == '__main__':
    unittest.main()
