import logging

from controllers.fake_controller import FakeController


class Main(object):
    """Represents the main class when the app is started"""

    # Environment variables
    HEALTH_CHECK_VARIABLE = 'HEALTH_CHECK'
    LOGGING_LEVEL_VARIABLE = 'LOGGING_LEVEL'
    MINUTES_BETWEEN_READS_VARIABLE = 'MINUTES_BETWEEN_READS'

    FAKE_SENSOR_VARIABLE = 'FAKE_SENSOR_ENABLED'
    BME_280_SENSOR_VARIABLE = 'BME_280_SENSOR_ENABLED'
    GROUND_SENSOR_VARIABLE = 'GROUND_SENSOR_ENABLED'
    RAINFALL_SENSOR_VARIABLE = 'RAINFALL_SENSOR_ENABLED'
    WIND_SENSOR_VARIABLE = 'WIND_SENSOR_ENABLED'

    SERVER_VARIABLE = 'SERVER'
    DATABASE_VARIABLE = 'DATABASE'
    USER_VARIABLE = 'USER'
    PASSWORD_VARIABLE = 'PASSWORD'

    # LOGGING CONSTANTS
    LOGGING_LEVELS = {'CRITICAL', 'ERROR', 'WARNING', 'INFO', 'DEBUG'}
    LOG_FORMAT = '%(asctime)s - %(levelname)s - %(message)s'

    def __init__(self, variables):
        self.variables = variables

    def validate_environment_variables(self):
        self.validate_generic_variables()
        self.validate_sensors_variables()
        self.validate_database_variables()

    def validate_generic_variables(self):
        if self.HEALTH_CHECK_VARIABLE in self.variables:
            self._check_bool_value(variable_name=self.HEALTH_CHECK_VARIABLE)

        if self.LOGGING_LEVEL_VARIABLE in self.variables:
            self._check_in_expected_values(variable_name=self.LOGGING_LEVEL_VARIABLE, expected_values=self.LOGGING_LEVELS)

        if self.MINUTES_BETWEEN_READS_VARIABLE in self.variables:
            self._check_integer_value(variable_name=self.MINUTES_BETWEEN_READS_VARIABLE)

    def _check_bool_value(self, variable_name):
        value = self.variables[variable_name]

        if value != 'true' and value != 'false':
            raise ValueError(f'"{value}" is not a valid boolean value.')

    def _check_in_expected_values(self, variable_name, expected_values):
        value = self.variables[variable_name]

        if value not in expected_values:
            raise ValueError(f'"{value}" is not in the expected values "{expected_values}".')

    def _check_integer_value(self, variable_name):
        value = self.variables[variable_name]

        try:
            val = int(value)
            if val < 0:
                raise ValueError
        except ValueError:
            raise ValueError(f'"{value}" is not a valid positive integer.')

    def validate_sensors_variables(self):
        if self.FAKE_SENSOR_VARIABLE in self.variables:
            self._check_bool_value(variable_name=self.FAKE_SENSOR_VARIABLE)

        if self.BME_280_SENSOR_VARIABLE in self.variables:
            self._check_bool_value(variable_name=self.BME_280_SENSOR_VARIABLE)

        if self.GROUND_SENSOR_VARIABLE in self.variables:
            self._check_bool_value(variable_name=self.GROUND_SENSOR_VARIABLE)

        if self.RAINFALL_SENSOR_VARIABLE in self.variables:
            self._check_bool_value(variable_name=self.RAINFALL_SENSOR_VARIABLE)

        if self.WIND_SENSOR_VARIABLE in self.variables:
            self._check_bool_value(variable_name=self.WIND_SENSOR_VARIABLE)

    def validate_database_variables(self):
        if self.SERVER_VARIABLE in self.variables:
            self._check_not_null_value(variable_name=self.SERVER_VARIABLE)

        if self.DATABASE_VARIABLE in self.variables:
            self._check_not_null_value(variable_name=self.DATABASE_VARIABLE)

        if self.USER_VARIABLE in self.variables:
            self._check_not_null_value(variable_name=self.USER_VARIABLE)

        if self.PASSWORD_VARIABLE in self.variables:
            self._check_not_null_value(variable_name=self.PASSWORD_VARIABLE)

    def _check_not_null_value(self, variable_name):
        value = self.variables[variable_name]

        if not value:
            raise ValueError(f'"{value}" is not a valid boolean value.')

    def configure_logging(self):
        logging.basicConfig(level=self.variables[self.LOGGING_LEVEL_VARIABLE], format=Main.LOG_FORMAT)

    def get_controllers_enabled(self):
        controllers = []

        if self.FAKE_SENSOR_VARIABLE in self.variables and self.variables[self.FAKE_SENSOR_VARIABLE] == 'true':
            controllers.append(FakeController(server=self.variables[self.SERVER_VARIABLE],
                                              database=self.variables[self.DATABASE_VARIABLE],
                                              user=self.variables[self.USER_VARIABLE],
                                              password=self.variables[self.PASSWORD_VARIABLE]))
            # When the fake controller is enabled, it will be the only one working
            return controllers
        # TODO Add more controllers!

    def get_minutes_between_reads(self):
        return self.variables[self.MINUTES_BETWEEN_READS_VARIABLE]

    @staticmethod
    def execute_controllers(controllers):
        for controller in controllers:
            try:
                controller.execute()
            except Exception as e:
                logging.error(f'Error while executing controller "{controller.__class__.__name__}". ', e)
