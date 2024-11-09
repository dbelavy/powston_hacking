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

## Available Variables

### Time & Location Variables
| Variable | Type | Example | Description |
|----------|------|---------|-------------|
| interval_time | datetime | 2024-11-01 16:55:00+10:00 | Current billing interval timestamp |
| timezone_str | string | "Australia/Brisbane" | System timezone |
| location | LocationInfo | - | Contains name, region, timezone, latitude, longitude |
| sunrise | datetime | - | Daily sunrise time |
| sunset | datetime | - | Daily sunset time |
| current_hour | integer | 16 | obtain from current_hour = interval_time.hour (24-hour format) |
| t_o_day | string | "peak" | Time period ("peak", "daytime", "nighttime") |

### Power Measurements
| Variable | Type | Example | Description |
|----------|------|---------|-------------|
| solar_power | float | 2.0W | Current solar generation |
| ppv | float | 2.0W | Photovoltaic power |
| grid_power | float | 1867.0W | Current grid power flow |
| pgrid | float | 1867.0W | Grid power measurement |
| house_power | float | -1865.0W | Household power consumption |
| reactive_power | float | 1018.0W | Reactive power measurement |
| max_ppv_power | integer | 0 | Maximum photovoltaic power |

### Battery Statistics
| Variable | Type | Example | Description |
|----------|------|---------|-------------|
| battery_soc | float | 100.0% | Battery state of charge |
| battery_capacity | integer | 9600 | Total battery capacity |
| battery_voltage | float | 333.5V | Battery voltage |
| battery_temperature | float | 28.0°C | Battery temperature |
| battery_current | float | 0.0A | Battery current |
| battery_charge | float | 9600.0 | Current charge level |

### Energy Metrics
| Variable | Type | Example | Description |
|----------|------|---------|-------------|
| daily_export_energy | float | 1887.6 | Energy exported today |
| total_export_energy | float | 1887.6 | Total energy exported |
| daily_charge_energy | float | 11.5 | Energy charged today |
| battery_charge_energy | float | 2710.4 | Total battery charge |
| daily_import_energy | float | 5318.3 | Energy imported today |
| total_import_energy | float | 5318.3 | Total energy imported |
| daily_discharge_energy | float | 6.7 | Energy discharged today |
| battery_discharge_energy | float | 2467.5 | Total battery discharge |

### Pricing Information
| Variable | Type | Example | Description |
|----------|------|---------|-------------|
| rrp | float | 77.8 | Reference retail price |
| buy_price | float | 30.9 | Current buy price |
| sell_price | float | 8.4 | Current sell price |
| buy_forecast | list | - | Future buy prices (8 hours) |
| sell_forecast | list | - | Future sell prices (8 hours) |
| avg_future_buy | float | 40.1 | Average future buy price |
| feed_in_tariff | float | 8.4 | Feed-in tariff rate |

### Grid Metrics
| Variable | Type | Example | Description |
|----------|------|---------|-------------|
| grid_frequency | float | 49.9 | Grid frequency |
| grid_voltage | float | 241.2 | Grid voltage |
| grid_current | float | 2.0 | Grid current (Phase A) |
| grid_current_B | float | 2.0 | Grid current (Phase B) |
| grid_current_C | float | 2.0 | Grid current (Phase C) |

### Solar Details
| Variable | Type | Example | Description |
|----------|------|---------|-------------|
| solar_voltage_1 | float | 0.0 | Solar panel voltage (String 1) |
| solar_current_1 | float | 0.0 | Solar panel current (String 1) |
| solar_voltage_2 | float | 0.0 | Solar panel voltage (String 2) |
| solar_current_2 | float | 0.0 | Solar panel current (String 2) |

## Control Parameters

### System Actions
The system supports the following control actions:
- **auto**: Maintain zero grid balance, charging/discharging to meet demand
- **charge**: Charge battery using grid and solar power
- **discharge**: Use battery for household demand without grid export
- **import**: Import from grid at full power for household and battery
- **export**: Export to grid at full power from battery and solar
- **stopped**: Pause battery operations, use grid for demand

### Solar Control
Solar generation can be controlled with two modes:
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

## Advanced Trading Strategies

### Time-Based Trading
```python
# Define time periods for optimal trading
sunrise_hour = sunrise.hour + 1
peak_start = 16
peak_end = 21

# Calculate average future buy price (next 2 hours)
avg_future_buy = sum(buy_forecast[0:4]) / len(buy_forecast[0:4])

# Time-of-day based strategy
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
# Constants for price-based decisions
PRICE_RATIO_THRESHOLD = 1.5  # Minimum ratio for profitable trading
MIN_SOC = 20                 # Minimum battery charge to maintain
HIGH_SOC = 80               # Target for charging before peak

# Negative price opportunity
if buy_price < 0:
    action = 'import'
    decision_reason = "Importing due to negative price"

# Price arbitrage opportunity
elif sell_price > (avg_future_buy * PRICE_RATIO_THRESHOLD) and battery_soc > MIN_SOC:
    action = 'export'
    decision_reason = f"Price arbitrage (Sell: {sell_price}, Avg future buy: {avg_future_buy})"

# Pre-peak charging strategy
elif (CHARGE_HOUR_START <= current_hour < CHARGE_HOUR_END) and battery_soc < HIGH_SOC:
    action = 'import'
    decision_reason = f"Scheduled charging before peak"
```

