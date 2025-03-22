
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
