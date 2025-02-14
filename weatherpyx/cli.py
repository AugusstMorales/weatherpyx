# weatherpyx/cli.py
import typer
from rich.console import Console
from rich.table import Table
from rich.prompt import Prompt
from typing import Optional
from .weather import WeatherAPI
from .config import Config

app = typer.Typer()
console = Console()

def setup_api_key():
    config = Config()
    if not config.get_api_key():
        console.print("[yellow]No API key found. Let's set it up![/yellow]")
        api_key = Prompt.ask("Please enter your OpenWeatherMap API key")
        config.save_api_key(api_key)
        console.print("[green]API key saved successfully![/green]")
    return config.get_api_key()

@app.command()
def weather(city: str, units: str = "metric"):
    """Get current weather for a city"""
    api_key = setup_api_key()
    
    try:
        weather_api = WeatherAPI(api_key)
        weather_data = weather_api.get_weather(city, units)
        
        table = Table(title=f"Current Weather in {city}")
        table.add_column("Metric", style="cyan")
        table.add_column("Value", style="magenta")
        
        table.add_row("Temperature", f"{weather_data.temperature}°C")
        table.add_row("Feels Like", f"{weather_data.feels_like}°C")
        table.add_row("Humidity", f"{weather_data.humidity}%")
        table.add_row("Description", weather_data.description.capitalize())
        table.add_row("Wind Speed", f"{weather_data.wind_speed} m/s")
        
        console.print(table)
        
    except Exception as e:
        console.print(f"[red]Error: {str(e)}[/red]")

@app.command()
def forecast(city: str, units: str = "metric"):
    """Get 5-day forecast for a city"""
    api_key = setup_api_key()
    
    try:
        weather_api = WeatherAPI(api_key)
        forecast_data = weather_api.get_forecast(city, units)
        
        table = Table(title=f"5-Day Forecast for {city}")
        table.add_column("Date", style="cyan")
        table.add_column("Temperature", style="magenta")
        table.add_column("Description", style="green")
        
        for item in forecast_data["list"][::8]:  # Get one forecast per day
            date = item["dt_txt"].split()[0]
            temp = f"{item['main']['temp']}°C"
            desc = item["weather"][0]["description"].capitalize()
            table.add_row(date, temp, desc)
        
        console.print(table)
        
    except Exception as e:
        console.print(f"[red]Error: {str(e)}[/red]")

if __name__ == "__main__":
    app()