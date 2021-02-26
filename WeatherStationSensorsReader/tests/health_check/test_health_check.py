import logging
import sys
import unittest
from unittest import mock
from unittest.mock import MagicMock

from health_check import health_check
from health_check.health_check import configure_logging_critical_level, main

sys.modules['bme280pi'] = MagicMock()
sys.modules['w1thermsensor'] = MagicMock()
from main.main_class import Main


class TesHealthCheck(unittest.TestCase):
    @mock.patch('health_check.health_check.logging')
    def test_when_configuring_critical_log_expected_method_should_be_called(self, mock_logging):
        # arrange
        mock_logging.CRITICAL = 50

        # act
        self.assertIsNone(configure_logging_critical_level())

        # assert
        mock_logging.basicConfig.assert_called_once_with(level=logging.CRITICAL, format=Main.LOG_FORMAT)

    @mock.patch('health_check.health_check.logging')
    @mock.patch('health_check.health_check.get_error_messages')
    def test_when_calling_main_expected_methods_should_be_called(self, mock_get, mock_logging):
        # arrange
        health_check.configure_logging_critical_level = MagicMock()
        mock_get.return_value = False

        # act
        self.assertEqual(main(), 0)

        # assert
        health_check.configure_logging_critical_level.assert_called_once()
        mock_logging.critical.assert_not_called()
        mock_get.assert_called_once()

    @mock.patch('health_check.health_check.logging')
    @mock.patch('health_check.health_check.get_error_messages')
    def test_when_getting_errors_exception_should_be_thrown(self, mock_get, mock_logging):
        # arrange
        health_check.configure_logging_critical_level = MagicMock()
        mock_get.return_value = True

        # act
        self.assertEqual(main(), 1)

        # assert
        health_check.configure_logging_critical_level.assert_called_once()
        mock_logging.critical.assert_called_once()
        mock_get.assert_called_once()


if __name__ == '__main__':
    unittest.main()
