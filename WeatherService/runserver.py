"""
This script runs the WeatherService application using a development server.
"""

import json, settings, logging
from os import environ
from WeatherService import app

if __name__ == '__main__':
    logFormatStr = '[%(asctime)s] p%(process)s {%(pathname)s:%(lineno)d} %(levelname)s - %(message)s'
    logging.basicConfig(format = logFormatStr, filename = settings.LOG_FILE, level=settings.LOG_LEVEL)
    formatter = logging.Formatter(logFormatStr,'%m-%d %H:%M:%S')
    streamHandler = logging.StreamHandler()
    streamHandler.setLevel(logging.DEBUG)
    streamHandler.setFormatter(formatter)
    app.logger.addHandler(streamHandler)

    app.config.update({
        'SERVER_HOST': settings.SERVER_HOST,
        'SERVER_PORT': settings.SERVER_PORT,
    })
    app.run(settings.SERVER_HOST, int(settings.SERVER_PORT), debug = settings.DEBUG)