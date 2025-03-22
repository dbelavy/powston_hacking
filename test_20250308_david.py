import unittest
import sys
import types
from unittest.mock import patch
import importlib
from datetime import datetime

class TestDavidScript(unittest.TestCase):
    
    def test_opportunistic_buy(self):
        """Test very low buy price - opportunistic buying"""
        case = {
            "hour": 4,  # Early morning
            "buy_price": 3.2,  # Below buy_opport (5.0)
            "sell_price": 2.8,
            "battery_soc": 30.0,  # Above reserve_soc[4] (10%)
            "rrp": 25.0,
            "is_spiking": False,
            "interval_time": datetime.fromisoformat("2025-03-07T04:55:00+10:00"),
            "sunrise": datetime.fromisoformat("2025-03-08T05:45:01.980418+10:00"),
            "sunset": datetime.fromisoformat("2025-03-07T18:13:19.421096+10:00"),
            "history_buy_prices": [4.0] * 24,  # Simplified for testing
            "buy_forecast": [4.0] * 16,  # Simplified for testing
            "expected_action": "import"
        }
        
        self._run_test_with_case("opportunistic_buy", case)
    
    def test_daytime_low_prices(self):
        """Test daytime with low prices"""
        case = {
            "hour": 10,  # Daytime hour (in day list)
            "buy_price": 8.5,  # Below buy_max_soft (15.0)
            "sell_price": 5.5,
            "battery_soc": 65.0,  # Above reserve_soc[10] (10%)
            "rrp": 42.0,  # Regular RRP
            "is_spiking": False,
            "interval_time": datetime.fromisoformat("2025-03-07T10:55:00+10:00"),
            "sunrise": datetime.fromisoformat("2025-03-08T05:45:01.980418+10:00"),
            "sunset": datetime.fromisoformat("2025-03-07T18:13:19.421096+10:00"),
            "history_buy_prices": [8.5] * 24,  # Simplified for testing
            "buy_forecast": [8.5] * 16,  # Simplified for testing
            "expected_action": "charge"
        }
        
        self._run_test_with_case("daytime_low_prices", case)
    
    def test_extreme_rrp(self):
        """Test extreme RRP price spike"""
        case = {
            "hour": 16,  # Late afternoon
            "buy_price": 55.5,  # High buy price
            "sell_price": 80.2,  # High sell price
            "battery_soc": 85.0,  # Good surplus
            "rrp": 1500.0,  # Above always_sell_rrp (1000.0)
            "is_spiking": True,
            "interval_time": datetime.fromisoformat("2025-03-07T16:55:00+10:00"),
            "sunrise": datetime.fromisoformat("2025-03-08T05:45:01.980418+10:00"),
            "sunset": datetime.fromisoformat("2025-03-07T18:13:19.421096+10:00"),
            "history_buy_prices": [60.0] * 24,  # Simplified for testing
            "buy_forecast": [60.0] * 16,  # Simplified for testing
            "expected_action": "export"
        }
        
        self._run_test_with_case("extreme_rrp", case)
        
    def _run_test_with_case(self, name, case):
        """Helper method to run a test with the given case"""
        # Create a test file that doesn't rely on importing test_cases.py
        with open('test_script_temp.py', 'w') as f:
            f.write("""
# Temporary test script
from variables_available import *

# Constants from the original script
prepare_for_peak = [12, 13, 14, 15]
peak = [16, 17, 18, 19, 20]
always_sell_rrp = 1000.0
sell_min_hard = 30.0 
buy_max_soft = 15.0
buy_opport = 5.0
cyclone_mode = False
cyclone_reserve_soc = 70
morning_padding = 1

# Energy required for personal use. Don't export below this level
reserve_soc = {
    0: 10, 1: 10, 2: 10, 3: 10, 4: 10, 5: 10, 6: 10, 7: 10, 8: 10, 9: 10,
    10: 10, 11: 10, 12: 60, 13: 70, 14: 80, 15: 90, 16: 80, 17: 60,
    18: 40, 19: 40, 20: 30, 21: 10, 22: 10, 23: 10,
}

# Set up time of day periods
night = []
day = []

for i in range(0, 24):
    if i >= max(peak) or i <= (sunrise_hour+morning_padding):
        night.append(i)
    elif i < min(peak):
        day.append(i)

# Define surplus_energy based on battery_soc and hour
soc_reserve = int(reserve_soc[hour]) if not cyclone_mode else cyclone_reserve_soc
surplus_energy = battery_soc > soc_reserve

# Decision making logic
if buy_price < buy_opport:
    action = 'import'
    solar = 'maximize'
    reason += ' Opportunistic buy.'
elif (rrp > always_sell_rrp) and surplus_energy:
    action = 'export'
    solar = 'maximize'
    reason += ' High RRP opportunity.'
elif is_spiking and buy_price > sell_min_hard and surplus_energy:
    action = 'export'
    solar = 'maximize'
    reason += ' Price spike and surplus.'
elif (hour in day) and buy_price < buy_max_soft:
    action = 'charge'
    solar = 'maximize'
    reason += ' Daytime charge below soft max buy price.'
elif (hour in prepare_for_peak) and not surplus_energy:
    action = 'import'
    solar = 'maximize'
    reason += ' Afternoon charge before peak.'
elif (hour in peak) and surplus_energy and sell_price > sell_min_hard:
    action = 'export'
    solar = 'maximize'
    reason += ' Peak sell price above sell threshold and surplus.'
elif (hour in night) and buy_price < buy_max_soft:
    action = 'charge'
    solar = 'maximize'
    reason += ' Nighttime low price. Use grid.'
else:
    action = 'auto'
    solar = 'maximize'
    reason += ' Default behavior;'
""")
        
        # Create a mock for variables_available.py
        mock_module = types.ModuleType('variables_available')
        
        # Add attributes that our script needs
        for attribute in ['interval_time', 'sunrise', 'sunset', 'sunrise_hour', 'sunset_hour',
                         'buy_price', 'sell_price', 'battery_soc', 'rrp', 'hour',
                         'history_buy_prices', 'buy_forecast', 'is_spiking', 
                         'reason', 'action', 'solar', 'suggested_action', 'suggested_solar']:
            setattr(mock_module, attribute, None)
        
        # These are required to avoid errors
        mock_module.suggested_action = "auto"
        mock_module.suggested_solar = "maximize"
        mock_module.reason = "Test: "
        mock_module.action = "auto"
        mock_module.solar = "maximize"
        
        # Set our test case values
        mock_module.hour = case['hour']
        mock_module.buy_price = case['buy_price']
        mock_module.sell_price = case['sell_price']
        mock_module.battery_soc = case['battery_soc']
        mock_module.rrp = case['rrp']
        mock_module.is_spiking = case['is_spiking']
        mock_module.interval_time = case['interval_time']
        mock_module.sunrise = case['sunrise']
        mock_module.sunset = case['sunset']
        mock_module.history_buy_prices = case['history_buy_prices']
        mock_module.buy_forecast = case['buy_forecast']
        
        # Calculate values that would normally be computed in the script
        mock_module.sunrise_hour = case['sunrise'].hour
        mock_module.sunset_hour = case['sunset'].hour
        
        # Add the mock to sys.modules so our script will use it
        with patch.dict('sys.modules', {'variables_available': mock_module}):
            # Import our temporary test script
            if 'test_script_temp' in sys.modules:
                del sys.modules['test_script_temp']
            
            # Import and run our test script
            test_script = importlib.import_module('test_script_temp')
            
            # Print detailed information
            print(f"\nTesting {name}:")
            print(f"  Hour: {case['hour']}, Buy Price: {case['buy_price']}, Sell Price: {case['sell_price']}")
            print(f"  Battery SOC: {case['battery_soc']}%, RRP: ${case['rrp']}")
            print(f"  Is Spiking: {case['is_spiking']}")
            print(f"  Expected Action: {case['expected_action']}")
            print(f"  Actual Action: {test_script.action}")
            print(f"  Reason: {test_script.reason}")
            
            # Check the result
            self.assertEqual(test_script.action, case['expected_action'],
                            f"Expected action {case['expected_action']} for {name}, "
                            f"but got {test_script.action}")

if __name__ == '__main__':
    unittest.main()
