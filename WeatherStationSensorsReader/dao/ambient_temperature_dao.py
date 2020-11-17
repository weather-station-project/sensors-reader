from datetime import datetime

from dao.dao import Dao


class AmbientTemperatureDao(Dao):
    """ Represents ambient temperature database access """

    INSERT_QUERY = 'INSERT INTO ambient_temperatures(temperature, date_time) VALUES(%s, %s)'
    DATA_QUERY = 'SELECT * FROM ambient_temperatures FETCH FIRST ROW ONLY'

    def __init__(self, server, database, user, password):
        super(AmbientTemperatureDao, self).__init__(server=server,
                                                    database=database,
                                                    user=user,
                                                    password=password)

    def _get_query(self):
        return self.INSERT_QUERY

    def _get_parameters(self, values):
        return values[0], datetime.now()

    def _get_health_check_query(self):
        return self.DATA_QUERY
