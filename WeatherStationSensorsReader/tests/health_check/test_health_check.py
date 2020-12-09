import logging
import unittest
from unittest import mock
from unittest.mock import MagicMock

from health_check import health_check
from health_check.health_check import configure_logging_critical_level, main
from main.main_class import Main


class TesHealthCheck(unittest.TestCase):
    @mock.patch('health_check.health_check.logging', autospec=True)
    def test_when_configuring_critical_log_expected_method_should_be_called(self, mock_logging):
        # arrange
        mock_logging.CRITICAL = 50

        # act
        self.assertIsNone(configure_logging_critical_level())

        # assert
        mock_logging.basicConfig.assert_called_once_with(level=logging.CRITICAL, format=Main.LOG_FORMAT)

    @mock.patch('health_check.health_check.Main', autospec=True)
    @mock.patch('health_check.health_check.logging', autospec=True)
    def test_when_calling_main_expected_methods_should_be_called(self, mock_logging, mock_main):
        # arrange
        test_controllers = ['test']
        health_check.configure_logging_critical_level = MagicMock()
        mock_main.return_value.get_controllers_enabled.return_value = test_controllers
        mock_main.return_value.execute_controllers_health_check.return_value = None

        # act
        self.assertEqual(main(), 0)

        # assert
        health_check.configure_logging_critical_level.assert_called_once()
        mock_main.return_value.validate_environment_variables.assert_called_once()
        mock_main.return_value.get_controllers_enabled.assert_called_once()
        mock_main.return_value.execute_controllers_health_check.assert_called_once_with(controllers=test_controllers)
        mock_logging.critical.assert_not_called()

    @mock.patch('health_check.health_check.Main', autospec=True)
    @mock.patch('health_check.health_check.logging', autospec=True)
    def test_when_calling_main_given_no_controllers_enabled_error_should_be_logged(self, mock_logging, mock_main):
        # arrange
        health_check.configure_logging_critical_level = MagicMock()
        mock_main.return_value.get_controllers_enabled.return_value = []

        # act
        self.assertEqual(main(), 1)

        # assert
        health_check.configure_logging_critical_level.assert_called_once()
        mock_main.return_value.validate_environment_variables.assert_called_once()
        mock_main.return_value.get_controllers_enabled.assert_called_once()
        mock_main.return_value.execute_controllers_health_check.assert_not_called()
        mock_logging.critical.assert_called_once()


if __name__ == '__main__':
    unittest.main()
