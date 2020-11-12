import random

from sensors.sensor import Sensor


class FakeSensor(Sensor):
    """Represents a fake sensor which returns random numbers"""

    MIN_LIMIT = 0
    MAX_LIMIT = 100
    VALUES_NUMBER = 5

    def read_values(self):
        return random.sample(range(self.MIN_LIMIT, self.MAX_LIMIT), self.VALUES_NUMBER)
