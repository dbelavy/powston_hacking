import python_weather
import asyncio
import os

async def get_weather():
    async with python_weather.Client(unit=python_weather.METRIC) as client:
        # Fetch weather for Sydney
        weather = await client.get('Brisbane, Australia')
        
        print(f"Current temperature: {weather.temperature}°C")
        
        # In python-weather, we iterate directly over the weather object
        for forecast in weather:
            print(f"\nDate: {forecast.date}")
            print(f"Max temp: {forecast.highest_temperature}°C")
            print(f"Min temp: {forecast.lowest_temperature}°C")
            print(f"Moon phase: {forecast.moon_phase}")
            
            if forecast.sunrise:
                print(f"Sunrise: {forecast.sunrise}")
            if forecast.sunset:
                print(f"Sunset: {forecast.sunset}")


               
        # Print all available attributes and methods
        print("\nAll attributes and methods:")
        print(dir(weather))
        
        # Try to print the object's dictionary
        print("\nObject variables:")
        try:
            pprint(vars(weather))
        except:
            print("Cannot print vars(weather)")
            
        # Print the raw object
        print("\nRaw object:")
        print(weather)
        
        # Print object representation
        print("\nObject representation:")
        print(repr(weather))
        
        # Iterate and print each attribute we can access
        print("\nTrying to access each attribute:")
        for attr in dir(weather):
            if not attr.startswith('_'):  # Skip private attributes
                try:
                    value = getattr(weather, attr)
                    print(f"{attr}: {value}")
                except:
                    print(f"Cannot access {attr}")

if __name__ == '__main__':
    # Fix for Windows event loop policy
    if os.name == 'nt':
        asyncio.set_event_loop_policy(asyncio.WindowsSelectorEventLoopPolicy())
    
    asyncio.run(get_weather())