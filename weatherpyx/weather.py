# weatherpyx/weather.py
from typing import Dict, Optional, List
import requests
from datetime import datetime
from pydantic import BaseModel
from rich.console import Console
from rich.table import Table
from rich.panel import Panel
from rich.layout import Layout
from rich.text import Text
from rich import box
from .config import Config

console = Console()

class WeatherData(BaseModel):
    temperature: float
    feels_like: float
    humidity: int
    description: str
    wind_speed: float
    city: str
    country: str
    sunrise: datetime
    sunset: datetime
    pressure: int
    visibility: float

class ForecastItem(BaseModel):
    date: datetime
    temperature: float
    feels_like: float
    humidity: int
    description: str
    wind_speed: float

class WeatherAPI:
    BASE_URL = "http://api.openweathermap.org/data/2.5"
    
    def __init__(self, api_key: Optional[str] = None):
        """
        Inicializa WeatherAPI.
        
        Args:
            api_key (Optional[str]): API key de OpenWeatherMap. 
                                   Si no se proporciona, se buscará en las variables de entorno
                                   o se solicitará al usuario.
        """
        self.config = Config()
        if api_key:
            self.config.save_api_key(api_key)
        self.api_key = self.config.get_api_key()

    def _make_request(self, endpoint: str, params: Dict) -> Dict:
        """Método auxiliar para hacer peticiones a la API"""
        try:
            response = requests.get(f"{self.BASE_URL}/{endpoint}", params=params)
            response.raise_for_status()
            return response.json()
        except requests.exceptions.HTTPError as http_err:
            if response.status_code == 401:
                console.print(Panel("[red]Error: API key inválida. Por favor, verifica tu API key.[/red]", 
                                  title="Error de Autenticación"))
            elif response.status_code == 404:
                console.print(Panel("[red]Error: Ciudad no encontrada.[/red]", 
                                  title="Error de Búsqueda"))
            else:
                console.print(Panel(f"[red]Error HTTP: {http_err}[/red]", 
                                  title="Error de Conexión"))
            raise
        except requests.exceptions.ConnectionError:
            console.print(Panel("[red]Error: No se pudo conectar con el servidor. Verifica tu conexión a internet.[/red]", 
                              title="Error de Conexión"))
            raise
        except Exception as e:
            console.print(Panel(f"[red]Error inesperado: {str(e)}[/red]", 
                              title="Error"))
            raise

    def get_weather(self, city: str, units: str = "metric", display: bool = True) -> WeatherData:
        """
        Obtiene el clima actual para una ciudad.
        
        Args:
            city (str): Nombre de la ciudad
            units (str): Unidades de medida ('metric', 'imperial', 'standard')
            display (bool): Si es True, muestra los resultados en consola
        
        Returns:
            WeatherData: Objeto con los datos del clima
        """
        params = {
            "q": city,
            "appid": self.api_key,
            "units": units
        }
        
        data = self._make_request("weather", params)
        
        weather_data = WeatherData(
            temperature=data["main"]["temp"],
            feels_like=data["main"]["feels_like"],
            humidity=data["main"]["humidity"],
            description=data["weather"][0]["description"],
            wind_speed=data["wind"]["speed"],
            city=data["name"],
            country=data["sys"]["country"],
            sunrise=datetime.fromtimestamp(data["sys"]["sunrise"]),
            sunset=datetime.fromtimestamp(data["sys"]["sunset"]),
            pressure=data["main"]["pressure"],
            visibility=data["visibility"] / 1000  # Convertir a km
        )

        if display:
            self._display_current_weather(weather_data, units)
        
        return weather_data

    def get_forecast(self, city: str, units: str = "metric", display: bool = True) -> List[ForecastItem]:
        """
        Obtiene el pronóstico del tiempo para 5 días.
        
        Args:
            city (str): Nombre de la ciudad
            units (str): Unidades de medida ('metric', 'imperial', 'standard')
            display (bool): Si es True, muestra los resultados en consola
        
        Returns:
            List[ForecastItem]: Lista de pronósticos
        """
        params = {
            "q": city,
            "appid": self.api_key,
            "units": units
        }
        
        data = self._make_request("forecast", params)
        
        forecast_items = []
        for item in data["list"][::8]:  # Un registro por día
            forecast_item = ForecastItem(
                date=datetime.fromtimestamp(item["dt"]),
                temperature=item["main"]["temp"],
                feels_like=item["main"]["feels_like"],
                humidity=item["main"]["humidity"],
                description=item["weather"][0]["description"],
                wind_speed=item["wind"]["speed"]
            )
            forecast_items.append(forecast_item)

        if display:
            self._display_forecast(forecast_items, city, units)
        
        return forecast_items

    def _display_current_weather(self, weather: WeatherData, units: str):
        """Muestra el clima actual usando Rich"""
        # Determinar unidad de temperatura
        temp_unit = "°C" if units == "metric" else "°F" if units == "imperial" else "K"
        
        # Crear layout
        layout = Layout()
        layout.split_column(
            Layout(name="main"),
            Layout(name="details")
        )

        # Panel principal
        main_text = Text.assemble(
            (f"\n🌍 {weather.city}, {weather.country}\n", "bold cyan"),
            (f"\n🌡️  Temperatura: {weather.temperature}{temp_unit}\n", "yellow"),
            (f"🤔 Sensación térmica: {weather.feels_like}{temp_unit}\n", "yellow"),
            (f"☁️  {weather.description.capitalize()}\n", "bold white"),
        )
        layout["main"].update(Panel(main_text, title="Clima Actual", border_style="cyan"))

        # Tabla de detalles
        table = Table(box=box.ROUNDED, show_header=False, border_style="blue")
        table.add_column("Métrica", style="cyan")
        table.add_column("Valor", style="yellow")
        
        table.add_row("💧 Humedad", f"{weather.humidity}%")
        table.add_row("💨 Viento", f"{weather.wind_speed} m/s")
        table.add_row("👁️  Visibilidad", f"{weather.visibility:.1f} km")
        table.add_row("⬆️ Amanecer", weather.sunrise.strftime("%H:%M"))
        table.add_row("⬇️ Atardecer", weather.sunset.strftime("%H:%M"))
        table.add_row("🎯 Presión", f"{weather.pressure} hPa")

        layout["details"].update(Panel(table, title="Detalles", border_style="blue"))
        
        console.print(layout)

    def _display_forecast(self, forecast: List[ForecastItem], city: str, units: str):
        """Muestra el pronóstico usando Rich"""
        temp_unit = "°C" if units == "metric" else "°F" if units == "imperial" else "K"
        
        table = Table(
            title=f"Pronóstico de 5 días para {city}",
            box=box.ROUNDED,
            show_header=True,
            header_style="bold cyan"
        )
        
        table.add_column("Fecha", style="cyan")
        table.add_column("Temp", justify="right", style="yellow")
        table.add_column("St", justify="right", style="yellow")
        table.add_column("Humedad", justify="right", style="blue")
        table.add_column("Viento", justify="right", style="green")
        table.add_column("Descripción", style="magenta")

        for item in forecast:
            table.add_row(
                item.date.strftime("%Y-%m-%d"),
                f"{item.temperature}{temp_unit}",
                f"{item.feels_like}{temp_unit}",
                f"{item.humidity}%",
                f"{item.wind_speed} m/s",
                item.description.capitalize()
            )

        console.print(Panel.fit(table, border_style="cyan"))