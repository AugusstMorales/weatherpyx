# test_weather.py
from weatherpyx.weather import WeatherAPI
from weatherpyx.config import Config
from rich.console import Console

console = Console()

def main():
    # Primero, asegurémonos de que tenemos una API key
    config = Config()
    
    # Forzar la solicitud de una nueva API key
    console.print("[yellow]Por favor, ingresa tu API key de OpenWeatherMap[/yellow]")
    api_key = input("API Key: ").strip()
    
    # Guardar la nueva API key
    config.save_api_key(api_key)
    
    # Crear instancia de WeatherAPI
    weather = WeatherAPI()

    try:
        # Obtener clima actual
        current = weather.get_weather("Madrid")
        print("\nClima actual en Madrid:")
        print(f"Temperatura: {current.temperature}°C")
        print(f"Sensación térmica: {current.feels_like}°C")
        print(f"Humedad: {current.humidity}%")
        print(f"Descripción: {current.description}")
        print(f"Velocidad del viento: {current.wind_speed} m/s")
        
        # Obtener pronóstico
        forecast = weather.get_forecast("Madrid")
        print("\nPronóstico para los próximos días:")
        for item in forecast["list"][::8]:  # Un registro por día
            print(f"Fecha: {item['dt_txt']}, Temperatura: {item['main']['temp']}°C")
            
    except Exception as e:
        pass

if __name__ == "__main__":
    main()