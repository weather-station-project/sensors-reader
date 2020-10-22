import logging
import os
import sys
from time import sleep

from main.main_class import Main


def configure_default_logging():
    logging.basicConfig(level=logging.ERROR, format=Main.LOG_FORMAT)


if __name__ == '__main__':
    try:
        configure_default_logging()

        main = Main(variables=os.environ)
        main.validate_environment_variables()
        main.configure_logging()

        controllers_enabled = main.get_controllers_enabled()

        if not controllers_enabled:
            raise Exception('There is no controller configured on the init. Please, read the documentation available on Github.')

        seconds_between_reads = main.get_minutes_between_reads() * 60
        while True:
            main.execute_controllers(controllers=controllers_enabled)

            logging.debug(f'Sleeping "{seconds_between_reads}" seconds.')
            sleep(seconds_between_reads)
    except Exception as e:
        logging.critical(e)
        sys.exit(1)

    sys.exit(0)
