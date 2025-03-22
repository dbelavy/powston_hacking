"""
Powston script for managing household battery
Note: individual requirements are highly variable. The only way to remove variability is to have a BIG battery. 1.5x your household usage is a good start.

In this script, the scructure is as follows:
* define constants - user defined
* define actions based state in some sort of user editable lookup table???
* validate variables received from Powston. Variables received from powston are received from third parties (eg Local Volts and AEMO) so they are flakey.
* 
* define functions that analyse the context 
* match the state to a preferred action
* error checking - not to be copied to powston
* rrp is in $/MWh

"""

# flake8: noqa

# constants

prepare_for_peak = [12, 13, 14, 15]
peak = [16, 17, 18, 19, 20]
sunniest_hours = [10,11,12,13,14]
always_sell_rrp = 1000.0
sell_min_hard = 30.0 # cents - never sell below this
buy_max_soft = 15.0 # cents - prefer to buy under this
buy_opport = 5.0 # cents
cyclone_mode = False
cyclone_reserve_soc = 70 # Reserve x% of battery for emergencies and self use. Don't export. Set to active with cyclone_mode = True
morning_padding = 1 # Hours after sunrise to consider as night

# Energy required for personal use. Don't export below this level Hour: % of battery
reserve_soc = {
    0: 10,
    1: 10,
    2: 10,
    3: 10,
    4: 10,
    5: 10,
    6: 10,
    7: 10,
    8: 10,
    9: 10,
    10: 10,
    11: 10,
    12: 60,
    13: 70,
    14: 80,
    15: 90,
    16: 80,
    17: 60,
    18: 40,
    19: 40,
    20: 30,
    21: 10,
    22: 10,
    23: 10,
}



# validate variables

# validate reason string
try:
    d_reason = f"Powston said:" + reason
except:
    d_reason = "Powston provided no reason string."

# passes the string back to reason
reason = d_reason

try:
    reason += f" Grid: {grid_power}. House power: {house_power}."
except:
    reason += f" Error getting grid power and house power."

# validate powston recommendations and set up default actions
try:
    valid_actions = ["stopped", "auto", "export", "import", "charge", "discharge"]
    valid_solar = ["maximize", "curtail"]
    if suggested_action in valid_actions:
        action = suggested_action
    else:
        action = "auto"
        reason += f" Invalid Powston action. Default to Auto."
    if suggested_solar in valid_solar:
        solar = suggested_solar
    else:
        solar = "maximize"
        reason += f" Invalid Powston solar. Defaulting."
except:
    action = "auto"
    solar = "maximize"
    reason += f" Error receiving Powston default actions."

reason += f" After Powston check Action: {action}, Solar: {solar}."

# validate variable: rrp_forecast (list) - NOT present - remove forecast



# try:
#     if forecast:
#         if len(forecast) != 0:
#             rrp_forecast = forecast
#         else:
#             reason += " RRP forecast is empty."
#     else:
#         reason += " RRP forecast not present."
# except:
#     reason += " Error getting RRP forecast."


# Validate variable: hour and month. Have had issues with time in the past.
try:
    month = interval_time.month
    hour = interval_time.hour

except:
    reason += " Error getting month and hour."
    month = 0
    hour = 25
    
reason += f" Month: {month}, Hour: {hour}"

# validate variable: sunrise_hour and sunset_hour

try:
    sunrise_hour = sunrise.hour
    sunset_hour = sunset.hour
except:
    sunrise_hour = 6
    sunset_hour = 18
    reason += " No Sunset or Sunrise - Defaulting to 6 and 18."

reason += f" Sunrise: {sunrise_hour}. Sunset: {sunset_hour}."


# set time of use periods - day/peak/night around sunrise and sunset
night = []
day = []

for i in range(0, 24):  # Note: range(0, 24) instead of range(0, 23) to include all 24 hours
    if i >= max(peak) or i <= (sunrise_hour+morning_padding):  # Use max() to get the maximum value of the peak list
        night.append(i)
    elif i < min(peak):  # Use min() to get the minimum value of the peak list
        day.append(i)
    else:
        pass # the rest will be peak set manually

# should now have: night, day and peak - lists
# validated: rrp_forecast (list)  ***NOT WORKING
# validated: sunrise_hour and sunset_hour
# Validated: hour and month
# validated: reason
# validated: default actions from powston



# this is historical data from 2023-2024 - use this for rrp and for z score.

