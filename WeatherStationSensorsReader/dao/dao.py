import logging
from abc import ABC, abstractmethod

import psycopg2

from exceptions.dao_exception import DaoException
from health_check.health_check_file_manager import register_success_for_class_into_health_check_file


class Dao(ABC):
    """Base class for DAOs"""

    def __init__(self, server, database, user, password):
        self.server = server
        self.database = database
        self.user = user
        self.password = password

    def insert(self, values):
        dao_name = self.__class__.__name__

        if not self.server:
            logging.warning(msg='Database connection not configured, the data will not be stored anywhere.')
            return

        try:
            sql_query = self.get_query()
            query_parameter_values = self.get_parameters(values=values)
            with psycopg2.connect(host=self.server,
                                  database=self.database,
                                  user=self.user,
                                  password=self.password) as conn:
                with conn.cursor() as cursor:
                    cursor.execute(query=sql_query, vars=query_parameter_values)

            logging.debug(msg=f'Executed query "{sql_query}" with values "{query_parameter_values}".')
            register_success_for_class_into_health_check_file(class_name=dao_name)
        except Exception as e:
            raise DaoException(class_name=dao_name,
                               message=f'Error in DAO "{dao_name}" while executing the query '
                                       f'"{sql_query}" with values {query_parameter_values}. ') from e

    @abstractmethod
    def get_query(self):
        raise NotImplementedError()

    @abstractmethod
    def get_parameters(self, values):
        raise NotImplementedError()
