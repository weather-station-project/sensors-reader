import logging
import sys
import unittest
from unittest import mock
from unittest.mock import MagicMock

sys.modules['bme280pi'] = MagicMock()
sys.modules['w1thermsensor'] = MagicMock()
from app import app
from app.app import configure_default_logging, get_true, main
from main.main_class import Main


class TestApp(unittest.TestCase):
    @mock.patch('app.app.logging')
    def test_when_configuring_default_log_expected_method_should_be_called(self, mock_logging):
        # arrange
        mock_logging.ERROR = 40

        # act
        self.assertIsNone(configure_default_logging())

        # assert
        mock_logging.basicConfig.assert_called_once_with(level=logging.ERROR, format=Main.LOG_FORMAT)

    def test_when_getting_true_true_value_should_be_returned(self):
        self.assertTrue(get_true())

    @mock.patch('app.app.sleep')
    @mock.patch('app.app.Main')
    @mock.patch('app.app.logging')
    def test_when_calling_main_expected_methods_should_be_called(self, mock_logging, mock_main, mock_sleep):
        # arrange
        test_controllers = ['test']
        test_time = 1
        app.configure_default_logging = MagicMock()
        mock_main.return_value.get_controllers_enabled.return_value = test_controllers
        mock_main.return_value.get_minutes_between_reads.return_value = test_time
        mock_main.return_value.execute_controllers.return_value = None
        app.get_true = MagicMock(side_effect=[True, False])
        app.erase_health_check_file = MagicMock()

        # act
        self.assertEqual(main(), 0)

        # assert
        app.configure_default_logging.assert_called_once()
        mock_main.return_value.validate_environment_variables.assert_called_once()
        mock_main.return_value.configure_logging.assert_called_once()
        mock_main.return_value.get_controllers_enabled.assert_called_once()
        mock_main.return_value.get_minutes_between_reads.assert_called_once()
        app.get_true.assert_any_call()
        app.erase_health_check_file.assert_called_once()
        mock_main.return_value.execute_controllers.assert_called_once_with(controllers=test_controllers)
        mock_logging.debug.assert_called_once_with(msg=f'Sleeping "{test_time * 60}" seconds.')
        mock_sleep.assert_any_call(test_time * 60)
        mock_logging.critical.assert_not_called()

    @mock.patch('app.app.sleep')
    @mock.patch('app.app.Main')
    @mock.patch('app.app.logging')
    def test_when_calling_main_given_no_controllers_enabled_error_should_be_logged(self, mock_logging, mock_main, mock_sleep):
        # arrange
        app.configure_default_logging = MagicMock()
        mock_main.return_value.get_controllers_enabled.return_value = []
        app.get_true = MagicMock(side_effect=[True, False])
        app.erase_health_check_file = MagicMock()

        # act
        self.assertEqual(main(), 1)

        # assert
        app.configure_default_logging.assert_called_once()
        mock_main.return_value.validate_environment_variables.assert_called_once()
        mock_main.return_value.configure_logging.assert_called_once()
        mock_main.return_value.get_controllers_enabled.assert_called_once()
        mock_main.return_value.get_minutes_between_reads.assert_not_called()
        app.get_true.assert_not_called()
        app.erase_health_check_file.assert_called_once()
        mock_main.return_value.execute_controllers.assert_not_called()
        mock_logging.debug.assert_not_called()
        mock_sleep.assert_not_called()
        mock_logging.critical.assert_called_once()


if __name__ == '__main__':
    unittest.main()