QLD_HISTORICAL_PRICES = {1: {0: {'Average_RRP': 98.94, 'SD_RRP': 36.99},
     1: {'Average_RRP': 89.85, 'SD_RRP': 32.51},
     2: {'Average_RRP': 85.61, 'SD_RRP': 27.22},
     3: {'Average_RRP': 83.0, 'SD_RRP': 25.91},
     4: {'Average_RRP': 89.98, 'SD_RRP': 26.86},
     5: {'Average_RRP': 98.2, 'SD_RRP': 37.22},
     6: {'Average_RRP': 66.86, 'SD_RRP': 50.52},
     7: {'Average_RRP': 49.48, 'SD_RRP': 48.82},
     8: {'Average_RRP': 50.33, 'SD_RRP': 51.48},
     9: {'Average_RRP': 52.52, 'SD_RRP': 57.15},
     10: {'Average_RRP': 41.97, 'SD_RRP': 35.56},
     11: {'Average_RRP': 46.0, 'SD_RRP': 40.69},
     12: {'Average_RRP': 51.4, 'SD_RRP': 46.79},
     13: {'Average_RRP': 64.98, 'SD_RRP': 55.76},
     14: {'Average_RRP': 76.92, 'SD_RRP': 55.3},
     15: {'Average_RRP': 104.05, 'SD_RRP': 388.42},
     16: {'Average_RRP': 103.07, 'SD_RRP': 89.2},
     17: {'Average_RRP': 242.15, 'SD_RRP': 1056.05},
     18: {'Average_RRP': 890.99, 'SD_RRP': 2837.32},
     19: {'Average_RRP': 225.82, 'SD_RRP': 601.69},
     20: {'Average_RRP': 148.25, 'SD_RRP': 75.91},
     21: {'Average_RRP': 126.08, 'SD_RRP': 53.83},
     22: {'Average_RRP': 120.31, 'SD_RRP': 55.72},
     23: {'Average_RRP': 106.04, 'SD_RRP': 43.46}},
 2: {0: {'Average_RRP': 92.95, 'SD_RRP': 33.07},
     1: {'Average_RRP': 85.94, 'SD_RRP': 27.85},
     2: {'Average_RRP': 79.23, 'SD_RRP': 25.83},
     3: {'Average_RRP': 76.41, 'SD_RRP': 20.67},
     4: {'Average_RRP': 81.63, 'SD_RRP': 21.59},
     5: {'Average_RRP': 104.99, 'SD_RRP': 37.37},
     6: {'Average_RRP': 94.37, 'SD_RRP': 45.93},
     7: {'Average_RRP': 52.65, 'SD_RRP': 49.16},
     8: {'Average_RRP': 39.5, 'SD_RRP': 41.04},
     9: {'Average_RRP': 38.84, 'SD_RRP': 42.73},
     10: {'Average_RRP': 34.24, 'SD_RRP': 38.97},
     11: {'Average_RRP': 36.06, 'SD_RRP': 38.12},
     12: {'Average_RRP': 47.37, 'SD_RRP': 50.59},
     13: {'Average_RRP': 55.31, 'SD_RRP': 53.25},
     14: {'Average_RRP': 70.63, 'SD_RRP': 68.67},
     15: {'Average_RRP': 80.43, 'SD_RRP': 78.08},
     16: {'Average_RRP': 100.49, 'SD_RRP': 84.52},
     17: {'Average_RRP': 278.4, 'SD_RRP': 1215.57},
     18: {'Average_RRP': 411.39, 'SD_RRP': 1348.6},
     19: {'Average_RRP': 195.68, 'SD_RRP': 453.77},
     20: {'Average_RRP': 135.93, 'SD_RRP': 59.26},
     21: {'Average_RRP': 114.78, 'SD_RRP': 46.89},
     22: {'Average_RRP': 106.32, 'SD_RRP': 43.26},
     23: {'Average_RRP': 95.32, 'SD_RRP': 29.58}},
 3: {0: {'Average_RRP': 83.03, 'SD_RRP': 17.58},
     1: {'Average_RRP': 77.14, 'SD_RRP': 16.56},
     2: {'Average_RRP': 73.8, 'SD_RRP': 15.82},
     3: {'Average_RRP': 74.29, 'SD_RRP': 16.28},
     4: {'Average_RRP': 78.58, 'SD_RRP': 18.62},
     5: {'Average_RRP': 93.13, 'SD_RRP': 25.21},
     6: {'Average_RRP': 113.36, 'SD_RRP': 52.83},
     7: {'Average_RRP': 59.18, 'SD_RRP': 39.31},
     8: {'Average_RRP': 49.44, 'SD_RRP': 60.69},
     9: {'Average_RRP': 42.5, 'SD_RRP': 61.49},
     10: {'Average_RRP': 36.95, 'SD_RRP': 62.4},
     11: {'Average_RRP': 32.21, 'SD_RRP': 63.77},
     12: {'Average_RRP': 39.51, 'SD_RRP': 61.89},
     13: {'Average_RRP': 60.39, 'SD_RRP': 72.38},
     14: {'Average_RRP': 70.02, 'SD_RRP': 69.19},
     15: {'Average_RRP': 81.95, 'SD_RRP': 57.52},
     16: {'Average_RRP': 99.63, 'SD_RRP': 69.16},
     17: {'Average_RRP': 256.39, 'SD_RRP': 1064.22},
     18: {'Average_RRP': 413.53, 'SD_RRP': 1617.79},
     19: {'Average_RRP': 137.0, 'SD_RRP': 63.32},
     20: {'Average_RRP': 109.81, 'SD_RRP': 41.6},
     21: {'Average_RRP': 96.66, 'SD_RRP': 25.61},
     22: {'Average_RRP': 96.97, 'SD_RRP': 25.06},
     23: {'Average_RRP': 90.57, 'SD_RRP': 22.03}},
 4: {0: {'Average_RRP': 109.3, 'SD_RRP': 37.96},
     1: {'Average_RRP': 98.73, 'SD_RRP': 31.95},
     2: {'Average_RRP': 92.79, 'SD_RRP': 30.37},
     3: {'Average_RRP': 91.99, 'SD_RRP': 28.09},
     4: {'Average_RRP': 96.04, 'SD_RRP': 32.2},
     5: {'Average_RRP': 105.02, 'SD_RRP': 39.95},
     6: {'Average_RRP': 131.08, 'SD_RRP': 58.35},
     7: {'Average_RRP': 68.72, 'SD_RRP': 49.48},
     8: {'Average_RRP': 27.19, 'SD_RRP': 40.74},
     9: {'Average_RRP': 14.26, 'SD_RRP': 43.92},
     10: {'Average_RRP': 7.48, 'SD_RRP': 47.61},
     11: {'Average_RRP': 11.01, 'SD_RRP': 47.55},
     12: {'Average_RRP': 18.7, 'SD_RRP': 48.62},
     13: {'Average_RRP': 32.29, 'SD_RRP': 48.12},
     14: {'Average_RRP': 57.06, 'SD_RRP': 57.87},
     15: {'Average_RRP': 74.86, 'SD_RRP': 49.01},
     16: {'Average_RRP': 130.29, 'SD_RRP': 70.7},
     17: {'Average_RRP': 259.28, 'SD_RRP': 172.02},
     18: {'Average_RRP': 255.18, 'SD_RRP': 567.3},
     19: {'Average_RRP': 140.33, 'SD_RRP': 44.09},
     20: {'Average_RRP': 135.97, 'SD_RRP': 51.6},
     21: {'Average_RRP': 124.43, 'SD_RRP': 42.96},
     22: {'Average_RRP': 132.54, 'SD_RRP': 47.13},
     23: {'Average_RRP': 122.34, 'SD_RRP': 46.75}},
 5: {0: {'Average_RRP': 129.54, 'SD_RRP': 58.45},
     1: {'Average_RRP': 111.25, 'SD_RRP': 49.42},
     2: {'Average_RRP': 99.51, 'SD_RRP': 43.45},
     3: {'Average_RRP': 97.83, 'SD_RRP': 40.13},
     4: {'Average_RRP': 108.65, 'SD_RRP': 43.98},
     5: {'Average_RRP': 130.39, 'SD_RRP': 53.8},
     6: {'Average_RRP': 222.31, 'SD_RRP': 535.64},
     7: {'Average_RRP': 152.35, 'SD_RRP': 112.53},
     8: {'Average_RRP': 37.16, 'SD_RRP': 52.35},
     9: {'Average_RRP': 16.83, 'SD_RRP': 50.89},
     10: {'Average_RRP': -0.66, 'SD_RRP': 42.42},
     11: {'Average_RRP': 2.03, 'SD_RRP': 44.49},
     12: {'Average_RRP': 9.11, 'SD_RRP': 49.46},
     13: {'Average_RRP': 21.26, 'SD_RRP': 52.19},
     14: {'Average_RRP': 48.42, 'SD_RRP': 52.22},
     15: {'Average_RRP': 85.22, 'SD_RRP': 62.97},
     16: {'Average_RRP': 182.49, 'SD_RRP': 74.22},
     17: {'Average_RRP': 533.67, 'SD_RRP': 1783.82},
     18: {'Average_RRP': 310.91, 'SD_RRP': 985.13},
     19: {'Average_RRP': 175.24, 'SD_RRP': 61.72},
     20: {'Average_RRP': 169.73, 'SD_RRP': 61.55},
     21: {'Average_RRP': 149.77, 'SD_RRP': 59.9},
     22: {'Average_RRP': 159.31, 'SD_RRP': 59.02},
     23: {'Average_RRP': 138.8, 'SD_RRP': 50.85}},
 6: {0: {'Average_RRP': 108.88, 'SD_RRP': 51.72},
     1: {'Average_RRP': 98.35, 'SD_RRP': 43.74},
     2: {'Average_RRP': 90.57, 'SD_RRP': 42.08},
     3: {'Average_RRP': 88.14, 'SD_RRP': 42.78},
     4: {'Average_RRP': 95.65, 'SD_RRP': 48.92},
     5: {'Average_RRP': 111.49, 'SD_RRP': 61.84},
     6: {'Average_RRP': 178.26, 'SD_RRP': 578.21},
     7: {'Average_RRP': 165.45, 'SD_RRP': 103.86},
     8: {'Average_RRP': 73.33, 'SD_RRP': 58.91},
     9: {'Average_RRP': 41.9, 'SD_RRP': 56.88},
     10: {'Average_RRP': 18.28, 'SD_RRP': 54.71},
     11: {'Average_RRP': 10.65, 'SD_RRP': 51.86},
     12: {'Average_RRP': 6.87, 'SD_RRP': 53.81},
     13: {'Average_RRP': 17.3, 'SD_RRP': 56.04},
     14: {'Average_RRP': 49.04, 'SD_RRP': 63.47},
     15: {'Average_RRP': 80.9, 'SD_RRP': 63.83},
     16: {'Average_RRP': 162.3, 'SD_RRP': 76.19},
     17: {'Average_RRP': 354.72, 'SD_RRP': 1042.38},
     18: {'Average_RRP': 248.9, 'SD_RRP': 535.02},
     19: {'Average_RRP': 174.07, 'SD_RRP': 75.16},
     20: {'Average_RRP': 159.48, 'SD_RRP': 70.58},
     21: {'Average_RRP': 135.4, 'SD_RRP': 66.85},
     22: {'Average_RRP': 134.43, 'SD_RRP': 64.34},
     23: {'Average_RRP': 123.23, 'SD_RRP': 60.68}},
 7: {0: {'Average_RRP': 90.68, 'SD_RRP': 31.2},
     1: {'Average_RRP': 79.86, 'SD_RRP': 23.62},
     2: {'Average_RRP': 74.84, 'SD_RRP': 24.69},
     3: {'Average_RRP': 73.12, 'SD_RRP': 27.09},
     4: {'Average_RRP': 79.18, 'SD_RRP': 29.03},
     5: {'Average_RRP': 120.68, 'SD_RRP': 639.55},
     6: {'Average_RRP': 149.04, 'SD_RRP': 76.03},
     7: {'Average_RRP': 163.86, 'SD_RRP': 88.45},
     8: {'Average_RRP': 69.0, 'SD_RRP': 63.05},
     9: {'Average_RRP': 39.02, 'SD_RRP': 57.36},
     10: {'Average_RRP': 16.81, 'SD_RRP': 55.94},
     11: {'Average_RRP': 8.81, 'SD_RRP': 55.88},
     12: {'Average_RRP': 2.55, 'SD_RRP': 54.87},
     13: {'Average_RRP': 9.6, 'SD_RRP': 57.76},
     14: {'Average_RRP': 25.94, 'SD_RRP': 50.92},
     15: {'Average_RRP': 56.09, 'SD_RRP': 50.8},
     16: {'Average_RRP': 121.43, 'SD_RRP': 72.15},
     17: {'Average_RRP': 242.64, 'SD_RRP': 374.77},
     18: {'Average_RRP': 294.69, 'SD_RRP': 736.98},
     19: {'Average_RRP': 157.32, 'SD_RRP': 68.62},
     20: {'Average_RRP': 142.21, 'SD_RRP': 55.49},
     21: {'Average_RRP': 117.78, 'SD_RRP': 45.64},
     22: {'Average_RRP': 118.14, 'SD_RRP': 47.92},
     23: {'Average_RRP': 102.52, 'SD_RRP': 38.82}},
 8: {0: {'Average_RRP': 96.81, 'SD_RRP': 39.81},
     1: {'Average_RRP': 87.58, 'SD_RRP': 34.92},
     2: {'Average_RRP': 82.45, 'SD_RRP': 32.67},
     3: {'Average_RRP': 80.96, 'SD_RRP': 32.52},
     4: {'Average_RRP': 87.94, 'SD_RRP': 41.93},
     5: {'Average_RRP': 105.18, 'SD_RRP': 49.24},
     6: {'Average_RRP': 162.33, 'SD_RRP': 177.73},
     7: {'Average_RRP': 103.79, 'SD_RRP': 113.27},
     8: {'Average_RRP': 18.75, 'SD_RRP': 54.08},
     9: {'Average_RRP': 4.7, 'SD_RRP': 65.25},
     10: {'Average_RRP': -8.72, 'SD_RRP': 67.68},
     11: {'Average_RRP': -10.09, 'SD_RRP': 53.63},
     12: {'Average_RRP': -12.85, 'SD_RRP': 49.84},
     13: {'Average_RRP': -8.73, 'SD_RRP': 50.8},
     14: {'Average_RRP': 6.87, 'SD_RRP': 58.12},
     15: {'Average_RRP': 31.92, 'SD_RRP': 62.96},
     16: {'Average_RRP': 104.63, 'SD_RRP': 75.38},
     17: {'Average_RRP': 385.71, 'SD_RRP': 1549.03},
     18: {'Average_RRP': 384.2, 'SD_RRP': 1220.3},
     19: {'Average_RRP': 176.7, 'SD_RRP': 323.18},
     20: {'Average_RRP': 140.48, 'SD_RRP': 58.02},
     21: {'Average_RRP': 122.4, 'SD_RRP': 49.56},
     22: {'Average_RRP': 120.65, 'SD_RRP': 48.71},
     23: {'Average_RRP': 109.32, 'SD_RRP': 41.78}},
 9: {0: {'Average_RRP': 75.26, 'SD_RRP': 18.66},
     1: {'Average_RRP': 68.46, 'SD_RRP': 17.16},
     2: {'Average_RRP': 63.43, 'SD_RRP': 14.53},
     3: {'Average_RRP': 63.63, 'SD_RRP': 14.84},
     4: {'Average_RRP': 66.68, 'SD_RRP': 16.72},
     5: {'Average_RRP': 74.32, 'SD_RRP': 21.04},
     6: {'Average_RRP': 72.4, 'SD_RRP': 45.76},
     7: {'Average_RRP': 3.89, 'SD_RRP': 36.46},
     8: {'Average_RRP': -18.95, 'SD_RRP': 28.61},
     9: {'Average_RRP': -31.24, 'SD_RRP': 27.73},
     10: {'Average_RRP': -35.1, 'SD_RRP': 23.71},
     11: {'Average_RRP': -36.31, 'SD_RRP': 38.26},
     12: {'Average_RRP': -34.33, 'SD_RRP': 26.7},
     13: {'Average_RRP': -30.37, 'SD_RRP': 29.33},
     14: {'Average_RRP': -15.51, 'SD_RRP': 39.95},
     15: {'Average_RRP': -1.2, 'SD_RRP': 37.69},
     16: {'Average_RRP': 45.99, 'SD_RRP': 84.8},
     17: {'Average_RRP': 206.53, 'SD_RRP': 952.37},
     18: {'Average_RRP': 209.56, 'SD_RRP': 912.55},
     19: {'Average_RRP': 107.96, 'SD_RRP': 34.5},
     20: {'Average_RRP': 91.69, 'SD_RRP': 26.08},
     21: {'Average_RRP': 83.69, 'SD_RRP': 25.0},
     22: {'Average_RRP': 90.43, 'SD_RRP': 27.5},
     23: {'Average_RRP': 84.3, 'SD_RRP': 22.02}},
 10: {0: {'Average_RRP': 82.87, 'SD_RRP': 37.28},
      1: {'Average_RRP': 79.54, 'SD_RRP': 39.67},
      2: {'Average_RRP': 73.29, 'SD_RRP': 28.36},
      3: {'Average_RRP': 73.96, 'SD_RRP': 29.18},
      4: {'Average_RRP': 79.17, 'SD_RRP': 33.4},
      5: {'Average_RRP': 88.55, 'SD_RRP': 45.48},
      6: {'Average_RRP': 33.53, 'SD_RRP': 47.92},
      7: {'Average_RRP': -8.72, 'SD_RRP': 36.93},
      8: {'Average_RRP': -21.65, 'SD_RRP': 32.23},
      9: {'Average_RRP': -30.31, 'SD_RRP': 25.07},
      10: {'Average_RRP': -32.88, 'SD_RRP': 23.75},
      11: {'Average_RRP': -33.18, 'SD_RRP': 24.34},
      12: {'Average_RRP': -31.47, 'SD_RRP': 25.23},
      13: {'Average_RRP': -23.95, 'SD_RRP': 32.47},
      14: {'Average_RRP': -5.49, 'SD_RRP': 48.82},
      15: {'Average_RRP': 17.13, 'SD_RRP': 52.4},
      16: {'Average_RRP': 55.22, 'SD_RRP': 50.77},
      17: {'Average_RRP': 188.3, 'SD_RRP': 676.65},
      18: {'Average_RRP': 193.63, 'SD_RRP': 370.89},
      19: {'Average_RRP': 123.31, 'SD_RRP': 56.59},
      20: {'Average_RRP': 104.0, 'SD_RRP': 51.34},
      21: {'Average_RRP': 90.49, 'SD_RRP': 45.35},
      22: {'Average_RRP': 106.19, 'SD_RRP': 62.29},
      23: {'Average_RRP': 93.23, 'SD_RRP': 52.49}},
 11: {0: {'Average_RRP': 114.86, 'SD_RRP': 57.83},
      1: {'Average_RRP': 101.03, 'SD_RRP': 45.29},
      2: {'Average_RRP': 98.18, 'SD_RRP': 47.76},
      3: {'Average_RRP': 100.52, 'SD_RRP': 78.47},
      4: {'Average_RRP': 106.67, 'SD_RRP': 57.82},
      5: {'Average_RRP': 110.18, 'SD_RRP': 91.96},
      6: {'Average_RRP': 61.14, 'SD_RRP': 164.28},
      7: {'Average_RRP': 48.68, 'SD_RRP': 66.19},
      8: {'Average_RRP': 36.55, 'SD_RRP': 65.94},
      9: {'Average_RRP': 24.06, 'SD_RRP': 67.11},
      10: {'Average_RRP': 13.31, 'SD_RRP': 52.42},
      11: {'Average_RRP': 14.55, 'SD_RRP': 53.46},
      12: {'Average_RRP': 17.81, 'SD_RRP': 53.97},
      13: {'Average_RRP': 31.83, 'SD_RRP': 60.51},
      14: {'Average_RRP': 50.5, 'SD_RRP': 73.51},
      15: {'Average_RRP': 80.04, 'SD_RRP': 381.49},
      16: {'Average_RRP': 152.94, 'SD_RRP': 671.25},
      17: {'Average_RRP': 486.75, 'SD_RRP': 1779.55},
      18: {'Average_RRP': 561.1, 'SD_RRP': 2185.45},
      19: {'Average_RRP': 257.61, 'SD_RRP': 1110.25},
      20: {'Average_RRP': 143.83, 'SD_RRP': 64.95},
      21: {'Average_RRP': 133.56, 'SD_RRP': 68.4},
      22: {'Average_RRP': 133.21, 'SD_RRP': 64.71},
      23: {'Average_RRP': 126.51, 'SD_RRP': 65.15}},
 12: {0: {'Average_RRP': 117.8, 'SD_RRP': 55.83},
      1: {'Average_RRP': 115.38, 'SD_RRP': 56.7},
      2: {'Average_RRP': 104.74, 'SD_RRP': 54.44},
      3: {'Average_RRP': 102.0, 'SD_RRP': 51.72},
      4: {'Average_RRP': 106.39, 'SD_RRP': 52.22},
      5: {'Average_RRP': 99.87, 'SD_RRP': 58.16},
      6: {'Average_RRP': 43.74, 'SD_RRP': 49.63},
      7: {'Average_RRP': 38.89, 'SD_RRP': 57.73},
      8: {'Average_RRP': 31.96, 'SD_RRP': 62.99},
      9: {'Average_RRP': 21.26, 'SD_RRP': 63.02},
      10: {'Average_RRP': 17.31, 'SD_RRP': 58.53},
      11: {'Average_RRP': 19.52, 'SD_RRP': 62.58},
      12: {'Average_RRP': 22.63, 'SD_RRP': 67.77},
      13: {'Average_RRP': 42.46, 'SD_RRP': 76.22},
      14: {'Average_RRP': 69.43, 'SD_RRP': 178.38},
      15: {'Average_RRP': 82.62, 'SD_RRP': 89.0},
      16: {'Average_RRP': 108.96, 'SD_RRP': 94.92},
      17: {'Average_RRP': 237.31, 'SD_RRP': 934.73},
      18: {'Average_RRP': 521.94, 'SD_RRP': 1841.67},
      19: {'Average_RRP': 245.34, 'SD_RRP': 682.66},
      20: {'Average_RRP': 162.76, 'SD_RRP': 74.22},
      21: {'Average_RRP': 138.45, 'SD_RRP': 59.74},
      22: {'Average_RRP': 144.83, 'SD_RRP': 66.86},
      23: {'Average_RRP': 133.67, 'SD_RRP': 63.06}}}



