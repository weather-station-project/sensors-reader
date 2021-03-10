import logging

from gpiozero import Button

from devices.samples_during_time_device import SamplesDuringTimeDevice


class RainGauge(SamplesDuringTimeDevice):
    """Represents the device which measures rain fall"""

    BUCKET_SIZE_IN_MM = 0.2794

    def __init__(self, rain_gauge_port_number):
        self.tipped_count = 0
        self.button = Button(pin=rain_gauge_port_number)
        self.button.when_pressed = self.bucket_tipped

        logging.debug(msg=f'Started rain gauge on port "{rain_gauge_port_number}".')

    def bucket_tipped(self):
        self.tipped_count = self.tipped_count + 1
        logging.debug(msg=f'Bucket tipped count {self.tipped_count}.')

    def get_sample(self):
        try:
            rain_amount = self.BUCKET_SIZE_IN_MM * self.tipped_count
            logging.debug(msg=f'Rain sample obtained "{rain_amount}" mm.')

            return rain_amount
        finally:
            self.tipped_count = 0
