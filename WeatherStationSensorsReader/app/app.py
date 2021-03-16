import logging
import os
import sys
from time import sleep

from health_check.health_check_file_manager import APP_KEY, register_error_in_health_check_file, erase_health_check_file
from main.main_class import Main


def configure_default_logging():
    logging.basicConfig(level=logging.ERROR, format=Main.LOG_FORMAT)


def get_true():
    # Stupid method for unit tests purposes to avoid infinite loop
    return True


def main():
    try:
        erase_health_check_file()

        configure_default_logging()

        main_class = Main(variables=os.environ)
        main_class.validate_environment_variables()
        main_class.configure_logging()

        controllers_enabled = main_class.get_controllers_enabled()

        if not controllers_enabled:
            raise Exception('There is no controller configured on the init. Please, read the documentation available on Github.')

        seconds_between_readings = main_class.get_value_as_int(variable_name=main_class.MINUTES_BETWEEN_READINGS_VARIABLE,
                                                               default_value=main_class.DEFAULT_MINUTES_BETWEEN_READINGS) * 60
        while get_true():
            logging.debug(msg=f'Sleeping "{seconds_between_readings}" seconds while sensors are doing readings.')
            sleep(seconds_between_readings)

            main_class.execute_controllers(controllers=controllers_enabled)
    except Exception as e:
        logging.critical(e)
        register_error_in_health_check_file(key=APP_KEY, message=repr(e))
        return 1

    return 0


if __name__ == '__main__':
    sys.exit(main())
