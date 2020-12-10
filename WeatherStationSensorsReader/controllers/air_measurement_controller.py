from controllers.controller import Controller
from dao.air_measurement_dao import AirMeasurementDao
from sensors.air_measurement_sensor import AirMeasurementSensor


class AirMeasurementController(Controller):
    """ Represents the controller with the air measurement sensor and DAO """

    def __init__(self, server, database, user, password):
        super(AirMeasurementController, self).__init__(sensor=AirMeasurementSensor(), dao=AirMeasurementDao(server=server,
                                                                                                            database=database,
                                                                                                            user=user,
                                                                                                            password=password))
