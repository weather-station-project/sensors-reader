from dao.dao import Dao


class FakeDao(Dao):
    """ Class to fake the database access """

    def __init__(self, server, database, user, password):
        super(FakeDao, self).__init__(server=server,
                                      database=database,
                                      user=user,
                                      password=password)

    def _get_query(self):
        pass

    def _get_parameters(self, values):
        pass
