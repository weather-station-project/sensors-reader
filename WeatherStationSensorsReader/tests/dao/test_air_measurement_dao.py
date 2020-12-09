import unittest
from datetime import datetime
from unittest import mock

from dao.air_measurement_dao import AirMeasurementDao


class TestAirMeasurementDao(unittest.TestCase):
    test_server = 'test_server'
    test_database = 'test_database'
    test_user = 'test_user'
    test_password = 'test_password'

    def setUp(self):
        self.dao = AirMeasurementDao(server=self.test_server, database=self.test_database, user=self.test_user, password=self.test_password)

    def test_when_constructor_called_properties_should_be_passed_to_the_correctly(self):
        self.assertEqual(self.dao.server, self.test_server)
        self.assertEqual(self.dao.database, self.test_database)
        self.assertEqual(self.dao.user, self.test_user)
        self.assertEqual(self.dao.password, self.test_password)

    def test_when_getting_query_expected_value_should_be_returned(self):
        self.assertEqual(self.dao.get_query(), self.dao.INSERT_QUERY)

    @mock.patch('dao.air_measurement_dao.datetime')
    def test_when_getting_parameters_expected_values_should_be_returned(self, mock_datetime):
        # arrange
        test_values = ['test_values', 'test2']
        expected_value = [test_values[0], test_values[1]]
        expected_time = datetime.now()
        mock_datetime.now.return_value = expected_time

        # act
        value1, value2, date = self.dao.get_parameters(values=test_values)

        # assert
        self.assertEqual(value1, expected_value[0])
        self.assertEqual(value2, expected_value[1])
        self.assertEqual(date, expected_time)

        mock_datetime.now.assert_called_once()

    def test_when_getting_health_query_called_expected_value_should_be_returned(self):
        self.assertEqual(self.dao.get_health_check_query(), self.dao.DATA_QUERY)


if __name__ == '__main__':
    unittest.main()