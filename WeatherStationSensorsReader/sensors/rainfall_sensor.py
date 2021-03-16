import logging

from gpiozero import Button

from sensors.sensor import Sensor


class RainfallSensor(Sensor):
    """Represents the sensor which measures rainfall"""

    BUCKET_SIZE_IN_MM = 0.2794

    def __init__(self, rain_gauge_port_number):
        self.button = Button(pin=rain_gauge_port_number)
        self.button.when_pressed = self.get_reading

        super().__init__()

        logging.debug(msg=f'Started rain gauge on port "{rain_gauge_port_number}".')

    def add_value_to_readings(self):
        # This sensor does not need to read async as the method when_pressed is the one which does it
        pass

    def get_reading(self):
        return [1]

    def get_average(self):
        return len(self.readings) * self.BUCKET_SIZE_IN_MM