# validate RRP. If it's not available, use the historical average

try: 
    rrp = float(rrp)
except:
    rrp = QLD_HISTORICAL_PRICES[month][hour]['Average_RRP']
    reason += f" RRP exception, default to historical."

reason += f" RRP: {rrp}."

# should now have: night, day and peak - lists
# validated: rrp_forecast (list) ***NOT WORKING
# validated: sunrise_hour and sunset_hour
# Validated: hour and month
# validated: rrp
# validated: reason
# validated: default actions from powston


# # validate threshold_1, threshold_2, threshold_3  

# flake8: noqa
# Validate thresholds (threshold_1, threshold_2, threshold_3)

try:
    reason += " Charge threshold validation."
    thresholds = {
        "Threshold_1": threshold_1,
        "Threshold_2": threshold_2,
        "Threshold_3": threshold_3,
    }
    for name, value in thresholds.items():
        if isinstance(value, (float, int)) and value == value:  # Check for valid type and not NaN
            reason += f" {name}: {value:.2f}. "
        else:
            reason += f" {name} is not a valid number. "
except NameError as e:
    reason += f"A threshold variable is not defined: {e}"

# validate thresholds


"""
Calculate the z-score for a given RRP value based on historical data for the same month and hour.

   rrp (float): The RRP value to calculate the z-score for.
    month (int): The month of the year (1-12) for the RRP value.
    hour (int): The hour of the day (0-23) for the RRP value.

"""
try:
    historical_rrp = float(QLD_HISTORICAL_PRICES[month][hour]['Average_RRP'])
    historical_sd_rrp = float(QLD_HISTORICAL_PRICES [month][hour]['SD_RRP'])
    if historical_sd_rrp == 0:
        z_score = 0.0 # 
    else:
        z_score = float((rrp - historical_rrp) / historical_sd_rrp)
    reason += f" Z-Score: {z_score:.2f}. Historical RRP: {historical_rrp}, SD: {historical_sd_rrp}."
    if month == 1:
        reason += " January is time to updated historical prices with new data."


