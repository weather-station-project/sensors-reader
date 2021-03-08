from datetime import datetime

from dao.dao import Dao


class AirMeasurementDao(Dao):
    """ Represents the air measurement database access """

    INSERT_QUERY = 'INSERT INTO air_measurements(pressure, humidity, date_time) VALUES(%s, %s, %s)'

    def get_query(self):
        return self.INSERT_QUERY

    def get_parameters(self, values):
        return values[0], values[1], datetime.now()
