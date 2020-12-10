from controllers.controller import Controller
from dao.ground_temperature_dao import GroundTemperatureDao
from sensors.ground_temperature_sensor import GroundTemperatureSensor


class AmbientTemperatureController(Controller):
    """ Represents the controller with the ground temperature sensor and DAO """

    def __init__(self, server, database, user, password):
        super(AmbientTemperatureController, self).__init__(sensor=GroundTemperatureSensor(), dao=GroundTemperatureDao(server=server,
                                                                                                                      database=database,
                                                                                                                      user=user,
                                                                                                                      password=password))
