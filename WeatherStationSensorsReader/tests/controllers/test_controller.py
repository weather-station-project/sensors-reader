import unittest
from unittest import mock
from unittest.mock import Mock, MagicMock

from controllers.controller import Controller
from dao.dao import Dao
from sensors.sensor import Sensor


class TestController(unittest.TestCase):
    def setUp(self):
        self.mock_sensor = Mock(spec=Sensor)
        self.mock_dao = Mock(spec=Dao)

    @mock.patch('controllers.controller.logging')
    def test_constructor_calls_logging_debug(self, mock_logging):
        controller = Controller(sensor=self.mock_sensor, dao=self.mock_dao)

        expected_message = f'Started controller "{controller.__class__.__name__}" ' \
                           f'with Sensor "{self.mock_sensor.__class__.__name__}" ' \
                           f'and DAO "{self.mock_dao.__class__.__name__}".'
        mock_logging.debug.assert_called_once_with(msg=expected_message)

    @mock.patch('controllers.controller.logging')
    def test_execute_expected_calls_are_made(self, mock_logging):
        # arrange
        test_read_result = 'test_read_result'
        self.mock_sensor.read = MagicMock(return_value=test_read_result)

        # act
        controller = Controller(sensor=self.mock_sensor, dao=self.mock_dao)
        controller.execute()

        # assert
        self.mock_sensor.read.assert_called_once()
        mock_logging.info.assert_any_call(msg=f'Obtained "{test_read_result}" from the sensor "{self.mock_sensor.__class__.__name__}".')
        self.mock_dao.insert.assert_called_once_with(values=test_read_result)
        mock_logging.info.assert_called_with(msg=f'{test_read_result} inserted correctly.')


if __name__ == '__main__':
    unittest.main()
