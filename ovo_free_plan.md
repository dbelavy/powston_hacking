# OVO Energy Plan Optimizer

This helps optimize energy usage and solar exports for users on OVO Energy plans in Queensland. It leverages time-of-use (TOU) rates, solar irradiance forecasts, and battery state-of-charge (SoC) to make informed decisions about when to charge, discharge, or hold battery operations.

## Features

* **Time-of-Use Optimization**: Aligns battery operations with OVO Energy's TOU periods to minimize costs and maximize solar export benefits.

* **Solar Forecast Integration**: Utilizes solar irradiance forecasts to anticipate solar generation and adjust battery behavior accordingly.

* **Dynamic Export Management**: Supports integration with Queensland's Dynamic Connections program to adapt to real-time export limits.

* **Customizable Rules**: Allows users to define and adjust rules based on their specific energy usage patterns and goals.

## OVO Energy Plan Context

OVO Energy offers various plans in Queensland, including the "Free 3" plan, which provides free electricity from 11 AM to 2 PM daily. However, the solar feed-in tariff (FiT) for exported energy is relatively low, at **3 cents per kilowatt-hour (kWh)**. This setup encourages users to consume electricity during the free period and optimize battery usage to reduce costs.

## Queensland Export Limitations

In Queensland, solar export limits are enforced to maintain grid stability:

* **Fixed Export Limits**: Typically, a 5 kW export limit is applied for single-phase systems.

* **Dynamic Connections Program**: Offered by Energex and Ergon Energy, this program allows for dynamic export limits, adjusting in real-time based on grid capacity, potentially allowing exports up to 10 kW per phase. ([redbacktech.com][2])

## Example Rules

```python
FREE_START = 11
FREE_END = 15
PEAK_START = 16
PEAK_END = 21

current_hour = interval_time.hour
global_tilted_irradiance = weather_data.get('hourly', {}).get('global_tilted_irradiance_instant', [0] * 24)

# Calculate cumulative irradiance from 10 AM to current hour
irradiance_past = sum(global_tilted_irradiance[10:current_hour])
# Calculate total expected irradiance from 10 AM to 3 PM
irradiance_total = sum(global_tilted_irradiance[10:15])
# Calculate percentage of expected irradiance already received
percent_pv_past = (irradiance_past / irradiance_total) * 100 if irradiance_total > 0 else 0

action = 'auto'
reason = "Default action: self consume as much as possible."

if current_hour < FREE_START and sunrise > interval_time:
    action = 'discharge'
    reason = "Early morning. Discharging to meet demand before scheduled charge window."
elif FREE_START <= current_hour < FREE_END:
    if battery_soc < 80:
        action = 'import'
        reason = f"Charging during off-peak hours ({FREE_START}-{FREE_END}) to reach 80% SoC."
    elif battery_soc < 95 and percent_pv_past < 50:
        action = 'import'
        reason = f"Charging to 95% SoC due to low solar generation ({percent_pv_past:.2f}% of expected)."
    else:
        action = 'discharge'
        reason = "Holding charge to allow for solar export during peak generation hours."
elif FREE_END <= current_hour < PEAK_START:
    action = 'charge'
    reason = "Pre-peak hours. Keep charge to prepare for evening peak demand."
elif PEAK_START <= current_hour < PEAK_END:
    action = 'discharge'
    reason = "Peak hours detected. Discharging to meet household demand and reduce grid usage."
```
## Customization

You can modify to adjust the decision-making logic. For example, to change the free electricity window:

```python
FREE_START = 11  # 11 AM
FREE_END = 14    # 2 PM
```

Adjust these values based on your specific OVO Energy plan details.
