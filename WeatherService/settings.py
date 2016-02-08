import json, logging
from os import environ

# default settings for development and testing
DEBUG = True
DB_HOST = 'localhost'
DB_USERNAME = 'postgres'
DB_PASSWORD = 'postgres'
DB_DATABASE = 'WeatherDB'
SERVER_HOST = environ.get('SERVER_NAME', 'localhost')
SERVER_PORT = environ.get('SERVER_PORT', '8080')
    
# load database settings from the environment vars if the application is running in Cloud Foundry environment
if environ.get('VCAP_SERVICES'):
    DEBUG = False
    _env = json.loads(environ.get('VCAP_SERVICES'))    
    DB_DATABASE = _env['postgres'][0]['credentials']['database']
    DB_HOST = _env['postgres'][0]['credentials']['host']
    DB_PASSWORD = _env['postgres'][0]['credentials']['password']
    DB_PORT = _env['postgres'][0]['credentials']['port']
    DB_USERNAME = _env['postgres'][0]['credentials']['dsn']

#  load server settings from environment vars - or use default values (localhost:8080)
if environ.get('VCAP_APP_HOST'): SERVER_HOST = environ.get('VCAP_APP_HOST', 'localhost')
if environ.get('VCAP_APP_PORT'): SERVER_PORT = environ.get('VCAP_APP_PORT', '8080')

# log settings
LOG_FILE = "weatherservice.log"
LOG_LEVEL = logging.DEBUG if DEBUG else logging.WARN
