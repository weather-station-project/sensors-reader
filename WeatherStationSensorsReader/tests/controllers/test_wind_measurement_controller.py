import sys
import unittest
from unittest import mock
from unittest.mock import MagicMock

sys.modules['MCP342X'] = MagicMock()
from controllers.wind_measurement_controller import WindMeasurementController
from dao.wind_measurement_dao import WindMeasurementDao
from sensors.wind_measurement_sensor import WindMeasurementSensor


class TestWindMeasurementController(unittest.TestCase):
    @mock.patch('controllers.wind_measurement_controller.WindMeasurementDao', autospec=True)
    @mock.patch('controllers.wind_measurement_controller.WindMeasurementSensor', autospec=True)
    def test_when_constructor_called_expected_classes_should_be_initialized(self, mock_wind_measurement_sensor, mock_wind_measurement_dao):
        # arrange
        test_server = 'test_server'
        test_database = 'test_database'
        test_user = 'test_user'
        test_password = 'test_password'
        test_port = 25

        # act
        controller = WindMeasurementController(anemometer_port_number=test_port,
                                               server=test_server,
                                               database=test_database,
                                               user=test_user,
                                               password=test_password)

        # assert
        self.assertIsInstance(controller, WindMeasurementController)
        self.assertIsInstance(controller.sensor, WindMeasurementSensor)
        self.assertIsInstance(controller.dao, WindMeasurementDao)

        mock_wind_measurement_sensor.assert_called_once_with(anemometer_port_number=test_port)
        mock_wind_measurement_dao.assert_called_once_with(server=test_server,
                                                          database=test_database,
                                                          user=test_user,
                                                          password=test_password)


if __name__ == '__main__':
    unittest.main()