except:
    z_score = 0.0
    reason += f" Z score failed, set to {z_score}."



# should now have: night, day and peak - lists
# validated: rrp_forecast (list)
# validated: sunrise_hour and sunset_hour
# Validated: hour and month
# validated: rrp
# calculated: z_score
# looked up: historical_rrp, historical_sd_rrp
# validated: reason
# validated: default actions from powston


# validate variable: buy_forecast (list)
try:
    if not isinstance(buy_forecast, list):
        reason += " buy_forecast is not a list. "
    elif not buy_forecast:  # Check if the list is empty
        reason += " buy_forecast list is empty. "
    else:
        avg_future_buy = (sum(buy_forecast[0:4]) / 4 )
        reason += f" Avg buy over next 4 epochs: {avg_future_buy:.2f}."

except:
    reason += " Error validating buy_forecast. "


# should now have: night, day and peak - lists
# validated: rrp_forecast (list)
# validated: sunrise_hour and sunset_hour
# Validated: hour and month
# validated: rrp
# calculated: z_score
# looked up: historical_rrp, historical_sd_rrp
# validated: reason
# validated: default actions from powston
# validated: buy_forecast list and added avg_future_buy for next 2 hours.


# validate buy_price and sell_price.


try:
    # Validate buy_price
    if isinstance(buy_price, (float, int)) and buy_price == buy_price:  # Check for valid type and not NaN
        reason += f" buy_price: {buy_price:.2f}. "
    else:
        reason += " buy_price is not a valid number. "
    # Validate sell_price
    if isinstance(sell_price, (float, int)) and sell_price == sell_price:  # Check for valid type, positive, and not NaN
        reason += f" sell_price: {sell_price:.2f}. "
    else:
        reason += " sell_price is not a valid number. "
