from devices.anemometer import Anemometer
from devices.vane import Vane
from sensors.sensor import Sensor


class WindMeasurementSensor(Sensor):
    """Represents the sensor which measures wind speed and wind direction"""

    def __init__(self, anemometer_port_number):
        self.anemometer = Anemometer(anemometer_port_number=anemometer_port_number)
        self.vane = Vane()

        super().__init__()

    def get_reading(self):
        return self.vane.get_reading()

    def get_average(self):
        return [self.vane.get_direction_average(angles=self.readings), self.anemometer.get_speed()]
