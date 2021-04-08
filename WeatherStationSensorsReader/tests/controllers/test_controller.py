import unittest
from unittest import mock
from unittest.mock import Mock

from controllers.controller import Controller
from dao.dao import Dao
from sensors.sensor import Sensor


class TestController(unittest.TestCase):
    def setUp(self):
        self.mock_sensor = Mock(spec=Sensor)
        self.mock_dao = Mock(spec=Dao)

    @mock.patch('controllers.controller.logging')
    def test_when_constructor_called_logging_debug_should_be_called(self, mock_logging):
        controller = Controller(sensor=self.mock_sensor, dao=self.mock_dao)

        expected_message = f'[{controller.__class__.__name__}] Started controller ' \
                           f'with Sensor "{self.mock_sensor.__class__.__name__}" ' \
                           f'and DAO "{self.mock_dao.__class__.__name__}".'
        mock_logging.debug.assert_called_once_with(msg=expected_message)

    @mock.patch('controllers.controller.logging')
    def test_when_normal_execution_expected_methods_should_be_called(self, mock_logging):
        # arrange
        test_read_result = 'test_read_result'
        self.mock_sensor.get_readings_average.return_value = test_read_result

        # act
        controller = Controller(sensor=self.mock_sensor, dao=self.mock_dao)
        self.assertIsNone(controller.execute())

        # assert
        self.mock_sensor.get_readings_average.assert_called_once()
        mock_logging.info.assert_any_call(msg=f'[{self.mock_sensor.__class__.__name__}] Obtained "{test_read_result}" from the sensor.')

        self.mock_dao.insert.assert_called_once_with(values=test_read_result)


if __name__ == '__main__':
    unittest.main()
