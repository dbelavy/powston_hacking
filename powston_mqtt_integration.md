## Powston MQTT Integration

Powston supports importing data from **Home Assistant MQTT feeds** using the `mqtt_data` dictionary structure.

---

### ✅ Structure & Access

MQTT values are available under `mqtt_data` as nested dictionaries. For example:

```python
solar_estimate_remaining = mqtt_data.get('solar_estimate', {}).get('solar_estimate_remaining')
```

Each feed is assumed to follow this pattern:
```json
{
  "solar_estimate": {
    "solar_estimate_remaining": 12.34,
    "solar_surplus_deficit": -3.21,
    "combined_pv_battery_state_of_charge": 47.5
  }
}
```

---

### ⚠️ Best Practices

| Concern | Strategy |
|--------|----------|
| Missing data | Use `.get()` with nested defaults to avoid `NoneType` errors. |
| Type safety | Wrap values with `isinstance()` or set sane defaults. |
| Divisions | Avoid direct division with MQTT-imported variables unless type-checked or clamped. |

---

### 🧪 Code Sample

```python
# Safe extraction from MQTT feed
solar_estimate_remaining = mqtt_data.get('solar_estimate', {}).get('solar_estimate_remaining')
if not isinstance(solar_estimate_remaining, (int, float)):
    solar_estimate_remaining = 0.1  # Fallback default

solar_surplus_deficit = mqtt_data.get('solar_estimate', {}).get('solar_surplus_deficit')
if not isinstance(solar_surplus_deficit, (int, float)):
    solar_surplus_deficit = 0.1

combined_battery_soc = mqtt_data.get('solar_estimate', {}).get('combined_pv_battery_state_of_charge')
if not isinstance(combined_battery_soc, (int, float)):
    combined_battery_soc = battery_soc if isinstance(battery_soc, (int, float)) else 0.0
```

---

### 🧠 Tips

- **Always provide fallback values** when pulling from `mqtt_data`, even for known-good keys.
- Define MQTT imports near the **top of your script** to ensure variables are available for decisions.
- Consider logging or flagging invalid or unexpected values during debug runs.

## 🏠 Home Assistant Example: Publishing MQTT Data

To feed solar forecast and battery data to Powston from Home Assistant, you can use an automation like this:

```yaml
alias: Powston Publish Solar Estimate to MQTT
description: ""
triggers:
  - minutes: /1
    trigger: time_pattern
actions:
  - data:
      qos: 0
      retain: true
      topic: bollar/mqtt_data/solar_estimate
      payload: |-
        {{
          {
            "combined_pv_battery_state_of_charge": states('sensor.pv_battery_state_of_charge') | float,
            "solar_estimate_remaining": states('sensor.solar_production_estimated_remaining_today_combined') | float,
            "solar_surplus_deficit": states('sensor.solar_surplus_or_deficit_until_4_pm') | float
          } | to_json
        }}
    action: mqtt.publish
mode: single
```

This publishes to `bollar/mqtt_data/solar_estimate` every minute with real-time values for solar estimates and battery state of charge.
