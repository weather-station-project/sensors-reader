import logging
import os
import sys
from time import sleep

from main.main_class import Main


def configure_default_logging():
    logging.basicConfig(level=logging.ERROR, format=Main.LOG_FORMAT)


def get_true():
    # Stupid method for unit tests purposes to avoid infinite loop
    return True


def main():
    try:
        configure_default_logging()

        main_class = Main(variables=os.environ)
        main_class.validate_environment_variables()
        main_class.configure_logging()

        controllers_enabled = main_class.get_controllers_enabled()

        if not controllers_enabled:
            raise Exception('There is no controller configured on the init. Please, read the documentation available on Github.')

        seconds_between_reads = main_class.get_minutes_between_reads() * 60
        while get_true():
            main_class.execute_controllers(controllers=controllers_enabled)

            logging.debug(msg=f'Sleeping "{seconds_between_reads}" seconds.')
            sleep(seconds_between_reads)
    except Exception as e:
        logging.critical(e)
        return 1

    return 0


if __name__ == '__main__':
    sys.exit(main())
