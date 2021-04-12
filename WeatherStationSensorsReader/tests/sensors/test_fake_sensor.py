import unittest
from unittest import mock

from sensors.fake_sensor import FakeSensor


class TestFakeSensor(unittest.TestCase):
    @mock.patch('sensors.fake_sensor.Sensor.__init__')
    def test_when_getting_readings_random_number_should_be_returned(self, mock_super):
        # arrange
        mock_super.return_value = None
        fake_sensor = FakeSensor()

        # act
        result = fake_sensor.get_reading()

        # assert
        self.assertIsInstance(result, list)
        self.assertEqual(len(result), fake_sensor.VALUES_NUMBER)
        for value in result:
            self.assertGreaterEqual(value, fake_sensor.MIN_LIMIT)
            self.assertLessEqual(value, fake_sensor.MAX_LIMIT)

        mock_super.assert_called_once()


if __name__ == '__main__':
    unittest.main()