except Exception as e:
    reason += f" Error validating buy_price or sell_price: {e}. "

# should now have: night, day and peak - lists
# validated: rrp_forecast (list)
# validated: sunrise_hour and sunset_hour
# Validated: hour and month
# validated: rrp
# calculated: z_score
# looked up: historical_rrp, historical_sd_rrp
# validated: reason
# validated: default actions from powston
# validated: buy_forecast list and added avg_future_buy for next 2 hours.
# validated: buy_price and sell_price.


# flake8: noqa

# validate history_buy_prices
try:
    # Validate history_buy_prices
    if not isinstance(history_buy_prices, list):  # Ensure it's a list
        reason += " History_buy_prices is not a valid list. "
    else:
        for price in history_buy_prices:
            if not isinstance(price, (float, int)) or price != price:  # Check for numbers and exclude NaN
                reason += " Elements of history_buy_prices are errors."
                break  # Stop checking further if an invalid price is found
        else:
            reason += " History_buy_prices valid. "
            # history_buy_prices is a list calculate average of last 1 hour for the last 12 elements of historical_buy_prices
            last_hour_average = sum(history_buy_prices[-12:])/12
            reason += f" Last 1 hour average price: {last_hour_average:.2f}"

except Exception as e:
    reason += f" Error validating buy_prices: {e}. "


