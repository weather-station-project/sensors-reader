import logging

import psycopg2


class Dao(object):
    """Base class for DAOs"""

    def __init__(self, server, database, user, password):
        self.server = server
        self.database = database
        self.user = user
        self.password = password

    def insert(self, values):
        if not self.server:
            logging.warning(msg='Database connection not configured, the data will not be stored anywhere.')
            return

        try:
            with psycopg2.connect(host=self.server,
                                  database=self.database,
                                  user=self.user,
                                  password=self.password) as conn:
                with conn.cursor() as cursor:
                    sql_query = self._get_query()
                    query_parameter_values = self._get_parameters(values)

                    cursor.execute(sql_query, query_parameter_values)

                    logging.debug(f'Executed query "{sql_query}" with values {query_parameter_values}.')
        except Exception as e:
            raise Exception(f'Error in DAO "{self.__class__.__name__} while executing the query "{sql_query}" with values {query_parameter_values}. ',
                            e)

    def _get_query(self):
        raise NotImplementedError('A sub-class must be implemented.')

    def _get_parameters(self, values):
        raise NotImplementedError('A sub-class must be implemented.')
