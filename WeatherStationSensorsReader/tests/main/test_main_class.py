import unittest
from unittest.mock import MagicMock

from main.main_class import Main


class MyTestCase(unittest.TestCase):
    def test_when_constructor_called_variables_should_be_assigned(self):
        test_variables = {'a': '1', 'b': '2'}

        main_class = Main(variables=test_variables)

        self.assertEqual(main_class.variables, test_variables)

    @staticmethod
    def test_when_validating_environment_variables_expected_methods_should_be_called():
        main_class = Main(None)
        main_class.validate_generic_variables = MagicMock()
        main_class.validate_sensors_variables = MagicMock()
        main_class.validate_database_variables = MagicMock()

        main_class.validate_environment_variables()

        main_class.validate_generic_variables.assert_called_once()
        main_class.validate_sensors_variables.assert_called_once()
        main_class.validate_database_variables.assert_called_once()

    @staticmethod
    def test_when_validating_generic_variables_expected_methods_should_be_called():
        # arrange
        test_variables = {Main.HEALTH_CHECK_VARIABLE: 'test',
                          Main.LOGGING_LEVEL_VARIABLE: 'test',
                          Main.MINUTES_BETWEEN_READS_VARIABLE: 'test'}
        main_class = Main(variables=test_variables)
        main_class._check_bool_value = MagicMock()
        main_class._check_in_expected_values = MagicMock()
        main_class._check_positive_integer_value = MagicMock()

        # act
        main_class.validate_generic_variables()

        # arrange
        main_class._check_bool_value.assert_called_once_with(variable_name=Main.HEALTH_CHECK_VARIABLE)
        main_class._check_in_expected_values.assert_called_once_with(variable_name=Main.LOGGING_LEVEL_VARIABLE,
                                                                     expected_values=Main.LOGGING_LEVELS.keys())
        main_class._check_positive_integer_value.assert_called_once_with(variable_name=Main.MINUTES_BETWEEN_READS_VARIABLE)

    @staticmethod
    def test_when_validating_generic_variables_given_no_variables_methods_should_not_be_called():
        # arrange
        main_class = Main(variables={})
        main_class._check_bool_value = MagicMock()
        main_class._check_in_expected_values = MagicMock()
        main_class._check_positive_integer_value = MagicMock()

        # act
        main_class.validate_generic_variables()

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



if __name__ == '__main__':
    unittest.main()
