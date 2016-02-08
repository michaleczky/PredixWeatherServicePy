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
cities = (3054643, 3060972, 2761369, 3067696, 3196359, 683506, 2950158, 6455259, 7287650, 2911298, 2925533, 2825297, 715429, 721472, 3050616, 3050434, 3045190, 3044774, 721239, 2643743, 6359304, 2995469)
for city in cities:
    resp = weatherdata.query_weather_data(city)
    weatherdata.load_data(resp)
