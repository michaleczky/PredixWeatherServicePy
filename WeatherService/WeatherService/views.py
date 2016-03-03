"""
Routes and views for the flask application.
"""
from datetime import datetime
from flask import render_template, json, request
from WeatherService import app, models
from lib import database, weatherdata
from settings import MIN_DATE_STR, MAX_DATE_STR, DATEFORMAT

@app.route('/')
@app.route('/home')
def home():
    """Renders the home page."""
    return render_template('index.html',
        title='Home Page',
        year=datetime.now().year,)

@app.route('/contact')
def contact():
    """Renders the contact page."""
    return render_template('contact.html',
        title='Contact',
        year=datetime.now().year,
        message='Your contact page.')

@app.route('/about')
def about():
    """Renders the about page."""
    return render_template('about.html',
        title='About',
        year=datetime.now().year,
        message='Your application description page.')

@app.route('/settings')
def settings():    
    """Renders the settings page."""
    try:        
        return render_template('settings.html',
            title = 'Configuration',
            config = app.config)
    except Exception as e:
        return render_template('error.html',
            title = 'Error',
            message = e.message)

@app.route('/collect')
def collect():
    from settings import OPENWEATHERMAP_CITIES
    """Collects data from the OpenWeatherMap service and shows the data collection result."""
    errors = []
    result = ''
    if (request.args.get('run') == '1'):
        for city in OPENWEATHERMAP_CITIES:
            resp = weatherdata.query_weather_data(city)
            weatherdata.load_data(resp)
            result = result + 'City %s weather information collected...\n' % resp['city']['name']
    return render_template('collect.html',
        result = result,
        title = 'Collect Data')

@app.route('/stats')
def stats():
    """Renders the statistics page."""
    errors = []    
    places = models.Place.get_all()
    models.Place.load_measurement_counts(places)
    return render_template('stats.html',
        title = 'Statistics',
        places = places)

@app.route('/api/cities')
def api_cities():
    """Returns the list of cities in JSON"""
    places = models.Place.get_all()
    return json.jsonify(results=[place.to_json() for place in places])

@app.route('/api/m')
def api_measurements():
    """Returns measurements from the database."""
    place_id = request.args.get('city', None)
    type_id = request.args.get('type', None)
    from_date = datetime.strptime(request.args.get('from', MIN_DATE_STR), DATEFORMAT)
    to_date = datetime.strptime(request.args.get('to', MAX_DATE_STR), DATEFORMAT)
    data = models.Measurement.get_all(place_id = place_id, from_date = from_date, to_date = to_date, type_id = type_id)
    models.Measurement.load_places(data)
    models.Measurement.load_types(data)    
    return json.jsonify(results = [m.to_json() for m in data])