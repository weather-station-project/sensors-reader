import logging
import os
import sys

from main.main_class import Main


def configure_logging_critical_level():
    logging.basicConfig(level=logging.CRITICAL, format=Main.LOG_FORMAT)


def main():
    try:
        configure_logging_critical_level()

        main_class = Main(variables=os.environ)
        main_class.validate_environment_variables()

        controllers_enabled = main_class.get_controllers_enabled()

        if not controllers_enabled:
            raise Exception('There is no controller configured on the init. Please, read the documentation available on Github.')

        main_class.execute_controllers_health_check(controllers=controllers_enabled)
    except Exception as e:
        logging.critical(e, exc_info=True)
        return 1

    return 0


if __name__ == '__main__':
    sys.exit(main())
