import unittest
from datetime import datetime
from unittest import mock

from dao.fake_dao import FakeDao


class TestFakeDao(unittest.TestCase):
    test_server = 'test_server'
    test_database = 'test_database'
    test_user = 'test_user'
    test_password = 'test_password'

    def setUp(self):
        self.dao = FakeDao(server=self.test_server, database=self.test_database, user=self.test_user, password=self.test_password)

    def test_when_constructor_called_properties_should_be_passed_to_the_correctly(self):
        self.assertEqual(self.dao.server, self.test_server)
        self.assertEqual(self.dao.database, self.test_database)
        self.assertEqual(self.dao.user, self.test_user)
        self.assertEqual(self.dao.password, self.test_password)

    def _test_when_getting_query_expected_value_should_be_returned(self):
        self.assertEqual(self.dao.get_query(), self.dao.QUERY)

    @mock.patch('dao.fake_dao.datetime')
    def test_when_getting_parameters_expected_values_should_be_returned(self, mock_datetime):
        # arrange
        test_values = 'test_values'
        expected_values = test_values
        expected_time = datetime.now()
        mock_datetime.now.return_value = expected_time

        # act
        values, date = self.dao.get_parameters(values=test_values)

        # assert
        self.assertEqual(values, expected_values)
        self.assertEqual(date, expected_time)
        mock_datetime.now.assert_called_once()

    def _test_when_getting_health_query_called_expected_value_should_be_returned(self):
        self.assertEqual(self.dao.get_health_check_query(), self.dao.QUERY)


if __name__ == '__main__':
    unittest.main()
