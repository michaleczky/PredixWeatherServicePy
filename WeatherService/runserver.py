"""
This script runs the WeatherService application using a development server.
"""

import json
from os import environ
from WeatherService import app, settings

if __name__ == '__main__':
    config = settings.get_as_dict()
    app.run(config['server.host'], config['server.port'])
