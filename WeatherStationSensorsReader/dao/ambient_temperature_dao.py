from datetime import datetime

from dao.dao import Dao


class AmbientTemperatureDao(Dao):
    """ Represents the ambient temperature database access """

    INSERT_QUERY = 'INSERT INTO ambient_temperatures(temperature, date_time) VALUES(%s, %s)'

    def get_query(self):
        return self.INSERT_QUERY

    def get_parameters(self, values):
        return values[0], datetime.now()
