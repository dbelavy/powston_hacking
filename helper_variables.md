# New Rule Helper Variables

These variables are in the rule engine, allowing for smarter decisions. Each is driven by configurable constants (listed in ALL\_CAPS) used for tuning.

---

## Tuning Constants (ALL\_CAPS)

* **`BATTERY_SOC_NEEDED`**: Minimum SOC (%) required overnight under normal conditions.
* **`BAD_SUN_DAY_KEEP_SOC`**: Extra SOC (%) held if poor solar forecast for tomorrow.
* **`GOOD_SUN_DAY`**: Threshold for GTI sum (in 100s of W/m²) to qualify tomorrow as a good solar day.
* **`GOOD_SUN_HOUR`**: Per-hour GTI threshold (in 10s of W/m²) used to define "solar generation hours".

---

## Helper Rule Variables

| Variable               | Description                                                             |
| ---------------------- | ----------------------------------------------------------------------- |
| `current_hour`         | Current hour (0–23) from `interval_time`.                               |
| `hourly_gti_forecast`  | List of global tilted irradiance (GTI) values (W/m²) by hour.           |
| `hours_until_midnight` | Hours remaining in the current day.                                     |
| `gti_sum_tomorrow`     | Total GTI forecast from midnight onward (W/m²).                         |
| `night_reserve`        | Final minimum SOC (%) to retain overnight, adjusted dynamically.        |
| `first_good_gti`       | Index of first hour when GTI exceeds `GOOD_SUN_HOUR * 10`.              |
| `last_good_gti`        | Last index (today only) before GTI falls below threshold.               |
| `is_solar_window_now`  | `True` if current hour falls within forecasted solar production window. |
| `is_daytime`           | `True` if between today’s `sunrise` and `sunset`.                       |
| `soc_surplus`          | SOC (%) minus `night_reserve`. Positive = excess energy.                |
| `time_left`            | Hours remaining to charge/discharge (until sunset or sunrise).          |
| `projected_deficit`    | Forecasted SOC shortfall by sunrise, if discharging continues.          |

---
