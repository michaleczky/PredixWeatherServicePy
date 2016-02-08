"""
Routes and views for the flask application.
"""
from datetime import datetime
from flask import render_template
from WeatherService import app
#import settings as appconfig

@app.route('/')
@app.route('/home')
def home():
    """Renders the home page."""
    return render_template(
        'index.html',
        title='Home Page',
        year=datetime.now().year,
    )

@app.route('/contact')
def contact():
    """Renders the contact page."""
    return render_template(
        'contact.html',
        title='Contact',
        year=datetime.now().year,
        message='Your contact page.'
    )

@app.route('/about')
def about():
    """Renders the about page."""
    return render_template(
        'about.html',
        title='About',
        year=datetime.now().year,
        message='Your application description page.'
    )

@app.route('/settings')
def settings():    
    """Renders the settings page."""
    try:        
        return render_template(
            'settings.html',
            title = 'Configuration',
            config = app.config                        
        )
    except Exception as e:
        return render_template(
            'error.html',
            title = 'Error',
            message = e.message            
        )