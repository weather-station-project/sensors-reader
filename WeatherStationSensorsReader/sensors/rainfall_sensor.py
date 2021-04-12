import logging

from gpiozero import Button

from health_check.health_check_file_manager import register_success_for_class_into_health_check_file
from sensors.sensor import Sensor


class RainfallSensor(Sensor):
    """Represents the sensor which measures rainfall"""

    BUCKET_SIZE_IN_MM = 0.2794

    def __init__(self, rain_gauge_port_number):
        self.button = Button(pin=rain_gauge_port_number)
        self.button.when_pressed = self.get_reading

        super().__init__()

        logging.debug(msg=f'[{self.__class__.__name__}] Started on the port "{rain_gauge_port_number}".')

    def add_value_to_readings(self):
        # This sensor does not need to read async as the method when_pressed is the one which does it
        pass

    def get_reading(self):
        logging.debug(msg=f'[{self.__class__.__name__}] Pressed.')
        self.readings.append(1)

    def get_readings_average(self):
        try:
            self.getting_readings = True
            sensor_name = self.__class__.__name__

            logging.debug(msg=f'[{sensor_name}] Getting amount of rain from the value "{len(self.readings)}"')
            average = self.get_average()
            register_success_for_class_into_health_check_file(class_name=sensor_name)

            return average
        finally:
            del self.readings[:]
            self.getting_readings = False

    def get_average(self):
        return [len(self.readings) * self.BUCKET_SIZE_IN_MM]
