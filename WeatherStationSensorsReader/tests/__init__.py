import sys
from unittest.mock import MagicMock

sys.modules['bme280pi'] = MagicMock()
sys.modules['w1thermsensor'] = MagicMock()
