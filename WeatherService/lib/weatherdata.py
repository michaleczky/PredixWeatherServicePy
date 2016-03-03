import datetime
import time
import json
import requests
import settings
import database
from WeatherService import app

MT_TEMP = 10
MT_TEMP_MIN = 11
MT_TEMP_MAX = 12
MT_PRESS = 20
MT_PRESS_SEALEV = 21
MT_PRESS_GRNDLEV = 22
MT_HUMID = 30
MT_RAIN_3H = 40
MT_WIND_SPEED = 50
MT_WIND_DEG = 51

def query_weather_data(city_id):
    """Queries the OpenWeatherMap service to get weather data between the start and end date."""
    url = 'http://api.openweathermap.org/data/2.5/forecast/city?id=%s&APPID=%s' % (city_id, settings.OPENWEATHERMAP_API_KEY)
    r = requests.get(url)
    app.logger.info('OpenWeatherMap API invoked. URL: %s; status code: %s' % (url, r.status_code))
    if (r.status_code == requests.codes.ok):
        return r.json()

def load_data(resp):
    place_id = _store_city(resp)    
    _store_measurements(place_id, resp)

def _store_city(resp):
    """Check cities exists in the DB, and if not stores them in the places table."""
    city = resp['city']
    row = database.query_row('SELECT COUNT(*) FROM Place WHERE Id = ?', (city['id'],))    
    if (row[0] == 0):
        database.execute('INSERT INTO Place (Id, Name, CoordLon, CoordLat, Country) VALUES (?,?,?,?,?)', (city['id'], city['name'], city['coord']['lon'], city['coord']['lat'], city['country']))
        database.commit()
        app.logger.info('Place %s added', city['name'])
    return city['id']


def _store_measurements(place_id, resp):
    """Stores the measurement values in the database."""
    i = 0
    j = 0
    for item in resp['list']:
        m = {}
        dt = datetime.datetime.utcfromtimestamp(int(item['dt']))
        if 'main' in item:
            if 'temp' in item['main']: 
                m[MT_TEMP] = item['main']['temp']
            if 'temp_min' in item['main']: 
                m[MT_TEMP_MIN] = item['main']['temp_min']
            if 'temp_max' in item['main']: 
                m[MT_TEMP_MAX] = item['main']['temp_max']
            if 'pressure' in item['main']: 
                m[MT_PRESS] = item['main']['pressure']
            if 'sea_level' in item['main']: 
                m[MT_PRESS_SEALEV] = item['main']['sea_level']
            if 'grnd_level' in item['main']: 
                m[MT_PRESS_GRNDLEV] = item['main']['grnd_level']
            if 'humidity' in item['main']: 
                m[MT_HUMID] = item['main']['humidity']
        if 'wind' in item:    
            if 'speed' in item['wind']: 
                m[MT_WIND_SPEED] = item['wind']['speed']
            if 'deg' in item['wind']: 
                m[MT_WIND_DEG] = item['wind']['deg']
        if 'rain' in item:
            if '3h' in item['rain']: 
                m[MT_RAIN_3H] = item['rain']['3h']
        for key in m:
            row = database.query_row('SELECT COUNT(*) FROM Measurement WHERE Time = ? AND Place = ? AND Type = ?', (dt, place_id, key))
            if row[0] == 0:
                (rowcount, lastid) = database.execute('INSERT INTO Measurement (Time, Place, Type, Value) VALUES (?,?,?,?)', (dt, place_id, key, m[key]))
                i = i + 1
            else:
                j = j + 1
    database.commit()    
    app.logger.info('%s measurements inserted for %s' % (i, place_id))
    if j > 0:
        app.logger.info('%s measurements skipped for %s' % (j, place_id))
