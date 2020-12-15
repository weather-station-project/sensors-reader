import unittest
from unittest import mock

from controllers.fake_controller import FakeController
from dao.fake_dao import FakeDao
from sensors.fake_sensor import FakeSensor


class TestFakeController(unittest.TestCase):
    @mock.patch('controllers.fake_controller.FakeDao', autospec=True)
    @mock.patch('controllers.fake_controller.FakeSensor', autospec=True)
    def test_when_constructor_called_expected_classes_should_be_initialized(self, mock_fake_sensor, mock_fake_dao):
        # arrange
        test_server = 'test_server'
        test_database = 'test_database'
        test_user = 'test_user'
        test_password = 'test_password'

        # act
        controller = FakeController(server=test_server,
                                    database=test_database,
                                    user=test_user,
                                    password=test_password)

        # assert
        self.assertIsInstance(controller, FakeController)
        self.assertIsInstance(controller.sensor, FakeSensor)
        self.assertIsInstance(controller.dao, FakeDao)

        mock_fake_sensor.assert_called_once()
        mock_fake_dao.assert_called_once_with(server=test_server,
                                              database=test_database,
                                              user=test_user,
                                              password=test_password)


if __name__ == '__main__':
    unittest.main()
