from devices.rain_gauge import RainGauge
from sensors.sensor import Sensor


class RainfallSensor(Sensor):
    """Represents the sensor which measures rainfall"""

    NUMBER_OF_READS = 1

    def __init__(self, rain_gauge_port_number):
        self.rain_gauge = RainGauge(rain_gauge_port_number=rain_gauge_port_number)

    def get_number_of_reads(self):
        return self.NUMBER_OF_READS

    def read_values(self):
        return [self.rain_gauge.get_sample()]
