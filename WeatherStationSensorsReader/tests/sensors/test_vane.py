import sys
import unittest
from unittest import mock
from unittest.mock import MagicMock

sys.modules['MCP342X'] = MagicMock()
from sensors.vane import Vane


class TestVane(unittest.TestCase):
    @mock.patch('sensors.vane.MCP342X')
    @mock.patch('sensors.vane.Vane.fill_adc_field')
    @mock.patch('sensors.vane.Vane.fill_min_max_adc')
    def setUp(self, mock_fill_min_max_adc, mock_fill_adc_field, mock_mcp):
        self.test_vane = Vane()

    @mock.patch('sensors.vane.MCP342X')
    @mock.patch('sensors.vane.Vane.fill_adc_field')
    @mock.patch('sensors.vane.Vane.fill_min_max_adc')
    @mock.patch('sensors.vane.logging')
    def test_when_calling_constructor_expected_values_should_be_returned(self,
                                                                         mock_logging,
                                                                         mock_fill_min_max_adc,
                                                                         mock_fill_adc_field,
                                                                         mock_mcp):
        # act
        self.assertIsNotNone(Vane())

        # assert
        mock_fill_min_max_adc.assert_called_once()
        mock_fill_adc_field.assert_called_once()
        mock_mcp.assert_called_once()
        mock_logging.debug.assert_called_once_with(msg=f'Started vane on port "{self.test_vane.ADDRESS}"'
                                                       f' in the sensor "{self.test_vane.__class__.__name__}".')

    def test_when_filling_adc_fields_expected_values_should_be_returned(self):
        # arrange
        mock_adc = MagicMock()
        mock_adc.max = 1
        mock_adc.vref = 1

        self.test_vane.adc = mock_adc
        self.test_vane.calculate_voltage_out = MagicMock(return_value=1)

        # act
        self.assertIsNone(self.test_vane.fill_adc_field())

        # arrange
        for item in self.test_vane.VANE_ANGLES_AND_DIRECTIONS_TABLE:
            self.test_vane.calculate_voltage_out.assert_any_call(r2=item['ohms'])
            self.assertEqual(item['adc'], 1)


if __name__ == '__main__':
    unittest.main()
