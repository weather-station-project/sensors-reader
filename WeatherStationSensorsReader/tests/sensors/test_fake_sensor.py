import unittest

from sensors.fake_sensor import FakeSensor


class TestFakeSensor(unittest.TestCase):
    def test_when_reading_values_random_number_should_be_returned(self):
        fake_sensor = FakeSensor()

        result = fake_sensor.read_values()

        self.assertIsInstance(result, list)
        self.assertEqual(len(result), fake_sensor.VALUES_NUMBER)
        for value in result:
            self.assertGreaterEqual(value, fake_sensor.MIN_LIMIT)
            self.assertLessEqual(value, fake_sensor.MAX_LIMIT)


if __name__ == '__main__':
    unittest.main()
