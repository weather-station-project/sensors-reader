import logging
import os
import unittest
from unittest import mock
from unittest.mock import MagicMock

from app import app
from app.app import configure_default_logging, get_true, main
from main.main_class import Main


class TestApp(unittest.TestCase):
    @mock.patch('app.app.logging', autospec=True)
    def test_when_configuring_default_log_expected_method_should_be_called(self, mock_logging):
        # arrange
        mock_logging.ERROR = 40

        # act
        self.assertIsNone(configure_default_logging())

        # assert
        mock_logging.basicConfig.assert_called_once_with(level=logging.ERROR, format=Main.LOG_FORMAT)

    def test_when_getting_true_true_value_should_be_returned(self):
        self.assertTrue(get_true())

    @mock.patch('app.app.sleep', autospec=True)
    @mock.patch('app.app.Main', autospec=True)
    @mock.patch('app.app.logging', autospec=True)
    def test_when_calling_main_expected_methods_should_be_called(self, mock_logging, mock_main, mock_sleep):
        # arrange
        test_controllers = ['test']
        app.configure_default_logging = MagicMock()
        app.get_true = MagicMock(side_effect=[True, False])

        # act
        self.assertEqual(main(), 0)

        # assert
        app.configure_default_logging.assert_called_once()
        # mock_main.validate_environment_variables.assert_called_once()
        # mock_main.configure_logging.assert_called_once()
        # mock_main.get_controllers_enabled.assert_called_once()
        app.get_true.assert_any_call()
        mock_logging.debug.assert_called_once_with(msg=f'Sleeping "0" seconds.')



if __name__ == '__main__':
    unittest.main()
