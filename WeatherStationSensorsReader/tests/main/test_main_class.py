import logging
import unittest
from unittest import mock
from unittest.mock import MagicMock, Mock

from controllers.controller import Controller
from controllers.fake_controller import FakeController
from main.main_class import Main


class TestMainClass(unittest.TestCase):
    def test_when_constructor_called_variables_should_be_assigned(self):
        test_variables = {'a': '1', 'b': '2'}

        main_class = Main(variables=test_variables)

        self.assertEqual(main_class.variables, test_variables)

    def test_when_validating_environment_variables_expected_methods_should_be_called(self):
        main_class = Main(None)
        main_class.validate_generic_variables = MagicMock()
        main_class.validate_sensors_variables = MagicMock()
        main_class.validate_database_variables = MagicMock()

        self.assertIsNone(main_class.validate_environment_variables())

        main_class.validate_generic_variables.assert_called_once()
        main_class.validate_sensors_variables.assert_called_once()
        main_class.validate_database_variables.assert_called_once()

    def test_when_validating_generic_variables_expected_methods_should_be_called(self):
        # arrange
        test_variables = {Main.HEALTH_CHECK_VARIABLE: 'test',
                          Main.LOGGING_LEVEL_VARIABLE: 'test',
                          Main.MINUTES_BETWEEN_READS_VARIABLE: 'test'}
        main_class = Main(variables=test_variables)
        main_class._check_bool_value = MagicMock()
        main_class._check_in_expected_values = MagicMock()
        main_class._check_positive_integer_value = MagicMock()

        # act
        self.assertIsNone(main_class.validate_generic_variables())

        # arrange
        main_class._check_bool_value.assert_called_once_with(variable_name=Main.HEALTH_CHECK_VARIABLE)
        main_class._check_in_expected_values.assert_called_once_with(variable_name=Main.LOGGING_LEVEL_VARIABLE,
                                                                     expected_values=Main.LOGGING_LEVELS.keys())
        main_class._check_positive_integer_value.assert_called_once_with(variable_name=Main.MINUTES_BETWEEN_READS_VARIABLE)

    def test_when_validating_generic_variables_given_no_variables_methods_should_not_be_called(self):
        # arrange
        main_class = Main(variables={})
        main_class._check_bool_value = MagicMock()
        main_class._check_in_expected_values = MagicMock()
        main_class._check_positive_integer_value = MagicMock()

        # act
        self.assertIsNone(main_class.validate_generic_variables())

        # arrange
        main_class._check_bool_value.assert_not_called()
        main_class._check_in_expected_values.assert_not_called()
        main_class._check_positive_integer_value.assert_not_called()

    def test_when_checking_bool_value_given_true_as_string_no_error_should_be_thrown(self):
        # arrange
        test_variable_name = 'test_variable_name'

        main_class = Main(variables={test_variable_name: 'true'})

        # act
        self.assertIsNone(main_class._check_bool_value(variable_name=test_variable_name))

    def test_when_checking_bool_value_given_false_as_string_no_error_should_be_thrown(self):
        # arrange
        test_variable_name = 'test_variable_name'

        main_class = Main(variables={test_variable_name: 'false'})

        # act
        self.assertIsNone(main_class._check_bool_value(variable_name=test_variable_name))

    def test_when_checking_bool_value_given_non_bool_string_error_should_be_thrown(self):
        # arrange
        test_variable_name = 'test_variable_name'

        main_class = Main(variables={test_variable_name: 'test'})

        # act
        with self.assertRaises(ValueError):
            main_class._check_bool_value(variable_name=test_variable_name)

    def test_when_checking_value_in_expected_values_given_value_included_no_error_should_be_thrown(self):
        # arrange
        test_variable_name = 'test_variable_name'
        test_expected_values = ['test1', 'test2']

        main_class = Main(variables={test_variable_name: test_expected_values[0]})

        # act
        self.assertIsNone(main_class._check_in_expected_values(variable_name=test_variable_name,
                                                               expected_values=test_expected_values))

    def test_when_checking_value_in_expected_values_given_value_not_included_error_should_be_thrown(self):
        # arrange
        test_variable_name = 'test_variable_name'
        test_expected_values = ['test1', 'test2']

        main_class = Main(variables={test_variable_name: 'blablabla'})

        # act
        with self.assertRaises(ValueError):
            main_class._check_in_expected_values(variable_name=test_variable_name,
                                                 expected_values=test_expected_values)

    def test_when_checking_positive_integer_given_invalid_number_error_should_be_thrown(self):
        # arrange
        test_variable_name = 'test_variable_name'

        main_class = Main(variables={test_variable_name: 'a'})

        # act
        with self.assertRaises(ValueError):
            main_class._check_positive_integer_value(variable_name=test_variable_name)

    def test_when_checking_positive_integer_given_negative_number_error_should_be_thrown(self):
        # arrange
        test_variable_name = 'test_variable_name'

        main_class = Main(variables={test_variable_name: '-1'})

        # act
        with self.assertRaises(ValueError):
            main_class._check_positive_integer_value(variable_name=test_variable_name)

    def test_when_checking_positive_integer_given_valid_positive_no_error_should_be_thrown(self):
        # arrange
        test_variable_name = 'test_variable_name'

        main_class = Main(variables={test_variable_name: '10'})

        # act
        self.assertIsNone(main_class._check_positive_integer_value(variable_name=test_variable_name))

    def test_when_validating_sensors_variables_expected_methods_should_be_called(self):
        # arrange
        test_variables = {Main.FAKE_SENSOR_VARIABLE: 'test',
                          Main.BME_280_SENSOR_VARIABLE: 'test',
                          Main.GROUND_SENSOR_VARIABLE: 'test',
                          Main.RAINFALL_SENSOR_VARIABLE: 'test',
                          Main.WIND_SENSOR_VARIABLE: 'test'}
        main_class = Main(variables=test_variables)
        main_class._check_bool_value = MagicMock()

        # act
        self.assertIsNone(main_class.validate_sensors_variables())

        # assert
        main_class._check_bool_value.assert_any_call(variable_name=Main.FAKE_SENSOR_VARIABLE)
        main_class._check_bool_value.assert_any_call(variable_name=Main.BME_280_SENSOR_VARIABLE)
        main_class._check_bool_value.assert_any_call(variable_name=Main.GROUND_SENSOR_VARIABLE)
        main_class._check_bool_value.assert_any_call(variable_name=Main.RAINFALL_SENSOR_VARIABLE)
        main_class._check_bool_value.assert_any_call(variable_name=Main.WIND_SENSOR_VARIABLE)

    def test_when_validating_sensors_variables_given_no_variables_methods_should_not_be_called(self):
        # arrange
        main_class = Main(variables={})
        main_class._check_bool_value = MagicMock()

        # act
        self.assertIsNone(main_class.validate_sensors_variables())

        # assert
        main_class._check_bool_value.assert_not_called()

    def test_when_validating_database_variables_expected_methods_should_be_called(self):
        # arrange
        test_variables = {Main.SERVER_VARIABLE: 'test',
                          Main.DATABASE_VARIABLE: 'test',
                          Main.USER_VARIABLE: 'test',
                          Main.PASSWORD_VARIABLE: 'test'}
        main_class = Main(variables=test_variables)
        main_class._check_not_null_value = MagicMock()

        # act
        self.assertIsNone(main_class.validate_database_variables())

        # assert
        main_class._check_not_null_value.assert_any_call(variable_name=Main.SERVER_VARIABLE)
        main_class._check_not_null_value.assert_any_call(variable_name=Main.DATABASE_VARIABLE)
        main_class._check_not_null_value.assert_any_call(variable_name=Main.USER_VARIABLE)
        main_class._check_not_null_value.assert_any_call(variable_name=Main.PASSWORD_VARIABLE)

    def test_when_validating_database_variables_given_no_variables_methods_should_not_be_called(self):
        # arrange
        main_class = Main(variables={})
        main_class._check_not_null_value = MagicMock()

        # act
        self.assertIsNone(main_class.validate_database_variables())

        # assert
        main_class._check_not_null_value.assert_not_called()

    def test_when_checking_not_null_value_given_empty_string_error_should_be_thrown(self):
        # arrange
        test_variable_name = 'test_variable_name'

        main_class = Main(variables={test_variable_name: ''})

        # act
        with self.assertRaises(ValueError):
            main_class._check_not_null_value(variable_name=test_variable_name)

    def test_when_checking_not_null_value_given_something_no_error_should_be_thrown(self):
        # arrange
        test_variable_name = 'test_variable_name'

        main_class = Main(variables={test_variable_name: 'test'})

        # act
        self.assertIsNone(main_class._check_not_null_value(variable_name=test_variable_name))

    @mock.patch('main.main_class.logging', autospec=True)
    def test_when_configuring_logging_given_no_variable_nothing_should_be_configured(self, mock_logging):
        # arrange
        main_class = Main(variables={})

        # act
        self.assertIsNone(main_class.configure_logging())

        # assert
        mock_logging.root.removeHandler.assert_not_called()
        mock_logging.basicConfig.assert_not_called()

    @mock.patch('main.main_class.logging', autospec=True)
    def test_when_configuring_logging_given_expected_methods_should_be_called(self, mock_logging):
        # arrange
        main_class = Main(variables={Main.LOGGING_LEVEL_VARIABLE: 'WARNING'})

        # act
        self.assertIsNone(main_class.configure_logging())

        # assert
        mock_logging.basicConfig.assert_called_once_with(level=logging.WARNING, format=Main.LOG_FORMAT)

    @mock.patch('main.main_class.FakeController', autospec=True)
    def test_when_getting_controllers_given_no_variables_empty_list_should_be_returned(self, mock_fake_controller):
        # arrange
        main_class = Main(variables={})

        # act
        result = main_class.get_controllers_enabled()

        # assert
        self.assertIsInstance(result, list)
        self.assertEqual(len(result), 0)
        mock_fake_controller.assert_not_called()

    @mock.patch('main.main_class.FakeController', autospec=True)
    def test_when_getting_controllers_given_fake_sensor_only_fake_controller_should_be_returned(self, mock_fake_controller):
        # arrange
        test_server = 'test_server'
        test_database = 'test_database'
        test_user = 'test_user'
        test_password = 'test_password'

        main_class = Main(variables={Main.FAKE_SENSOR_VARIABLE: 'true',
                                     Main.SERVER_VARIABLE: test_server,
                                     Main.DATABASE_VARIABLE: test_database,
                                     Main.USER_VARIABLE: test_user,
                                     Main.PASSWORD_VARIABLE: test_password})

        # act
        result = main_class.get_controllers_enabled()

        # assert
        self.assertIsInstance(result, list)
        self.assertEqual(len(result), 1)
        self.assertIsInstance(result[0], FakeController)
        mock_fake_controller.assert_called_once_with(server=test_server,
                                                     database=test_database,
                                                     user=test_user,
                                                     password=test_password)

    def test_when_getting_minutes_given_no_variable_default_should_be_returned(self):
        # arrange
        main_class = Main(variables={})

        # act
        self.assertEqual(main_class.get_minutes_between_reads(), Main.DEFAULT_MINUTES_BETWEEN_READS)

    def test_when_getting_minutes_given_value_expected_value_should_be_returned(self):
        # arrange
        test_value = '5'
        main_class = Main(variables={Main.MINUTES_BETWEEN_READS_VARIABLE: test_value})

        # act
        self.assertEqual(main_class.get_minutes_between_reads(), int(test_value))

    @mock.patch('main.main_class.logging', autospec=True)
    def test_when_executing_controllers_given_empty_list_nothing_should_be_executed(self, mock_logging):
        # arrange
        main_class = Main(variables={})
        mock_controller = Mock(spec=Controller)
        test_controllers = []

        # act
        self.assertIsNone(main_class.execute_controllers(test_controllers))

        # assert
        mock_controller.execute.assert_not_called()
        mock_logging.error.assert_not_called()

    @mock.patch('main.main_class.logging', autospec=True)
    def test_when_executing_controllers_given_controllers_they_should_be_executed(self, mock_logging):
        # arrange
        main_class = Main(variables={})
        mock_controller = Mock(spec=Controller)
        test_controllers = [mock_controller]

        # act
        self.assertIsNone(main_class.execute_controllers(test_controllers))

        # assert
        mock_controller.execute.assert_called_once()
        mock_logging.error.assert_not_called()

    @mock.patch('main.main_class.logging', autospec=True)
    def test_when_executing_controllers_given_failing_controllers_error_should_not_be_thrown(self, mock_logging):
        # arrange
        main_class = Main(variables={})
        mock_controller = Mock(spec=Controller)
        mock_controller.execute.side_effect = Exception('test')
        test_controllers = [mock_controller]

        # act
        self.assertIsNone(main_class.execute_controllers(test_controllers))

        # assert
        mock_controller.execute.assert_called_once()
        mock_logging.error.assert_called_once_with(f'Error while executing controller "{mock_controller.__class__.__name__}". ',
                                                   mock_controller.execute.side_effect)


if __name__ == '__main__':
    unittest.main()
