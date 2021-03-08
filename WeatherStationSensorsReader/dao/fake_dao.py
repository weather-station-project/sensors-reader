from datetime import datetime

from dao.dao import Dao


class FakeDao(Dao):
    """ Represents the fake the database access """

    QUERY = 'SELECT 1'

    def get_query(self):
        return self.QUERY

    def get_parameters(self, values):
        return values, datetime.now()
