class Main(object):
    """Represents the main class then the app is started"""

    HEALTH_CHECK_VARIABLE = 'HEALTH_CHECK'

    FAKE_SENSOR_VARIABLE = 'FAKE_SENSOR'
    BME_280_SENSOR_VARIABLE = 'BME_280_SENSOR'
    GROUND_SENSOR_VARIABLE = 'GROUND_SENSOR'
    RAINFALL_SENSOR_VARIABLE = 'RAINFALL_SENSOR'
    WIND_SENSOR_VARIABLE = 'WIND_SENSOR'

    SERVER_VARIABLE = 'SERVER'
    DATABASE_VARIABLE = 'DATABASE'
    USER_VARIABLE = 'USER'
    PASSWORD_VARIABLE = 'PASSWORD'

    def __init__(self, variables):
        self.variables = variables

    def validate_environment_variables(self):
        self.validate_generic_variables()
        self.validate_sensors_variables()
        self.validate_database_variables()

    def validate_generic_variables(self):
        if self.HEALTH_CHECK_VARIABLE in self.variables:
            self._check_bool_value(self.HEALTH_CHECK_VARIABLE)

    def _check_bool_value(self, variable_name):
        value = self.variables[variable_name]

        if value != 'true' and value != 'false':
            raise ValueError(value)

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
            raise ValueError(value)
