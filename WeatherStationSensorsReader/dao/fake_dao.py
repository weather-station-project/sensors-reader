from datetime import datetime

from dao.dao import Dao


class FakeDao(Dao):
    """ Represents fake the database access """

    QUERY = 'SELECT 1'

    def __init__(self, server, database, user, password):
        super(FakeDao, self).__init__(server=server,
                                      database=database,
                                      user=user,
                                      password=password)

    def _get_query(self):
        return self.QUERY

    def _get_parameters(self, values):
        return values, datetime.now()

    def _get_health_check_query(self):
        return self.QUERY
