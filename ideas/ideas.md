Integrating weather data.

Pull data from Bureau of Meteorology

Note: API times may be long and could slow down your switching!


import sys
from weather_au import api

w = api.WeatherApi(search='parkville+vic', debug=0)

location = w.location()

# check if the search produced a result (other methods will also return None if the search fails).
if location is None:
    sys.exit('Search failed for location ' + loc)

print(f"\nLocation: {location['name']} {location['state']}, timezone:{location['timezone']}\n")

for warn in w.warnings():
    print(f"Warning short title:  {warn['short_title']}")

    warning = w.warning(id=warn['id'])
    print(f"Warning title:        {warning['title']}")

observations = w.observations()
print(f"\nObservations (temp): {observations['temp']:2}")

forecast_rain = w.forecast_rain()
print(f"Forecast Rain:       amount:{forecast_rain['amount']}, chance:{forecast_rain['chance']}")

print('\n3 Hourly:')
for f in w.forecasts_3hourly():
    print(f"{f['time']} temp:{f['temp']:2}, {f['icon_descriptor']}")




My location is "Brisbane, Qld"



