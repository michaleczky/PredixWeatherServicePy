"""
This script runs the WeatherService application using a development server.
"""

from os import environ
from WeatherService import app

if __name__ == '__main__':
    HOST = environ.get('VCAP_APP_HOST', 'localhost')
    PORT = int(environ.get('VCAP_APP_PORT', '5555'))
    app.run(HOST, PORT)