# should now have: night, day and peak - lists
# validated: rrp_forecast (list)
# validated: sunrise_hour and sunset_hour
# Validated: hour and month
# validated: rrp
# calculated: z_score
# looked up: historical_rrp, historical_sd_rrp
# validated: reason
# validated: default actions from powston
# validated: buy_forecast list and added avg_future_buy for next 2 hours.
# validated: buy_price and sell_price.
# validated: history_buy_prices and created last_hour_average


# I define a spike as sell_price > historical and future buy prices.

is_spiking = False

if sell_price > last_hour_average and sell_price > avg_future_buy:
    is_spiking = True
    reason += " Price is spiking. Consider selling."
else:
    reason += " Not spiking."


# should now have: night, day and peak - lists
# validated: rrp_forecast (list)
# validated: sunrise_hour and sunset_hour
# Validated: hour and month
# validated: rrp
# calculated: z_score
# looked up: historical_rrp, historical_sd_rrp
# validated: reason
# validated: default actions from powston
# validated: buy_forecast list and added avg_future_buy for next 2 hours.
# validated: buy_price and sell_price.
# validated: history_buy_prices and created last_hour_average
# created: is_spiking






# flake8: noqa
# validate battery_soc
try:
    if isinstance(battery_soc, (float, int)) and battery_soc == battery_soc:  # Check for valid type and not NaN
        reason += f" Battery_soc: {battery_soc:.2f}."
    else:
        reason += " Battery_soc is not a valid number."
