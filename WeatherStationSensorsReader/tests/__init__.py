import sys
from unittest.mock import MagicMock

sys.modules['bme280pi'] = MagicMock()