from datetime import datetime

from dao.dao import Dao


class AmbientTemperatureDao(Dao):
    """ Represents ambient temperature database access """

    INSERT_QUERY = 'INSERT INTO ambient_temperatures(temperature, date_time) VALUES(%s, %s)'
    DATA_QUERY = 'SELECT * FROM ambient_temperatures FETCH FIRST ROW ONLY'

    def get_query(self):
        return self.INSERT_QUERY

    def get_parameters(self, values):
        return values[0], datetime.now()

    def get_health_check_query(self):
        return self.DATA_QUERY
