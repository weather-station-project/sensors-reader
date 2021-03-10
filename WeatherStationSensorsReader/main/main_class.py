import logging

from controllers.air_measurement_controller import AirMeasurementController
from controllers.ambient_temperature_controller import AmbientTemperatureController
from controllers.fake_controller import FakeController
from controllers.ground_temperature_controller import GroundTemperatureController
from controllers.rainfall_controller import RainfallController
from controllers.wind_measurement_controller import WindMeasurementController
from exceptions.dao_exception import DaoException
from exceptions.sensor_exception import SensorException
from health_check.health_check_file_manager import register_error_in_health_check_file, APP_KEY


class Main(object):
    """Represents the main class when the app is started"""

    # Environment variables
    LOGGING_LEVEL_VARIABLE = 'LOGGING_LEVEL'
    MINUTES_BETWEEN_READS_VARIABLE = 'MINUTES_BETWEEN_READS'

    FAKE_SENSOR_VARIABLE = 'FAKE_SENSOR_ENABLED'
    BME_280_SENSOR_VARIABLE = 'BME_280_SENSOR_ENABLED'
    GROUND_SENSOR_VARIABLE = 'GROUND_SENSOR_ENABLED'
    RAINFALL_SENSOR_VARIABLE = 'RAINFALL_SENSOR_ENABLED'
    WIND_SENSOR_VARIABLE = 'WIND_SENSOR_ENABLED'

    ANEMOMETER_PORT_NUMBER_VARIABLE = 'ANEMOMETER_PORT_NUMBER'
    RAIN_GAUGE_PORT_NUMBER_VARIABLE = 'RAIN_GAUGE_PORT_NUMBER'

    SERVER_VARIABLE = 'SERVER'
    DATABASE_VARIABLE = 'DATABASE'
    USER_VARIABLE = 'USER'
    PASSWORD_VARIABLE = 'PASSWORD'

    # LOGGING CONSTANTS
    LOGGING_LEVELS = {'CRITICAL': logging.CRITICAL,
                      'ERROR': logging.ERROR,
                      'WARNING': logging.WARNING,
                      'INFO': logging.INFO,
                      'DEBUG': logging.DEBUG}
    LOG_FORMAT = '%(asctime)s - %(levelname)s - %(message)s'

    # DEFAULT VALUES
    DEFAULT_MINUTES_BETWEEN_READS = 5
    DEFAULT_ANEMOMETER_PORT_NUMBER = 22
    DEFAULT_RAIN_GAUGE_PORT_NUMBER = 22

    def __init__(self, variables):
        self.variables = variables

    def validate_environment_variables(self):
        self.validate_generic_variables()
        self.validate_sensors_variables()
        self.validate_database_variables()

    def validate_generic_variables(self):
        if self.LOGGING_LEVEL_VARIABLE in self.variables:
            self.check_in_expected_values(variable_name=self.LOGGING_LEVEL_VARIABLE, expected_values=self.LOGGING_LEVELS.keys())

        if self.MINUTES_BETWEEN_READS_VARIABLE in self.variables:
            self.check_positive_integer_value(variable_name=self.MINUTES_BETWEEN_READS_VARIABLE)

    def check_bool_value(self, variable_name):
        value = self.variables[variable_name]

        if value != 'true' and value != 'false':
            raise ValueError(f'"{value}" is not a valid boolean value.')

    def check_in_expected_values(self, variable_name, expected_values):
        value = self.variables[variable_name]

        if value not in expected_values:
            raise ValueError(f'"{value}" is not in the expected values "{expected_values}".')

    def check_positive_integer_value(self, variable_name):
        value = self.variables[variable_name]

        try:
            val = int(value)
            if val < 0:
                raise ValueError
        except ValueError:
            raise ValueError(f'"{value}" is not a valid positive integer.')

    def validate_sensors_variables(self):
        if self.FAKE_SENSOR_VARIABLE in self.variables:
            self.check_bool_value(variable_name=self.FAKE_SENSOR_VARIABLE)

        if self.BME_280_SENSOR_VARIABLE in self.variables:
            self.check_bool_value(variable_name=self.BME_280_SENSOR_VARIABLE)

        if self.GROUND_SENSOR_VARIABLE in self.variables:
            self.check_bool_value(variable_name=self.GROUND_SENSOR_VARIABLE)

        if self.RAINFALL_SENSOR_VARIABLE in self.variables:
            self.check_bool_value(variable_name=self.RAINFALL_SENSOR_VARIABLE)

        if self.WIND_SENSOR_VARIABLE in self.variables:
            self.check_bool_value(variable_name=self.WIND_SENSOR_VARIABLE)

        if self.ANEMOMETER_PORT_NUMBER_VARIABLE in self.variables:
            self.check_positive_integer_value(variable_name=self.ANEMOMETER_PORT_NUMBER_VARIABLE)

        if self.RAIN_GAUGE_PORT_NUMBER_VARIABLE in self.variables:
            self.check_positive_integer_value(variable_name=self.RAIN_GAUGE_PORT_NUMBER_VARIABLE)

    def validate_database_variables(self):
        if self.SERVER_VARIABLE in self.variables:
            self.check_not_null_value(variable_name=self.SERVER_VARIABLE)

        if self.DATABASE_VARIABLE in self.variables:
            self.check_not_null_value(variable_name=self.DATABASE_VARIABLE)

        if self.USER_VARIABLE in self.variables:
            self.check_not_null_value(variable_name=self.USER_VARIABLE)

        if self.PASSWORD_VARIABLE in self.variables:
            self.check_not_null_value(variable_name=self.PASSWORD_VARIABLE)

    def check_not_null_value(self, variable_name):
        value = self.variables[variable_name]

        if not value:
            raise ValueError(f'"{value}" is not a valid boolean value.')

    def configure_logging(self):
        if self.LOGGING_LEVEL_VARIABLE not in self.variables:
            return

        for handler in logging.root.handlers[:]:
            logging.root.removeHandler(hdlr=handler)

        level_value = self.variables[self.LOGGING_LEVEL_VARIABLE]
        logging.basicConfig(level=self.LOGGING_LEVELS[level_value], format=self.LOG_FORMAT)

    def get_controllers_enabled(self):
        server = self.variables[self.SERVER_VARIABLE] if self.SERVER_VARIABLE in self.variables else None
        database = self.variables[self.DATABASE_VARIABLE] if self.DATABASE_VARIABLE in self.variables else None
        user = self.variables[self.USER_VARIABLE] if self.USER_VARIABLE in self.variables else None
        password = self.variables[self.PASSWORD_VARIABLE] if self.PASSWORD_VARIABLE in self.variables else None
        controllers = []

        if self.is_controller_enabled(self.FAKE_SENSOR_VARIABLE):
            controllers.append(FakeController(server=server, database=database, user=user, password=password))
            # When the fake controller is enabled, it will be the only one working
            return controllers

        if self.is_controller_enabled(self.BME_280_SENSOR_VARIABLE):
            controllers.append(AmbientTemperatureController(server=server, database=database, user=user, password=password))
            controllers.append(AirMeasurementController(server=server, database=database, user=user, password=password))

        if self.is_controller_enabled(self.GROUND_SENSOR_VARIABLE):
            controllers.append(GroundTemperatureController(server=server, database=database, user=user, password=password))

        if self.is_controller_enabled(self.WIND_SENSOR_VARIABLE):
            controllers.append(
                WindMeasurementController(anemometer_port_number=self.get_value_as_int(variable_name=self.ANEMOMETER_PORT_NUMBER_VARIABLE,
                                                                                       default_value=self.DEFAULT_ANEMOMETER_PORT_NUMBER),
                                          server=server,
                                          database=database,
                                          user=user,
                                          password=password))
        if self.is_controller_enabled(self.RAINFALL_SENSOR_VARIABLE):
            controllers.append(RainfallController(rain_gauge_port_number=self.get_value_as_int(variable_name=self.RAIN_GAUGE_PORT_NUMBER_VARIABLE,
                                                                                               default_value=self.DEFAULT_RAIN_GAUGE_PORT_NUMBER),
                                                  server=server,
                                                  database=database,
                                                  user=user,
                                                  password=password))

        return controllers

    def is_controller_enabled(self, variable_name):
        return variable_name in self.variables and self.variables[variable_name] == 'true'

    def get_value_as_int(self, variable_name, default_value):
        if variable_name in self.variables:
            return int(self.variables[variable_name])

        return default_value

    @staticmethod
    def execute_controllers(controllers):
        for controller in controllers:
            try:
                controller.execute()
            except (DaoException, SensorException) as e:
                logging.error(e, exc_info=True)
                register_error_in_health_check_file(key=e.class_name, message=repr(e))
            except Exception as e:
                logging.exception(f'Error while executing controller "{controller.__class__.__name__}".')
                register_error_in_health_check_file(key=APP_KEY, message=repr(e))
