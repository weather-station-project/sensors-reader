from bme280pi import Sensor as Bme280Sensor

from sensors.sensor import Sensor


class AmbientTemperatureSensor(Sensor):
    """Represents the sensor which measures ambient temperature"""

    def __init__(self):
        self.sensor = Bme280Sensor()

    def read_values(self):
        return [self.sensor.get_temperature(unit='C')]
