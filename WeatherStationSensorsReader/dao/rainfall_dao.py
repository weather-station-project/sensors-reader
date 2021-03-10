from datetime import datetime

from dao.dao import Dao


class RainfallDao(Dao):
    """ Represents the rainfall database access """

    INSERT_QUERY = 'INSERT INTO rainfall(amount, date_time) VALUES(%s, %s)'

    def get_query(self):
        return self.INSERT_QUERY

    def get_parameters(self, values):
        return values[0], datetime.now()
