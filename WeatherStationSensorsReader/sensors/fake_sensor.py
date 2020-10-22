import random

from sensors.sensor import Sensor


class FakeSensor(Sensor):
    """Represents a fake sensor which returns random numbers"""

    def _read_value(self):
        return random.randint(0, 100)
