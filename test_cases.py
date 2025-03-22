# Test Scenarios


test_cases = {
    "daytime_low_prices": {
        "description": "Daytime with low prices",
        "hour": 10,  # Daytime hour (in day list)
        "buy_price": 8.5,  # Below buy_max_soft (15.0)
        "sell_price": 5.5,
        "battery_soc": 65.0,  # Above reserve_soc[10] (10%)
        "rrp": 42.0,  # Regular RRP
        "is_spiking": False,
        "interval_time": datetime.fromisoformat("2025-03-07T10:55:00+10:00")
    },
    
    "daytime_high_prices": {
        "description": "Daytime with high prices",
        "hour": 11,  # Daytime hour
        "buy_price": 25.6,  # Above buy_max_soft (15.0)
        "sell_price": 15.2,  # Above sell_min_hard but not spiking
        "battery_soc": 70.0,  # Above reserve_soc[11] (10%)
        "rrp": 120.0,  # Higher RRP but below always_sell_rrp
        "is_spiking": False,
        "interval_time": datetime.fromisoformat("2025-03-07T11:55:00+10:00")
    },
    
    "peak_high_prices_high_surplus": {
        "description": "Peak with high prices and high surplus power",
        "hour": 18,  # Peak hour
        "buy_price": 45.5,  # High buy price
        "sell_price": 35.2,  # Above sell_min_hard (30.0)
        "battery_soc": 95.0,  # Well above reserve_soc[18] (40%)
        "rrp": 890.99,  # Very high RRP but below always_sell_rrp
        "is_spiking": True,
        "interval_time": datetime.fromisoformat("2025-03-07T18:55:00+10:00")
    },
    
    "peak_high_prices_low_surplus": {
        "description": "Peak with high prices but low surplus power",
        "hour": 17,  # Peak hour
        "buy_price": 48.2,  # High buy price
        "sell_price": 32.5,  # Above sell_min_hard (30.0)
        "battery_soc": 62.0,  # Just barely above reserve_soc[17] (60%)
        "rrp": 242.15,  # High RRP
        "is_spiking": True,
        "interval_time": datetime.fromisoformat("2025-03-07T17:55:00+10:00")
    },
    
    "peak_low_prices": {
        "description": "Peak with low prices",
        "hour": 19,  # Peak hour
        "buy_price": 20.5,  # Above buy_max_soft but low for peak
        "sell_price": 8.2,  # Below sell_min_hard (30.0)
        "battery_soc": 75.0,  # Above reserve_soc[19] (40%)
        "rrp": 95.0,  # Below typical peak values
        "is_spiking": False,
        "interval_time": datetime.fromisoformat("2025-03-07T19:55:00+10:00")
    },
    
    "night_high_prices": {
        "description": "Night with high prices",
        "hour": 23,  # Night hour
        "buy_price": 28.6,  # Above buy_max_soft (15.0)
        "sell_price": 18.2,  # Below sell_min_hard (30.0) but high
        "battery_soc": 45.0,  # Above reserve_soc[23] (10%)
        "rrp": 106.04,  # Regular night RRP
        "is_spiking": True,
        "interval_time": datetime.fromisoformat("2025-03-07T23:55:00+10:00")
    },
    
    "opportunistic_buy": {
        "description": "Very low buy price - opportunistic buying",
        "hour": 4,  # Early morning
        "buy_price": 3.2,  # Below buy_opport (5.0)
        "sell_price": 2.8,
        "battery_soc": 30.0,  # Above reserve_soc[4] (10%)
        "rrp": 25.0,
        "is_spiking": False,
        "interval_time": datetime.fromisoformat("2025-03-07T04:55:00+10:00")
    },
    
    "extreme_rrp": {
        "description": "Extreme RRP price spike",
        "hour": 16,  # Late afternoon
        "buy_price": 55.5,  # High buy price
        "sell_price": 80.2,  # High sell price
        "battery_soc": 85.0,  # Good surplus
        "rrp": 1500.0,  # Above always_sell_rrp (1000.0)
        "is_spiking": True,
        "interval_time": datetime.fromisoformat("2025-03-07T16:55:00+10:00")
    }
}