except Exception as e:
    reason += f" Error validating battery_soc: {e}. "

# should now have: night, day and peak - lists
# validated: rrp_forecast (list)
# validated: sunrise_hour and sunset_hour
# Validated: hour and month
# validated: rrp
# calculated: z_score
# looked up: historical_rrp, historical_sd_rrp
# validated: reason
# validated: default actions from powston
# validated: buy_forecast list and added avg_future_buy for next 2 hours.
# validated: buy_price and sell_price.
# validated: history_buy_prices and created last_hour_average
# created: is_spiking
# validated battery_soc



# Find out if I have spare energy for export

try:
    # Look up reserve SOC - depending on cyclone mode
    soc_reserve = int(reserve_soc[hour]) if not cyclone_mode else cyclone_reserve_soc
    surplus_energy = False  # Default setting

    if cyclone_mode:  # Cyclone mode active
        if battery_soc > soc_reserve:
            surplus_energy = True
        reason += f" Cyclone mode reserve: {soc_reserve}. Surplus energy: {surplus_energy}. "

    elif battery_soc < soc_reserve:  # Non-cyclone mode, SOC below reserve
        reason += f" SOC below reserve. Reserve SOC: {soc_reserve}. Surplus energy: {surplus_energy}. "

    else:  # Non-cyclone mode, SOC is enough for surplus
        surplus_energy = True
        reason += f" Min SOC: {soc_reserve}. Surplus energy: {surplus_energy}. "

