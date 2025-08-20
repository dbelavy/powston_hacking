# Available System Variables

## Time & Location Variables
| Variable | Type | Example | Description |
|----------|------|---------|-------------|
| interval_time | datetime | 2024-11-01 16:55:00+10:00 | Current billing interval timestamp |
| timezone_str | string | "Australia/Brisbane" | System timezone |
| location | LocationInfo | - | Contains name, region, timezone, latitude, longitude |
| sunrise | datetime | - | Daily sunrise time |
| sunset | datetime | - | Daily sunset time |
| current_hour | integer | 16 | Current hour from interval_time |

## Power Measurements
| Variable | Type | Example | Description |
|----------|------|---------|-------------|
| solar_power | float | 2.0 | Current solar generation (W) |
| grid_power | float | 1867.0 | Current grid power flow (W) |
| house_power | float | -1865.0 | Household power consumption (W) |

## Battery Statistics
| Variable | Type | Example | Description |
|----------|------|---------|-------------|
| battery_soc | float | 100.0 | Battery state of charge (%) |
| battery_capacity | float | 9600.0 | Total battery capacity (Wh) |

## Pricing Information
| Variable | Type | Example | Description |
|----------|------|---------|-------------|
| rrp | float | 77.8 | Reference retail price ($/MWh) |
| buy_price | float | 30.9 | Current buy price (c/kWh) |
| sell_price | float | 8.4 | Current sell price (c/kWh) |
| buy_forecast | list | [25.2, 28.1, ...] | Future buy prices (8 hours ahead) |
| sell_forecast | list | [8.4, 9.2, ...] | Future sell prices (8 hours ahead) |
| forecast | list | [77.8, 85.0, ...] | RRP forecast ($/MWh) |
| history_buy_prices | list | - | Historical buy price data |
| general_tariff | float | 28.5 | General electricity tariff (c/kWh) |
| feed_in_tariff | float | 8.4 | Feed-in tariff rate (c/kWh) |

## Weather and PV Forecast Variables
| Variable | Type | Example | Description |
|----------|------|---------|-------------|
| weather_data | dict | - | Complete weather forecast data |
| cloud_cover | float | 45.2 | Current cloud cover percentage |
| hourly_gti_forecast | list | [0, 50, 200, ...] | Hourly global tilted irradiance (W/m²) |
| gti_today | float | 8500.0 | Total GTI forecast for today |
| gti_past | float | 2100.0 | GTI accumulated so far today |
| gti_to_2pm | float | 4500.0 | GTI forecast until 2 PM |
| gti_sum_tomorrow | float | 9200.0 | Tomorrow's total GTI forecast |
| hours_until_midnight | integer | 8 | Hours remaining until midnight |

## System Configuration
| Variable | Type | Example | Description |
|----------|------|---------|-------------|
| optimal_charging | integer | 1 | Charging optimization setting |
| optimal_discharging | integer | 1 | Discharging optimization setting |
| import_soc | float | 95.0 | SOC threshold for import operations |
| feed_in_power_limitation | Optional[float] | 5000.0 | Export power limit (W) |
| always_export_rrp | Optional[float] | 1000.0 | RRP threshold for auto-export ($/MWh) |

## ML Thresholds and Confidence
| Variable | Type | Example | Description |
|----------|------|---------|-------------|
| threshold_1 | float | 0.75 | ML model threshold 1 |
| threshold_2 | float | 0.80 | ML model threshold 2 |
| threshold_3 | float | 0.85 | ML model threshold 3 |
| threshold_4 | float | 0.90 | ML model threshold 4 |
| threshold_5 | float | 0.95 | ML model threshold 5 |
| confidence_1 | float | 0.82 | ML model confidence 1 |
| confidence_2 | float | 0.87 | ML model confidence 2 |
| confidence_3 | float | 0.91 | ML model confidence 3 |
| confidence_4 | float | 0.94 | ML model confidence 4 |
| confidence_5 | float | 0.97 | ML model confidence 5 |

## System State
| Variable | Type | Example | Description |
|----------|------|---------|-------------|
| last_action | string | "auto" | Previous system action |
| action_pattern | list | ["auto", "charge", ...] | Recent action history |
| action_method | string | "script" | How action was determined |
| reason | string | "Default auto mode" | Current action reasoning |

## Site Information
| Variable | Type | Example | Description |
|----------|------|---------|-------------|
| APP_VERSION | string | "2.1.5" | Application version |
| serial_number | string | "INV123456" | Inverter serial number |
| manufacturer | string | "Sungrow" | Inverter manufacturer |
| product_name | string | "SH10RT" | Inverter product name |
| site_name | string | "Home Solar" | Site display name |
| site_id | integer | 12345 | Unique site identifier |
| state | string | "QLD" | Australian state |
| inverter_id | integer | 1839 | Inverter identifier |
| user_code_id | integer | 101 | User script identifier |
| user_code_name | string | "Auto Trading" | User script name |

## System Capabilities
| Variable | Type | Example | Description |
|----------|------|---------|-------------|
| hybrid | boolean | true | Hybrid inverter capability |
| data_logger | boolean | true | Data logging enabled |
| api_only | boolean | false | API-only operation mode |
| use_api | boolean | true | Use API for control |
| use_local | boolean | false | Use local control |
| read_only | boolean | false | Read-only mode |

## Live Data Quality
| Variable | Type | Example | Description |
|----------|------|---------|-------------|
| lv_quality | string | "good" | Live data quality indicator |
| lv_time | datetime | 2024-11-01 16:55:00+10:00 | Last live data timestamp |
| lv_buy_price | float | 30.9 | Last valid buy price |
| lv_sell_price | float | 8.4 | Last valid sell price |

## Data Collections
| Variable | Type | Example | Description |
|----------|------|---------|-------------|
| user_cache | dict | - | User-specific cached data |
| meter_df | dict | - | Meter reading data |
| last_days_df | dict | - | Historical daily data |
| inverters | dict | - | Multi-inverter data collection |
| site_statistics | dict | - | Site performance statistics |
| inverter_statistics | dict | - | Inverter performance statistics |
| mqtt_data | dict | - | MQTT sensor data from Home Assistant |
| runtime_params | dict | - | Runtime configuration parameters |

## Derived Solar Variables
| Variable | Type | Example | Description |
|----------|------|---------|-------------|
| night_reserve | float | 69.0 | Required battery reserve for overnight (%) |
| first_good_gti | integer | 7 | First hour with good solar irradiance |
| last_good_gti | integer | 17 | Last hour with good solar irradiance |
| is_solar_window_now | boolean | true | Whether currently in productive solar window |
| is_daytime | boolean | true | Whether between sunrise and sunset |
| soc_surplus | float | 15.5 | Battery SOC above night reserve (%) |
| time_left | float | 6.5 | Hours remaining until sunrise/sunset |
| projected_deficit | float | -5.2 | Projected SOC deficit by morning (%) |

## Decision Logging
| Variable | Type | Example | Description |
|----------|------|---------|-------------|
| decisions | DecisionLogger | - | Structured decision logging object with priority system |
