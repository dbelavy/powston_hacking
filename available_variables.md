# Available System Variables

## Time & Location Variables
| Variable | Type | Example | Description |
|----------|------|---------|-------------|
| interval_time | datetime | 2024-11-01 16:55:00+10:00 | Current billing interval timestamp |
| timezone_str | string | "Australia/Brisbane" | System timezone |
| location | LocationInfo | - | Contains name, region, timezone, latitude, longitude |
| sunrise | datetime | - | Daily sunrise time |
| sunset | datetime | - | Daily sunset time |

## Power Measurements
| Variable | Type | Example | Description |
|----------|------|---------|-------------|
| solar_power | float | 2.0W | Current solar generation |
| ppv | float | 2.0W | Photovoltaic power |
| grid_power | float | 1867.0W | Current grid power flow |
| pgrid | float | 1867.0W | Grid power measurement |
| house_power | float | -1865.0W | Household power consumption |
| reactive_power | float | 1018.0W | Reactive power measurement |
| max_ppv_power | integer | 0 | Maximum photovoltaic power |

## Battery Statistics
| Variable | Type | Example | Description |
|----------|------|---------|-------------|
| battery_soc | float | 100.0% | Battery state of charge |
| battery_capacity | integer | 9600 | Total battery capacity |
| battery_voltage | float | 333.5V | Battery voltage |
| battery_temperature | float | 28.0°C | Battery temperature |
| battery_current | float | 0.0A | Battery current |
| battery_charge | float | 9600.0 | Current charge level |

## Energy Metrics
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

## Pricing Information
| Variable | Type | Example | Description |
|----------|------|---------|-------------|
| rrp | float | 77.8 | Reference retail price |
| buy_price | float | 30.9 | Current buy price |
| sell_price | float | 8.4 | Current sell price |
| buy_forecast | list | - | Future buy prices (8 hours) |
| sell_forecast | list | - | Future sell prices (8 hours) |
| feed_in_tariff | float | 8.4 | Feed-in tariff rate |

## Grid Metrics
| Variable | Type | Example | Description |
|----------|------|---------|-------------|
| grid_frequency | float | 49.9 | Grid frequency |
| grid_voltage | float | 241.2 | Grid voltage |
| grid_current | float | 2.0 | Grid current (Phase A) |
| grid_current_B | float | 2.0 | Grid current (Phase B) |
| grid_current_C | float | 2.0 | Grid current (Phase C) |

## Solar Details
| Variable | Type | Example | Description |
|----------|------|---------|-------------|
| solar_voltage_1 | float | 0.0 | Solar panel voltage (String 1) |
| solar_current_1 | float | 0.0 | Solar panel current (String 1) |
| solar_voltage_2 | float | 0.0 | Solar panel voltage (String 2) |
| solar_current_2 | float | 0.0 | Solar panel current (String 2) |

## Derived Variables
| Variable | Type | Source | Description |
|----------|------|--------|-------------|
| sunrise_hour | integer | `sunrise.hour + 1` | Hour of sunrise plus one hour buffer |
| avg_future_buy | float | `sum(buy_forecast[0:4]) / len(buy_forecast[0:4])` | Average buy price over next 4 epochs |
| house_kW | integer | `int(abs(house_power) // 1000) + 1` | House consumption in kilowatts, rounded up |
| t_o_day | string | Based on current_hour vs sunrise/peak times | Time of day category (daytime/peak/nighttime) |
| curtail_level | integer | `max(1, min(9, house_kW))` | Solar curtailment level based on house consumption |
