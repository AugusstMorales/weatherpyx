# weatherpyx/__init__.py
from .weather import WeatherAPI
from .config import Config

__version__ = "0.1.0"
__all__ = ["WeatherAPI", "Config"]