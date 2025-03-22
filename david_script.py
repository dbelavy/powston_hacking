# Constants
MIN_SOC = 20
HIGH_SOC = 95
CHARGE_HOUR_START = 12
CHARGE_HOUR_END = 15
MIN_SELL_PRICE = 25
TAKE_THE_MONEY = 200
GOOD_MONEY = 80
PRICE_RATIO_THRESHOLD = 1.05

def safe_float(value):
    """Safely convert any value to float"""
    try:
        return float(value)
    except (ValueError, TypeError):
        return 0.0

def safe_get(variables, key, default=0):
    """Safely get a value from variables dictionary"""
    try:
        value = variables.get(key, default)
        return value if value is not None else default
    except (AttributeError, KeyError):
        return default

def safe_list_float(value):
    """Safely convert list to list of floats"""
    try:
        if not isinstance(value, list):
            return []
        return [safe_float(x) for x in value]
    except (ValueError, TypeError):
        return []

def safe_get_hour(time_obj):
    """Safely get hour from time object"""
    try:
        return time_obj.hour
    except (AttributeError, TypeError):
        return 0

def calculate_sma(data, period):
    """Calculate Simple Moving Average"""
    try:
        if not data or len(data) < period:
            return [0]
        results = []
        for i in range(len(data) - period + 1):
            window = data[i:i + period]
            average = sum(window) / period
            results.append(average)
        return results
    except (ValueError, TypeError):
        return [0]

def calculate_avg_future_buy(buy_forecast, rrp):
    """Calculate average future buy price"""
    try:
        if buy_forecast and len(buy_forecast) >= 4:
            return sum(buy_forecast[0:4]) / 4
        return safe_float(rrp) / 10
    except (ValueError, TypeError):
        return 0

def determine_time_of_day(current_hour, sunrise_hour):
    """Determine time of day and initial action"""
    try:
        peak_start = 16
        peak_end = 21
        if sunrise_hour <= current_hour < peak_start:
            return 'daytime', 'charge', 0
        elif peak_start <= current_hour < peak_end:
            battery_reserve = {16: 20, 17: 15, 18: 10, 19: 5, 20: 3}
            return 'peak', 'auto', battery_reserve.get(current_hour, 0)
        return 'nighttime', 'auto', 0
    except (ValueError, TypeError):
        return 'daytime', 'auto', 0

def is_price_spiking(sell_price, sma, avg_future_buy):
    """Determine if price is spiking"""
    try:
        if not sma:
            return False
        return (sell_price > sma[-1] and sell_price > (avg_future_buy * PRICE_RATIO_THRESHOLD))
    except (ValueError, TypeError):
        return False

def determine_action(battery_soc, sell_price, buy_price, avg_future_buy, t_o_day, is_spiking, current_hour, battery_capacity, soc_reserve):
    """Determine battery action based on conditions"""
    try:
        if buy_price < 0:
            return 'import', "Importing due to negative price"
        if sell_price > TAKE_THE_MONEY and battery_soc > MIN_SOC:
            return 'export', f"Price > ${TAKE_THE_MONEY/100:.2f} so Take the Money"
        if is_spiking and battery_soc > MIN_SOC and sell_price > MIN_SELL_PRICE:
            return 'export', f"Price arbitrage (Sell: {sell_price:.1f}, Avg future buy: {avg_future_buy:.1f})"
        if CHARGE_HOUR_START <= current_hour < CHARGE_HOUR_END and battery_soc < HIGH_SOC:
            return 'import', f"Scheduled charging before peak. Battery not full between {CHARGE_HOUR_START}:00 and {CHARGE_HOUR_END}:00"
        if t_o_day == "nighttime" and battery_soc > 50 and sell_price > MIN_SELL_PRICE:
            return 'export', 'Pick up nighttime export option'
        if t_o_day == "peak" and sell_price > GOOD_MONEY and battery_soc > (soc_reserve / safe_float(battery_capacity) * 100 if battery_capacity else 0):
            return 'export2000', 'Take a little off the table for good money'
        return 'auto', f"Default {t_o_day} operation"
    except (ValueError, TypeError, ZeroDivisionError):
        return 'auto', "Error in decision making"

