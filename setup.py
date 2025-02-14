# setup.py
from setuptools import setup, find_packages

setup(
    name="weatherpyx",
    version="0.1.0",
    packages=find_packages(),
    install_requires=[
        "rich>=10.0.0",
        "requests>=2.25.1",
        "python-dotenv>=0.19.0",
        "typer>=0.4.0",
        "pydantic>=2.0.0"
    ],
    entry_points={
        "console_scripts": [
            "weatherpyx=weatherpyx.cli:app"
        ]
    },
    author="AugusstMorales",
    author_email="augustodevelop.py@gmail.com",
    description="A simple and intuitive OpenWeatherMap API wrapper with CLI interface",
    long_description=open("README.md").read(),
    long_description_content_type="text/markdown",
    url="https://github.com/AugusstMorales/weatherpyx",
    classifiers=[
        "Programming Language :: Python :: 3",
        "License :: OSI Approved :: MIT License",
        "Operating System :: OS Independent",
    ],
    python_requires=">=3.7",
)