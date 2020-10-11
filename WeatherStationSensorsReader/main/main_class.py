import logging


class Main(object):
    """Represents the main class when the app is started"""

    # Environment variables
    HEALTH_CHECK_VARIABLE = 'HEALTH_CHECK'
    LOGGING_LEVEL_VARIABLE = 'LOGGING_LEVEL'

    FAKE_SENSOR_VARIABLE = 'FAKE_SENSOR'
    BME_280_SENSOR_VARIABLE = 'BME_280_SENSOR'
    GROUND_SENSOR_VARIABLE = 'GROUND_SENSOR'
    RAINFALL_SENSOR_VARIABLE = 'RAINFALL_SENSOR'
    WIND_SENSOR_VARIABLE = 'WIND_SENSOR'

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
            self._check_bool_value(self.HEALTH_CHECK_VARIABLE)

        if self.LOGGING_LEVEL_VARIABLE in self.variables:
            self._check_in_expected_values(self.LOGGING_LEVEL_VARIABLE, self.LOGGING_LEVELS)

    def _check_bool_value(self, variable_name):
        value = self.variables[variable_name]

        if value != 'true' and value != 'false':
            raise ValueError(f'"{value}" is not a valid boolean value')

    def _check_in_expected_values(self, variable_name, expected_values):
        value = self.variables[variable_name]

        if value not in expected_values:
            raise ValueError(f'"{value}" is not in the expected values "{expected_values}"')

    def validate_sensors_variables(self):
        if self.FAKE_SENSOR_VARIABLE in self.variables:
            self._check_bool_value(self.FAKE_SENSOR_VARIABLE)

        if self.BME_280_SENSOR_VARIABLE in self.variables:
            self._check_bool_value(self.BME_280_SENSOR_VARIABLE)

        if self.GROUND_SENSOR_VARIABLE in self.variables:
            self._check_bool_value(self.GROUND_SENSOR_VARIABLE)

        if self.RAINFALL_SENSOR_VARIABLE in self.variables:
            self._check_bool_value(self.RAINFALL_SENSOR_VARIABLE)

        if self.WIND_SENSOR_VARIABLE in self.variables:
            self._check_bool_value(self.WIND_SENSOR_VARIABLE)

    def validate_database_variables(self):
        if self.SERVER_VARIABLE in self.variables:
            self._check_not_null_value(self.SERVER_VARIABLE)

        if self.DATABASE_VARIABLE in self.variables:
            self._check_not_null_value(self.DATABASE_VARIABLE)

        if self.USER_VARIABLE in self.variables:
            self._check_not_null_value(self.USER_VARIABLE)

        if self.PASSWORD_VARIABLE in self.variables:
            self._check_not_null_value(self.PASSWORD_VARIABLE)

    def _check_not_null_value(self, variable_name):
        value = self.variables[variable_name]

        if not value:
            raise ValueError(f'"{value}" is not a valid boolean value')

    def configure_logging(self):
        logging.basicConfig(level=self.variables[self.LOGGING_LEVEL_VARIABLE], format=Main.LOG_FORMAT)