def build_reason_string(vars_dict, t_o_day, action, solar, is_spiking, decision_reason, current_hour, sma_1hr):
    """Build detailed reason string"""
    try:
        house_power = safe_float(vars_dict.get('house_power', 0))
        grid_power = safe_float(vars_dict.get('grid_power', 0))
        solar_power = safe_float(vars_dict.get('solar_power', 0))
        battery_soc = safe_float(vars_dict.get('battery_soc', 20))
        battery_voltage = safe_float(vars_dict.get('battery_voltage', 0))
        battery_current = safe_float(vars_dict.get('battery_current', 0))
        sell_price = safe_float(vars_dict.get('sell_price', 0))
        buy_price = safe_float(vars_dict.get('buy_price', 0))
        suggested_action = str(vars_dict.get('suggested_action', 'auto'))
        suggested_solar = str(vars_dict.get('suggested_solar', 'export'))
        current_usage = house_power / 1000
        solar_generation = solar_power / 1000
        battery_power = battery_voltage * battery_current
        avg_future_buy = calculate_avg_future_buy(safe_list_float(vars_dict.get('buy_forecast', [])), vars_dict.get('rrp', 0))
        parts = [
            f"Powston suggests action: ({suggested_action}) and solar: ({suggested_solar})",
            f"Time of day: {t_o_day}",
            f"Current hour: {current_hour}",
            f"Avg Buy price over next 4 epochs: {avg_future_buy:.1f}c",
            f"Buy price: {buy_price:.1f}c",
            f"Sell price: {sell_price:.1f}c",
            f"House usage: {current_usage:.1f}kW",
            f"Solar generation: {solar_generation:.1f}kW",
            f"Grid: {grid_power/1000:.2f}kW",
            f"Battery power: {battery_power/1000:.2f}kW",
            f"Battery SOC: {battery_soc:.1f}%",
            f"Most recent 1hr SMA: {sma_1hr[-1]:.2f}",
            f"Is spiking = {1 if is_spiking else 0}",
            f"Decision reason: {decision_reason}",
            f"Decision: action ({action}) solar ({solar})"
        ]
        return " | ".join(parts)
    except (ValueError, TypeError, ZeroDivisionError):
        return "Error building reason string"

def process_battery_management(vars_dict):
    """Main entry point for battery management"""
    interval_time = vars_dict.get('interval_time')
    sunrise = vars_dict.get('sunrise')
    current_hour = safe_get_hour(interval_time)
    sunrise_hour = safe_get_hour(sunrise) + 1
    battery_soc = safe_float(vars_dict.get('battery_soc', 20))
    battery_capacity = safe_float(vars_dict.get('battery_capacity', 25.6))
    sell_price = safe_float(vars_dict.get('sell_price', 0))
    buy_price = safe_float(vars_dict.get('buy_price', 0))
    t_o_day, initial_action, soc_reserve = determine_time_of_day(current_hour, sunrise_hour)
    history_prices = safe_list_float(vars_dict.get('history_buy_prices', []))
    if not history_prices:
        history_prices = [0] * 12
    sma_1hr = calculate_sma(history_prices, 12)
    avg_future_buy = calculate_avg_future_buy(safe_list_float(vars_dict.get('buy_forecast', [])), vars_dict.get('rrp', 0))
    is_spiking = is_price_spiking(sell_price, sma_1hr, avg_future_buy)
    action, decision_reason = determine_action(battery_soc, sell_price, buy_price, avg_future_buy, t_o_day, is_spiking, current_hour, battery_capacity, soc_reserve)
    solar = str(vars_dict.get('suggested_solar', 'export'))
    reason = build_reason_string(vars_dict, t_o_day, action, solar, is_spiking, decision_reason, current_hour, sma_1hr)
    return action, solar, reason

# The script expects all variables to be available in the global scope
# It will process them and set these output variables:
# action: str - The battery action to take
# solar: str - The solar mode to use
# reason: str - The detailed reason for the decision
action, solar, reason = process_battery_management(globals())