### Multi-Inverter Trading Strategy
```python
# Get data from primary inverter
house_power = inverters['inverter_params_1839']['house_power']  # positive is consumption
battery_soc = inverters['inverter_params_1839']['battery_soc']
grid_balance = inverters['inverter_params_1839']['grid_power']  # positive is drawing from grid

# Calculate house consumption in kW for curtailment decisions
house_kW = int(abs(house_power) // 1000) + 1

# Advanced solar control based on multiple conditions
if buy_price < 0:
    action = 'curtail100-curtail'  # Full curtailment during negative prices
elif sell_price > 0:
    action = 'export-export'       # Maximum export when profitable
elif battery_soc <= 95:
    action = 'export-export'       # Fill battery when not full
elif battery_soc > 95 and sell_price < 0:
    # Dynamic curtailment based on house consumption
    if house_kW > 9:
        action = 'export-export'   # High consumption needs full power
    else:
        # Curtail to match house consumption
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

# Time-based control
if sunrise_hour <= current_hour < peak_start:
    action = "charge"
elif peak_start <= current_hour < peak_end:
    action = "auto"
else:
    action = "auto"

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




## Using Reason Strings
The system uses a `reason` string to log decision-making processes and system state. This provides transparency and helps with debugging and monitoring system behavior.

## Best Practices for Reason Strings

1. **Start with System State**
```python
# Begin with core system metrics
reason += f" House: {house_power}W. Battery: {battery_power}W. Grid: {grid_balance}W. Battery: {battery_soc:.1f}%."
```

2. **Log Price Information**
```python
# Include current and forecasted prices
reason += f" Avg Buy price over the next 4 epochs: {avg_future_buy:.1f}c ~"
reason += f" Sell price {sell_price:.1f}c."
```

3. **Document System Suggestions**
```python
# Log what the system suggests before your logic
reason += f" Powston suggested action: ({suggested_action}) and solar: ({suggested_solar})."
```

4. **Record Time Context**
```python
# Include time-based information
reason += f" Current hour: {current_hour}. Time of day: {t_o_day}."
```

5. **Explain Decisions**
```python
# Document why a decision was made
if buy_price < 0:
    decision_reason = f" Electricity is free: {buy_price}c"
    action = 'curtail100-curtail'
    reason += decision_reason
```

6. **Log Final Decisions**
```python
# Always end with the final decision and its rationale
reason += f" {decision_reason}. Decision: action: {action}, solar: {solar}"
```

## Example of Comprehensive Reason String
```python
# Initialize reason string
reason = ""

# System state
reason += f" House: {house_power}W. Battery: {battery_power}W. Grid: {grid_balance}W."
reason += f" Battery: {battery_soc:.1f}%."

# Price information
reason += f" Avg Buy price over the next 4 epochs: {avg_future_buy:.1f}c."
reason += f" Sell price {sell_price:.1f}c."

# System suggestions
reason += f" Powston suggested action: ({suggested_action}) and solar: ({suggested_solar})."

# Time context
reason += f" Current hour: {current_hour}. Time of day: {t_o_day}."

# Decision making process
if buy_price < 0:
    decision_reason = f" Electricity is free: {buy_price}c"
    action = 'curtail100-curtail'
elif battery_soc > 95 and sell_price < 0:
    decision_reason = f" Battery full and negative sell price"
    if house_kW > 9:
        decision_reason += " High house consumption. Solar at max."
        action = 'export-export'
    else:
        curtail_level = max(1, min(9, house_kW))
        action = f'curtail{curtail_level}000-curtail'
        decision_reason += f" Curtail to {curtail_level:.1f}kW"

# Final decision
reason += f" {decision_reason}. Decision: {action} and {solar}."
```

## Benefits of Good Reason Strings

1. **Debugging**
   - Easily trace decision-making process
   - Identify unexpected behavior
   - Validate system logic

2. **Monitoring**
   - Track system performance
   - Understand state transitions
   - Verify price responsiveness

3. **Optimization**
   - Analyze decision patterns
   - Identify improvement opportunities
   - Fine-tune thresholds

4. **Maintenance**
   - Troubleshoot issues
   - Verify system health
   - Track long-term behavior

## Guidelines for Reason String Format

1. **Consistency**
   - Use consistent formatting
   - Include units (W, kW, %, c)
   - Format decimals consistently (.1f)

2. **Readability**
   - Use clear separators between components
   - Group related information
   - Include spaces after periods

3. **Completeness**
   - Include all relevant metrics
   - Document both inputs and outputs
   - Explain conditional logic

4. **Precision**
   - Use appropriate decimal places
   - Include timestamps when relevant
   - Document specific thresholds
