# weatherpyx/config.py
import os
from pathlib import Path
from dotenv import load_dotenv
from rich.prompt import Prompt
from rich.console import Console

console = Console()

class Config:
    def __init__(self):
        self.config_dir = Path.home() / ".weatherpyx"
        self.config_file = self.config_dir / ".env"
        self._ensure_config_dir()
        load_dotenv(self.config_file)

    def _ensure_config_dir(self):
        self.config_dir.mkdir(exist_ok=True)
        if not self.config_file.exists():
            self.config_file.touch()

    def save_api_key(self, api_key: str):
        with open(self.config_file, "w") as f:
            f.write(f"OPENWEATHER_API_KEY={api_key}")
        os.environ["OPENWEATHER_API_KEY"] = api_key

    def get_api_key(self) -> str:
        api_key = os.getenv("OPENWEATHER_API_KEY")
        if not api_key:
            console.print("[yellow]No se encontró una API key. Por favor, ingresa tu API key de OpenWeatherMap.[/yellow]")
            api_key = Prompt.ask("OpenWeatherMap API key")
            self.save_api_key(api_key)
            console.print("[green]¡API key guardada exitosamente![/green]")
        return api_key