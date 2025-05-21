# POWSTON Energy Management System

## Overview
POWSTON is an advanced energy management system that combines smart hardware devices with a cloud-based platform to optimize power management in your home. The system enables intelligent control of battery storage, solar power integration, and automated energy trading based on real-time market conditions.

## System Architecture

### Core Components
- Hardware devices for power management
- Cloud-based control platform
- Python-based customization interface
- Real-time monitoring and control systems

### Key Features
- Automated battery management
- Solar power integration
- Real-time energy trading
- Custom control scripts support
- Dynamic pricing optimization

## System Variables
For a complete list of available system variables and their descriptions, please see [available_variables.md](available_variables.md).

## Control System

### System Actions
The system supports the following control actions:
- **auto**: Maintain zero grid balance, charging/discharging to meet demand
- **charge**: Charge battery only from solar power excess after meeting house demand
- **discharge**: Use battery for household demand without grid export
- **import**: Import from grid at full power for household and battery
- **export**: Export to grid at full power from battery and solar
- **stopped**: Pause battery operations, use grid for demand

### Solar Control Modes
- **export**: Operate at maximum capacity with grid export
- **curtail**: Limit generation to match household demand

### System Parameters
| Parameter | Type | Description |
|-----------|------|-------------|
| optimal_charging | integer | Charging optimization setting |
| optimal_discharging | integer | Discharging optimization setting |
| feed_in_power_limitation | integer | Export power limit |
| export_power_limitation | integer | Maximum export power |
| export_power_limitation_enable | integer | Export limitation control |

## Trading Strategies

### Time-Based Strategy
```python
# Define time periods
sunrise_hour = sunrise.hour + 1
peak_start = 16
peak_end = 21

# Time-of-day based control
if sunrise_hour <= current_hour < peak_start:
    t_o_day = 'daytime'
    action = "charge"  # Charge during daytime for peak usage
elif peak_start <= current_hour < peak_end:
    t_o_day = 'peak'
    action = "auto"    # Auto mode during peak for optimal grid balance
else:
    t_o_day = 'nighttime'
    action = "auto"    # Auto mode at night to maintain grid balance
```

### Price Arbitrage Strategy
```python
# Constants
PRICE_RATIO_THRESHOLD = 1.5  # Minimum ratio for profitable trading
MIN_SOC = 20                 # Minimum battery charge to maintain
HIGH_SOC = 80               # Target for charging before peak

# Calculate average future buy price
avg_future_buy = sum(buy_forecast[0:4]) / len(buy_forecast[0:4]) if buy_forecast else None

# Trading logic
if buy_price < 0:
    action = 'import'
    decision_reason = "Importing due to negative price"
elif sell_price > (avg_future_buy * PRICE_RATIO_THRESHOLD) and battery_soc > MIN_SOC:
    action = 'export'
    decision_reason = f"Price arbitrage (Sell: {sell_price}, Avg future buy: {avg_future_buy})"
elif (CHARGE_HOUR_START <= current_hour < CHARGE_HOUR_END) and battery_soc < HIGH_SOC:
    action = 'import'
    decision_reason = f"Scheduled charging before peak"
```


### Solar Forecast Strategy
Use solar irradiance forecasts to estimate battery SOC and decide whether to import
```python
IMPORT_TOLERANCE = 50  # Acceptable % margin over the lowest forecasted buy price
MIN_SOC_AT_PEAK = 70  # Target SOC (%) by 4 PM

# Accumulate past and expected solar irradiance until 4 PM
global_tilted_irradiance_past = sum(
    weather_data.get('hourly', {}).get('global_tilted_irradiance_instant', [-1]*24)[:interval_time.hour]
)
global_tilted_irradiance_to_2pm = sum(
    weather_data.get('hourly', {}).get('global_tilted_irradiance_instant', [-1]*24)[:16]
)

# Only apply this logic before 4 PM
if 4 < interval_time.hour < 16 and buy_forecast:
    low_buy_price = round(min(buy_forecast), 2)
    precent_pv_past = round(global_tilted_irradiance_past / global_tilted_irradiance_to_2pm * MIN_SOC_AT_PEAK, 2)
    
    reason += f" Solar Forecast Strategy: Expected SOC from PV by 4 PM ~{precent_pv_past}%."

    tolerant_low_price = round(low_buy_price * ((100 + IMPORT_TOLERANCE) / 100), 2)

    if action in ['auto', 'charge'] and battery_soc < precent_pv_past and buy_price < tolerant_low_price:
        action = 'import'
        reason += f" Buy price {buy_price}c is lower than {tolerant_low_price}c. Importing to meet target SOC."
    else:
        reason += f" Holding current action: {action}. Waiting as import price {buy_price}c > {tolerant_low_price}c."
```

### Multi-Inverter Strategy
```python
# Get inverter data
house_power = inverters.get('inverter_params_1839', {}).get('house_power',0)
battery_soc = inverters.get('inverter_params_1839', {}).get('battery_soc',0)
grid_balance = inverters.get('inverter_params_1839', {}).get('grid_power',0)

# Calculate house consumption in kW
house_kW = int(abs(house_power) // 1000) + 1

# Solar control logic
if buy_price < 0:
    action = 'curtail100-curtail'  # Full curtailment during negative prices
elif sell_price > 0:
    action = 'export-export'       # Maximum export when profitable
elif battery_soc <= 95:
    action = 'export-export'       # Fill battery when not full
elif battery_soc > 95 and sell_price < 0:
    if house_kW > 9:
        action = 'export-export'   # High consumption needs full power
    else:
        curtail_level = max(1, min(9, house_kW))
        action = f'curtail{curtail_level}000-curtail'
```

### Trading Strategy Best Practices
1. **Price Monitoring**
   - Track real-time prices and forecasts
   - Set appropriate thresholds for buy/sell decisions
   - Consider network charges in price calculations

2. **Battery Management**
   - Maintain minimum SOC for grid stability
   - Charge during low-price periods
   - Reserve capacity for peak price periods
   - Monitor battery health and temperature

3. **Solar Integration**
   - Optimize self-consumption during peak prices
   - Curtail generation during negative prices
   - Balance between battery charging and grid export

4. **Load Management**
   - Adjust strategies based on household consumption
   - Consider time-of-use tariffs
   - Plan for peak demand periods

5. **Market Participation**
   - Use price forecasts for planning
   - Set profit thresholds for trading
   - Consider grid stability requirements
   - Monitor regulatory compliance

## Basic Code Examples

### Basic Battery Management
```python
# Constants
MIN_SOC = 20
HIGH_SOC = 80
CHARGE_HOUR_START = 13
CHARGE_HOUR_END = 15
PRICE_RATIO_THRESHOLD = 1.5

# Price-based decisions
if buy_price < 0:
    action = 'import'
elif sell_price > (avg_future_buy * PRICE_RATIO_THRESHOLD) and battery_soc > MIN_SOC:
    action = 'export'
```

### Solar Inverter Control
```python
# Price-based solar control
if buy_price < 0:
    action = 'curtail100-curtail'
elif sell_price > 0:
    action = 'export-export'
elif battery_soc <= 95:
    action = 'export-export'
else:
    curtail_level = max(1, min(9, house_kW))
    action = f'curtail{curtail_level}000-curtail'
```

## Best Practices
1. Always maintain minimum battery SOC (State of Charge)
2. Consider time-of-use pricing for charge/discharge cycles
3. Optimize for peak/off-peak periods
4. Monitor battery temperature and health
5. Balance between self-consumption and grid export
6. Use forecasting data for predictive control
