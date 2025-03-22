hour = interval_time.hour

# Constants
SOC_FULL = 100  # Full SOC threshold
SOC_THRESHOLD_25 = 25  # SOC threshold for export if price is above $0.15/kWh
SOC_THRESHOLD_20 = 20  # SOC threshold for export if price is above $0.40/kWh
SOC_THRESHOLD_15 = 15  # SOC threshold for export if price is above $1.00/kWh
SOC_THRESHOLD_40 = 40  # SOC threshold for import
SOC_THRESHOLD_60 = 60  # SOC threshold for import
SOC_THRESHOLD_80 = 80  # SOC threshold for import
SOC_THRESHOLD_95 = 95  # SOC threshold for import
sell_price1 = 20
sell_price2 = 50
sell_price3 = 100
buy_price1 = 5

# Initialize actions and reasons
action = 'auto'
reason = ''

# Simplify export logic based on sell price thresholds
if action == 'auto':
    if sell_price >= sell_price3 and battery_soc > SOC_THRESHOLD_15:
        action = 'export'
        solar = 'export'
        reason = f'Exporting due to high price, final SOC: {SOC_THRESHOLD_15}%'
    elif sell_price >= sell_price2 and battery_soc > SOC_THRESHOLD_20:
        action = 'export'
        solar = 'export'
        reason = f'Exporting due to good price, final SOC: {SOC_THRESHOLD_20}%'
    elif sell_price >= sell_price1 and battery_soc > SOC_THRESHOLD_25:
        action = 'export'
        solar = 'export'
        reason = f'Exporting due to moderate price, final SOC: {SOC_THRESHOLD_25}%'
    else:
        action = 'auto'

if buy_price <= buy_price1:  # Price is $0.03/kWh or less
    if battery_soc <= 100:
        action = 'import'
        reason = 'Importing due to low buy price'

# Ensure export between 6PM and 7PM if no other conditions are met
if 18 <= hour < 19 and action == 'auto':
    if battery_soc > 60:
        action = 'export'
        reason = 'Exporting between 6PM and 7PM'
    elif battery_soc <= 50 and action == 'export':
        action = 'auto'
        reason = 'SOC too low to export'

# If SOC not at certain level by 11am import
if battery_soc <= SOC_THRESHOLD_40:
    if 9 <= hour < 10:
        action = 'import'
        reason = 'Charging due to low SOC'
    elif battery_soc >= SOC_THRESHOLD_60:
        action = 'auto'
        reason = 'SOC sufficient'

# If SOC not at certain level by 1pm import
if battery_soc <= SOC_THRESHOLD_60:
    if 10 <= hour < 11:
        action = 'import'
        reason = 'Charging due to low SOC'
    elif battery_soc >= SOC_THRESHOLD_80:
        action = 'auto'
        reason = 'SOC sufficient'

# If SOC not at certain level by 3pm import
if battery_soc <= SOC_THRESHOLD_95:
    if 11 <= hour < 12:
        action = 'import'
        reason = 'Charging due to low SOC'
    elif battery_soc >= SOC_FULL:
        action = 'auto'
        reason = 'SOC full'