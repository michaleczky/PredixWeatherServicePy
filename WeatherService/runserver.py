"""
This script runs the WeatherService application using a development server.
"""

import json, settings, logging, sys
from os import environ
from WeatherService import app

if __name__ == '__main__':
    # setup the logging    
    logFormatStr = '[%(asctime)s] {%(pathname)s:%(lineno)d} %(levelname)s - %(message)s'
    logging.basicConfig(format = logFormatStr, stream = sys.stdout, level = settings.LOG_LEVEL)
    # start the app
    app.config.update({
        'SERVER_HOST': settings.SERVER_HOST,
        'SERVER_PORT': settings.SERVER_PORT,
    })
    app.run(settings.SERVER_HOST, int(settings.SERVER_PORT), debug = settings.DEBUG)