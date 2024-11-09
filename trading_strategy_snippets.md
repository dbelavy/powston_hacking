# POWSTON Trading Strategy Snippets

This guide provides reusable code snippets for different trading strategies, organized by type. Each snippet includes the strategy logic, explanation, and example code.

Several ideas from rbollar's code here:
https://github.com/rbollar/powston_script/blob/main/script.py

## 1. Price-Based Trading Strategies

### High Price Export Strategy
```python
# Strategy: Export when sell price is exceptionally high
always_sell_price = 75.0  # Price threshold for guaranteed selling

if sell_price >= always_sell_price and battery_soc > 10:
    action = 'export'
    solar = 'export'
    reason += f" High price export: {sell_price}c exceeds threshold of {always_sell_price}c"
```
**Logic**: Maximize profit by selling when prices are exceptionally high, while maintaining minimum battery levels. Note, if prices remain high for a long time, you may need to buy back later at high prices.

### Negative Price Strategy
```python
# Strategy: Import during negative prices, curtail solar
if buy_price <= 0.0 and battery_soc < full_battery:
    action = 'import'
    solar = 'curtail'
    reason += f" Negative price import: Buy at {buy_price}c"

# Additional negative price handling
elif sell_price < 0.0 and buy_price < abs(sell_price):
    action = 'auto'
    solar = 'curtail'
    reason += f" Negative export price: {sell_price}c"
```
**Logic**: Take advantage of negative prices to charge battery and avoid paying to export.

## 2. Time-Based Trading Strategies

### Peak Preparation Strategy
```python
# Strategy: Ensure battery is charged before peak period
peak_time = 16  # 4 PM
start_charging_time = peak_time - time_to_full_charge

if start_charging_time <= current_hour < peak_time and battery_soc < full_battery:
    action = 'import'
    solar = 'export'
    reason += f" Charging for peak period: {battery_soc}% < {full_battery}%"
```
**Logic**: Prepare for peak demand by ensuring battery is fully charged.

### Day/Night Strategy
```python
# Strategy: Different behaviors for day and night
if daytime:  # solar_power > 0 and hour < peak_time
    action = 'auto'
    solar = 'export'
    reason += " Daytime: Optimizing solar generation"
else:
    action = 'discharge'
    solar = 'export'
    reason += " Nighttime: Using stored energy"
```
**Logic**: Optimize for solar generation during day, use stored energy at night.

## 3. Battery State Trading Strategies

### Battery Protection Strategy
```python
# Strategy: Protect battery from over-discharge during peak
MIN_SOC = 10
if interval_time.hour > 17 and interval_time.hour < 21 and battery_soc < MIN_SOC:
    action = 'auto'
    reason += f" Protecting battery: {battery_soc}% < {MIN_SOC}%"
```
**Logic**: Prevent battery depletion during critical periods.

### Dynamic Reserve Strategy
```python
# Strategy: Adjust reserve based on time until sunrise
if 0 <= hours_until_sunrise_plus_active <= solar_active_hours:
    reserve_factor = max(0, 1 - hours_until_sunrise_plus_active / solar_active_hours)
    required_min_soc = reserve_factor * (estimated_consumption_kW / battery_capacity) * 100
    reason += f" Dynamic reserve: {required_min_soc:.1f}%"
```
**Logic**: Dynamically adjust battery reserve based on time until solar generation resumes.

## 4. Forecast-Based Trading Strategies

### Price Forecast Optimization
```python
# Strategy: Use price forecasts for optimal trading
# Apply uncertainty discount to forecasts
uncertainty_discount = 0.10  # 10% per hour

discounted_buy_forecast = [
    buy_forecast[i] * ((1 + uncertainty_discount) ** i)
    for i in range(min(8, len(buy_forecast)))
]

discounted_sell_forecast = [
    sell_forecast[i] * ((1 - uncertainty_discount) ** i)
    for i in range(min(8, len(sell_forecast)))
]

# Check for optimal buy/sell opportunities
if (buy_price < max_buy_price and 
    battery_soc > required_min_soc and 
    sell_price >= max(discounted_sell_forecast) and 
    sell_price >= min_sell_price):
    action = 'export'
    reason += f" Optimal sell price: current {sell_price}c vs forecast max {max(discounted_sell_forecast)}c"
```
**Logic**: Use discounted forecasts to make optimal trading decisions while accounting for uncertainty.

### Load Forecast Integration


```python
# Strategy: Consider minimum house power usage forecast
min_house_power = [
    1500.0,  # 12 AM
    1500.0,  # 1 AM
    # ... (24 hour values)
    1500.0   # 11 PM
]

effective_house_power = max(
    house_power / num_inverters,
    min_house_power[current_hour] / num_inverters
)

estimated_consumption_kW = effective_house_power * hours_until_lowest_buy
required_min_soc = reserve_factor * (estimated_consumption_kW / battery_capacity) * 100
```
**Logic**: Integrate load forecasts to ensure sufficient capacity for expected demand.

## 5. Solar Generation Trading Strategies

### Solar Curtailment Strategy
```python
# Strategy: Dynamic solar curtailment based on house consumption
if battery_soc > 95 and sell_price < 0:
    house_kW = int(abs(house_power) // 1000) + 1
    if house_kW > 9:
        action = 'export-export'
        reason += " High consumption, maximum solar"
    else:
        curtail_level = max(1, min(9, house_kW))
        action = f'curtail{curtail_level}000-curtail'
        reason += f" Curtailing to {curtail_level}kW"
```
**Logic**: Dynamically adjust solar generation based on consumption and grid conditions.

### Daytime Solar Optimization
```python
# Strategy: Optimize solar usage during daytime
if daytime:
    if sell_price >= min_day_sell_price and battery_soc >= required_min_soc:
        action = 'export'
        solar = 'export'
        reason += f" Daytime export: price {sell_price}c > {min_day_sell_price}c"
    else:
        action = 'auto'
        solar = 'export'
        reason += " Daytime charging priority"
```
**Logic**: Balance between immediate export and battery charging during solar generation periods.

## Best Practices for Strategy Implementation

1. **Combine Strategies Carefully**
   - Consider strategy priorities
   - Handle conflicts between strategies
   - Maintain clear decision hierarchy

2. **Monitor and Log**
   - Use detailed reason strings
   - Track strategy performance
   - Log key decision points

3. **Safety Checks**
   - Validate battery SOC limits
   - Check price thresholds
   - Verify time-based conditions

4. **Dynamic Parameters**
   - Adjust thresholds based on conditions
   - Use forecasts when available
   - Consider seasonal variations

5. **Error Handling**
   - Handle missing data gracefully
   - Provide fallback strategies
   - Maintain safe default behaviors