def run_test(test_name):
    """Run a specific test scenario"""
    global hour, buy_price, sell_price, battery_soc, rrp, is_spiking, interval_time
    
    # Reset all variables to their original values
    # This would be where you'd restore your base variables
    
    # Apply the test case
    test = test_cases[test_name]
    print(f"\nRunning test: {test['description']}")
    
    # Override variables with test values
    hour = test["hour"]
    buy_price = test["buy_price"]
    sell_price = test["sell_price"]
    battery_soc = test["battery_soc"]
    rrp = test["rrp"]
    is_spiking = test["is_spiking"]
    interval_time = test["interval_time"]
    
    # Here you would run your decision-making logic
    # And then print the results
    
    # For example:
    # [Your decision logic here]
    
    print(f"Hour: {hour}")
    print(f"Buy price: {buy_price}")
    print(f"Sell price: {sell_price}")
    print(f"Battery SOC: {battery_soc}")
    print(f"RRP: {rrp}")
    print(f"Is spiking: {is_spiking}")
    print(f"Result - Action: {action}, Solar: {solar}")
    print(f"Reason: {reason}")

# Run a specific test
# run_test("daytime_low_prices")

# Or run all tests
# for test_name in test_cases:
#     run_test(test_name)




def run_all_tests():
    """Run all test cases and display results"""
    # Store original values
    original_values = {
        "hour": hour,
        "buy_price": buy_price, 
        "sell_price": sell_price,
        "battery_soc": battery_soc,
        "rrp": rrp,
        "interval_time": interval_time,
        # Add other variables you need to preserve
    }
    
    results = {}
    
    # Run each test case
    for test_name, test_case in test_cases.items():
        print(f"\n=== Testing: {test_case['description']} ===")
        
        # Set test variables
        global hour, buy_price, sell_price, battery_soc, rrp, is_spiking, interval_time
        global action, solar, reason, forecast, sunrise, sunset
        
        hour = test_case["hour"]
        buy_price = test_case["buy_price"]
        sell_price = test_case["sell_price"]
        battery_soc = test_case["battery_soc"]
        rrp = test_case["rrp"]
        is_spiking = test_case["is_spiking"]
        interval_time = test_case["interval_time"]
        
        # Reset action, solar, and reason
        action = "auto"  # default
        solar = "maximize"  # default
        reason = "Test run: "
        
        # Set up time of day periods
        sunrise_hour = 6  # Default values
        sunset_hour = 18
        
        # Define time periods
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
        
        # Run the decision logic (copied from your script)
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
        
        # Store results
        results[test_name] = {
            "scenario": test_case["description"],
            "hour": hour,
            "buy_price": buy_price,
            "sell_price": sell_price,
            "battery_soc": battery_soc,
            "rrp": rrp,
            "is_spiking": is_spiking,
            "surplus_energy": surplus_energy,
            "time_category": "peak" if hour in peak else "day" if hour in day else "night",
            "action": action,
            "solar": solar,
            "reason": reason
        }
        
        # Display results
        print(f"Hour: {hour} ({'peak' if hour in peak else 'day' if hour in day else 'night'})")
        print(f"Buy: ${buy_price:.2f}, Sell: ${sell_price:.2f}, RRP: ${rrp:.2f}")
        print(f"Battery: {battery_soc}%, Reserve: {soc_reserve}%, Surplus: {surplus_energy}")
        print(f"Is spiking: {is_spiking}")
        print(f"Result → Action: {action}, Solar: {solar}")
        print(f"Reason: {reason}")
    
    # Restore original values
    hour = original_values["hour"]
    buy_price = original_values["buy_price"]
    sell_price = original_values["sell_price"]
    battery_soc = original_values["battery_soc"]
    rrp = original_values["rrp"]
    interval_time = original_values["interval_time"]
    
    return results


# Or to run a specific test:
def run_specific_test(test_name):
    """Run a single test case by name"""
    if test_name not in test_cases:
        print(f"Test '{test_name}' not found.")
        return
        
    # Create a temporary dictionary with just the one test
    single_test = {test_name: test_cases[test_name]}
    
    # Store original test_cases
    global test_cases
    orig_test_cases = test_cases
    
    # Run only the specific test
    test_cases = single_test
    results = run_all_tests()
    
    # Restore full test cases
    test_cases = orig_test_cases
    
    return results