except KeyError as e:
    reason += f" Error: Reserve SOC not found for hour {hour}. {e}. "
except ValueError as e:
    reason += f" Error: Invalid reserve SOC value. {e}. "
except Exception as e:
    reason += f" Unexpected error: {e}. "

# should now have: night, day and peak - lists
# validated: rrp_forecast (list)
# validated: sunrise_hour and sunset_hour
# Validated: hour and month
# validated: rrp
# calculated: z_score
# looked up: historical_rrp, historical_sd_rrp
# validated: reason
# validated: default actions from powston
# validated: buy_forecast list and added avg_future_buy for next 2 hours.
# validated: buy_price and sell_price.
# validated: history_buy_prices and created last_hour_average
# created: is_spiking
# validated battery_soc
# created: soc_reserve (not for later use)
# added variable "surplus_energy"

# flake8: noqa



# DECISION MAKING BELOW HERE
# depends on time of day (hour), surplus energy, is_spiking, zscore
# always_sell_rrp = 1000
# sell_min_hard = 30 # cents - never sell below this
# buy_max_soft = 15 # cents - prefer to buy under this
# buy_opport = 5 # cents


# Define the decision logic without using a state dictionary
# needed to do late binding of variables for Powston's system.
# needed to do late binding of variables for Powston's system.
# Define the decision options without functions
# Debug version - print each condition and result
# Create a single check function that takes all necessary params and a condition number
# Simple sequential decision logic

if (rrp<threshold_1 and battery_soc<100 and hour in sunniest_hours):
    action = 'import'
    solar = 'maximize'
    reason += ' RRP below threshold 1 in sunny hour.'
elif (buy_price < buy_opport) and battery_soc<100:
    action = 'import'
    solar = 'maximize'
    reason += f' Buy price below {buy_opport}c.'
elif (rrp > always_sell_rrp) and surplus_energy:
    action = 'export'
    solar = 'maximize'
    reason += f' RRP > ${always_sell_rrp}/MWh. Opportunistic sell.'
elif is_spiking and buy_price > sell_min_hard and surplus_energy:
    action = 'export'
    solar = 'maximize'
    reason += ' Price spike and surplus.'
elif (rrp < threshold_2 and (hour in sunniest_hours) and (battery_soc<100) and buy_price < buy_max_soft):
    action = 'import'
    solar = 'maximize'
    reason += ' Price below threshold 2 AND buy_max_soft - import'
elif (hour in day) and buy_price < buy_max_soft:
    action = 'charge'
    solar = 'maximize'
    reason += ' Daytime charge below soft max buy price.'
elif (hour in prepare_for_peak) and not surplus_energy:
    action = 'import'
    solar = 'maximize'
    reason += ' Afternoon charge before peak regardless of price'
elif (hour in peak) and surplus_energy and sell_price > sell_min_hard:
    action = 'export'
    solar = 'maximize'
    reason += ' Peak sell price above sell threshold and surplus.'
elif (hour in night) and buy_price < buy_max_soft:
    action = 'charge'
    solar = 'maximize'
    reason += ' Nighttime low price. Use grid.'
#elif (hour in peak) and hour >= sunset_hour:
##    action = 'export'
#    solar = 'curtail'
#    feed_in_power_limitation = 200
#    reason += f" Export 200 for evening."
else:
    action = 'auto'
    solar = 'maximize'
    reason += ' Default behavior;'
reason += f" Final action: {action}. Final solar: {solar}."

