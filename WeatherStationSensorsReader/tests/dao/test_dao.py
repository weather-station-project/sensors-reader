import unittest
from unittest import mock
from unittest.mock import MagicMock

from dao.dao import Dao


class TestDao(unittest.TestCase):
    test_server = 'test_server'
    test_database = 'test_database'
    test_user = 'test_user'
    test_password = 'test_password'

    test_query = 'test_query'
    test_values = 'test_values'
    test_parameter_values = 'test_parameter_values'
    test_health_check_query = 'test_health_check_query'

    def setUp(self):
        Dao.__abstractmethods__ = set()
        self.dao = Dao(server=self.test_server, database=self.test_database, user=self.test_user, password=self.test_password)
        self.dao.get_query = MagicMock(return_value=self.test_query)
        self.dao.get_parameters = MagicMock(return_value=self.test_parameter_values)
        self.dao.get_health_check_query = MagicMock(return_value=self.test_health_check_query)

    def test_when_constructor_called_properties_should_be_assigned_correctly(self):
        self.assertEqual(self.dao.server, self.test_server)
        self.assertEqual(self.dao.database, self.test_database)
        self.assertEqual(self.dao.user, self.test_user)
        self.assertEqual(self.dao.password, self.test_password)

    @mock.patch('dao.dao.logging', autospec=True)
    def test_when_no_server_warning_should_be_raised(self, mock_logging):
        Dao(server='', database=self.test_database, user=self.test_user, password=self.test_password).insert(values=None)

        mock_logging.warning.assert_called_once_with(msg='Database connection not configured, the data will not be stored anywhere.')

    @mock.patch('dao.dao.logging', autospec=True)
    def test_when_values_is_null_exception_should_be_thrown(self, mock_logging):
        with self.assertRaises(ValueError):
            self.dao.insert(values=None)

        mock_logging.warning.assert_not_called()

    @mock.patch('dao.dao.psycopg2', autospec=True)
    @mock.patch('dao.dao.logging', autospec=True)
    def test_when_error_on_connection_exception_should_be_thrown(self, mock_logging, mock_psycopg2):
        # arrange
        mock_psycopg2.connect.side_effect = Exception('test')

        # act
        with self.assertRaises(Exception):
            self.dao.insert(values=self.test_values)

        # assert
        mock_logging.warning.assert_not_called()
        self.dao.get_query.assert_called_once()
        self.dao.get_parameters.assert_called_once_with(values=self.test_values)
        mock_psycopg2.connect.assert_called_once_with(host=self.test_server,
                                                      database=self.test_database,
                                                      user=self.test_user,
                                                      password=self.test_password)
        mock_logging.debug.assert_not_called()

    @mock.patch('psycopg2.connect')
    @mock.patch('dao.dao.logging', autospec=True)
    def test_when_no_error_values_should_be_inserted(self, mock_logging, mock_connect):
        # act
        self.assertIsNone(self.dao.insert(values=self.test_values))

        # assert
        mock_logging.warning.assert_not_called()
        self.dao.get_query.assert_called_once()
        self.dao.get_parameters.assert_called_once_with(values=self.test_values)
        mock_connect.assert_called_once_with(host=self.test_server,
                                             database=self.test_database,
                                             user=self.test_user,
                                             password=self.test_password)
        mock_connect().__enter__().cursor.assert_called_once()
        mock_connect().__enter__().cursor().__enter__().execute.assert_called_once_with(query=self.test_query, vars=self.test_parameter_values)
        mock_logging.debug.assert_called_once_with(msg=f'Executed query "{self.test_query}" with values {self.test_parameter_values}.')

    @mock.patch('psycopg2.connect')
    def test_when_checking_health_query_should_be_executed(self, mock_connect):
        # act
        self.assertIsNone(self.dao.health_check())

        # assert
        self.dao.get_health_check_query.assert_called_once()
        mock_connect.assert_called_once_with(host=self.test_server,
                                             database=self.test_database,
                                             user=self.test_user,
                                             password=self.test_password)
        mock_connect().__enter__().cursor.assert_called_once()
        mock_connect().__enter__().cursor().__enter__().execute.assert_called_once_with(query=self.test_health_check_query)


if __name__ == '__main__':
    unittest.main()
