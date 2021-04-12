from controllers.controller import Controller
from dao.rainfall_dao import RainfallDao
from sensors.rainfall_sensor import RainfallSensor


class RainfallController(Controller):
    """ Represents the controller with the rainfall measurement sensor and DAO """

    def __init__(self, rain_gauge_port_number, server, database, user, password):
        super(RainfallController, self).__init__(sensor=RainfallSensor(rain_gauge_port_number=rain_gauge_port_number),
                                                 dao=RainfallDao(server=server,
                                                                 database=database,
                                                                 user=user,
                                                                 password=password))
