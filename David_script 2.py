# from datetime import timezone, timedelta

# Constants
MIN_SOC = 20
HIGH_SOC = 95
CHARGE_HOUR_START = 13
CHARGE_HOUR_END = 15
MIN_SELL_PRICE = 20

# BATTERY_POWER = battery_capacity * battery_soc / 100000 # in kWh
# SELL_PRICE_THRESHOLD = 50
PRICE_RATIO_THRESHOLD = 1.5
sunrise_hour = sunrise.hour + 1
peak_start = 16
peak_end = 21

# Calculate average future buy price (next 2 hours)
avg_future_buy = sum(buy_forecast[0:4]) / len(buy_forecast[0:4]) if buy_forecast else None
# Get current hour
current_hour = interval_time.hour
# current_hour = interval_time.astimezone(timezone(timedelta(hours=10))).hour
# current_hour = (interval_time.hour + 10) % 24

# Determine time of day
if sunrise_hour <= current_hour < peak_start:
    t_o_day = 'daytime'
    action = "charge"
elif peak_start <= current_hour < peak_end:
    t_o_day = 'peak'
    action = "auto"
else:
    t_o_day = 'nighttime'
    action = "auto"

# Build moving average
prices = 10 #history_buy_prices

# Simple Moving Average (SMA) for different periods
def calculate_sma(data, period):
    results = []
    for i in range(len(data) - period + 1):
        window = data[i:i + period]
        average = sum(window) / period
        results.append(average)
    return results

if buy_price < 0:
    action = 'import'
    decision_reason = "Importing due to negative price"

elif sell_price > (avg_future_buy * PRICE_RATIO_THRESHOLD) and battery_soc > MIN_SOC and sell_price > MIN_SELL_PRICE:
    action = 'export'
    decision_reason = f"Price arbitrage (Sell: {sell_price}, Avg future buy: {avg_future_buy})"

# elif sell_price > SELL_PRICE_THRESHOLD and battery_soc > 50:
#    action = 'export'
#    decision_reason = f" Sell price above export threshold of {SELL_PRICE_THRESHOLD}."

elif (CHARGE_HOUR_START <= current_hour < CHARGE_HOUR_END) and battery_soc < HIGH_SOC:
    action = 'import'
    decision_reason = f" Scheduled charging before peak. Battery not full between {CHARGE_HOUR_START}:00 and {CHARGE_HOUR_END}:00."

else:
    decision_reason = f"Default {t_o_day} operation"

# Add final decision to reason
reason += f" {decision_reason}. Decision: action: {action}"

# reason += f" History buy prices: {history_buy_prices}."
