from sensors.sensor import Sensor
import random


class FakeSensor(Sensor):
    def _read_value(self):
        return random.randint(0, 100)
