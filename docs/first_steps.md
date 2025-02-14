# First steps

To use this library we are going to create a new virtual environment and install it like any user:

- Create and activate a new virtual environment (for clean testing):

``` bash

# Crear nuevo directorio de prueba
mkdir test_weatherpyx
cd test_weatherpyx

# Crear entorno virtual
python -m venv venv

# Activar el entorno virtual
# En Linux/Mac:
source venv/bin/activate
# En Windows:
# venv\Scripts\activate

```
- Create a test file **(test.py)**:

``` bash
touch test.py
```

``` bash
from weatherpyx import WeatherAPI

def main():
    # Creará una instancia y pedirá la API key si no existe
    weather = WeatherAPI()
    
    # Probar el clima actual
    weather.get_weather("Madrid")
    
    # Probar el pronóstico
    weather.get_forecast("Madrid")

if __name__ == "__main__":
    main()

```

- Run the test:

``` bash
python test.py

``` 
- **You can also try the command line interface directly:**

``` bash
# Ver el clima actual
weatherpyx weather "Madrid"

# Ver el pronóstico
weatherpyx forecast "Madrid"

``` 

**If you find any bugs or want to make improvements, you can:**

- Correct the code
- Update version in setup.py
- Re-upload to PyPI with a new version