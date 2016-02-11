import settings
import logging
import datetime
from lib import database, weatherdata
from WeatherService import app

# setup the logging
logFormatStr = '[%(asctime)s] p%(process)s {%(pathname)s:%(lineno)d} %(levelname)s - %(message)s'
logging.basicConfig(format = logFormatStr, filename = settings.LOG_FILE, level=settings.LOG_LEVEL)
formatter = logging.Formatter(logFormatStr,'%m-%d %H:%M:%S')
streamHandler = logging.StreamHandler()
streamHandler.setLevel(logging.DEBUG)
streamHandler.setFormatter(formatter)
app.logger.addHandler(streamHandler)

# create database if not exists - just an open connection needed for that
conn = database.get_connection()    
try:
    conn = database.get_connection()    
except:
    app.logger.error('Can\'t connect to the database.')

# request data from weather webservice and stores in the db
for city in settings.OPENWEATHERMAP_CITIES:
    resp = weatherdata.query_weather_data(city)
    weatherdata.load_data(resp)
