from statistics import mean

from sensors.anemometer import Anemometer
from sensors.sensor import Sensor
from sensors.vane import Vane


class WindMeasurementSensor(Sensor):
    """Represents the sensor which measures wind speed, wind direction and wind gust"""

    def __init__(self):
        self.anemometer = Anemometer()
        self.vane = Vane()

    def read_values(self):
        speed_samples = self.anemometer.get_wind_speed_samples()

        direction_angle = self.vane.get_wind_direction_angle()
        wind_speed = mean(data=speed_samples)
        gust_speed = max(speed_samples)

        return [direction_angle, wind_speed, gust_speed]

    def get_averages(self, reads):
        transposed_matrix = list(zip(*reads))

        return [self.vane.get_direction_average(direction_angles=transposed_matrix[0]),
                mean(data=transposed_matrix[1]),
                mean(data=transposed_matrix[2])]
