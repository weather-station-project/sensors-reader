import logging
import sys

from health_check.health_check_file_manager import get_error_messages
from main.main_class import Main


def configure_logging_critical_level():
    logging.basicConfig(level=logging.CRITICAL, format=Main.LOG_FORMAT)


def main():
    try:
        configure_logging_critical_level()

        error_messages = get_error_messages()
        if error_messages:
            raise RuntimeError(f'Error in health check "{error_messages}".')
    except Exception as e:
        logging.critical(e, exc_info=True)
        return 1

    return 0


if __name__ == '__main__':
    sys.exit(main())
