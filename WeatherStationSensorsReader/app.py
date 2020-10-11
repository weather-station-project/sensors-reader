import logging
import os
import sys

from main.main_class import Main


def configure_default_logging():
    logging.basicConfig(level=logging.ERROR, format=Main.LOG_FORMAT)


if __name__ == '__main__':
    try:
        configure_default_logging()

        main = Main(os.environ)
        main.validate_environment_variables()
        main.configure_logging()
    except ValueError as e:
        logging.critical(e)
        pass

    # Sensors initialization
    # db class initialization
    # Logging initialization?

    sys.exit(0)
