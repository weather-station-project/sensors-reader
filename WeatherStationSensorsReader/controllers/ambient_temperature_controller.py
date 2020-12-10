from controllers.controller import Controller
from dao.ambient_temperature_dao import AmbientTemperatureDao
from sensors.ambient_temperature_sensor import AmbientTemperatureSensor


class AmbientTemperatureController(Controller):
    """ Represents the controller with the ambient temperature sensor and DAO """

    def __init__(self, server, database, user, password):
        super(AmbientTemperatureController, self).__init__(sensor=AmbientTemperatureSensor(), dao=AmbientTemperatureDao(server=server,
                                                                                                                        database=database,
                                                                                                                        user=user,
                                                                                                                        password=password))
