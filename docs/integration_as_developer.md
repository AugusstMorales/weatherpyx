# Integration as developer

This document provides basic examples of how to integrate and use the WeatherPyX library in your projects. For advanced usage, API reference, or contribution guidelines, please refer to the corresponding documents.

``` python
from weatherpyx import WeatherAPI

# Inicializar
weather = WeatherAPI()

# Obtener datos sin mostrarlos (para procesamiento)
data = weather.get_weather("Madrid", display=False)
print(f"Temperatura: {data.temperature}°C")
print(f"Humedad: {data.humidity}%")

# Obtener pronóstico como datos
forecast = weather.get_forecast("Madrid", display=False)
for day in forecast:
    print(f"Fecha: {day.date}, Temp: {day.temperature}°C")

``` 

- **Get current location and show weather:**
To use this example, you first need to install the additional dependencies:

``` bash

pip install weatherpyx geocoder rich

``` 

**This script:**

- Automatically detect your city using IP geolocation
- Shows the current weather at your location
- Shows the forecast for the next few days
- Handle errors elegantly
- It has a nice visual interface using Rich

You can also integrate it into your own code like this:

``` Python

from weatherpyx import WeatherAPI
import geocoder

# Obtener ubicación
g = geocoder.ip('me')
city = g.city

# Obtener clima
weather = WeatherAPI()
current_weather = weather.get_weather(city, display=False)

# Usar los datos como necesites
print(f"Temperatura en {city}: {current_weather.temperature}°C")

``` 
**Some important notes:**

- IP geolocation is not 100% accurate, but it is sufficient for this purpose
- Does not require special user permissions
- It is fast and does not consume many resources
- Works on any platform


**If you find any bugs or want to make improvements, you can:**

- Correct the code
- Update version in setup.py
- Re-upload to PyPI with a new version