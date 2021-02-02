from controllers.controller import Controller
from dao.wind_measurement_dao import WindMeasurementDao
from sensors.wind_measurement_sensor import WindMeasurementSensor


class WindMeasurementController(Controller):
    """ Represents the controller with the wind measurement sensor and DAO """

    def __init__(self, anemometer_port_number, server, database, user, password):
        super(WindMeasurementController, self).__init__(sensor=WindMeasurementSensor(anemometer_port_number=anemometer_port_number),
                                                        dao=WindMeasurementDao(server=server,
                                                                               database=database,
                                                                               user=user,
                                                                               password=password))
