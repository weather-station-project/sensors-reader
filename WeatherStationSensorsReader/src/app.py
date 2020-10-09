import sys
import os

from src.main.main_class import Main

if __name__ == '__main__':
    main = Main(os.environ)

    try:
        main.validate_environment_variables()
    except ValueError as e:
        pass

    # Sensors initialization
    # db class initialization
    # Logging initialization?

    sys.exit(0)
