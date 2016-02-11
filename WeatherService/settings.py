import json, logging
from datetime import datetime
from os import environ

# default settings for development and testing
DEBUG = True
DB_HOST = 'localhost'
DB_USERNAME = 'postgres'
DB_PASSWORD = 'postgres'
DB_DATABASE = 'WeatherDB'
SERVER_HOST = environ.get('SERVER_NAME', 'localhost')
SERVER_PORT = environ.get('SERVER_PORT', '8080')

# weather service
OPENWEATHERMAP_API_KEY = '76daea430717531e830e04d35e0682e7'
OPENWEATHERMAP_CITIES = (3054643, 3060972, 2761369, 3067696, 3196359, 683506, 2950158, 6455259, 7287650, 2911298, 2925533, 2825297, 715429, 721472, 3050616, 3050434, 3045190, 3044774, 721239, 2643743, 6359304, 2995469)
    
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

# datetime settings
MIN_DATE = datetime(1901, 01, 01)
MIN_DATE_STR = '1901-01-01'
MAX_DATE = datetime(2099, 12, 31)
MAX_DATE_STR = '2099-12-31'
DATEFORMAT = '%Y-%m-%d'

# database schema 
DDE_SCRIPT = """

    CREATE TABLE IF NOT EXISTS Param (
        ParamObjType        NVARCHAR(32)        NOT NULL    DEFAULT '__GLOBAL__',
        ParamObject         INT                 NOT NULL    DEFAULT -1,
        ParamName           NVARCHAR(32)        NOT NULL,
        ParamValue          NVARCHAR(1024)      NOT NULL,
        ParamDesc           NVARCHAR(1024),
        PRIMARY KEY (ParamObjType, ParamObject, ParamName)
    );

    CREATE TABLE IF NOT EXISTS Place (
        Id                  INT                 NOT NULL,
        Name                NVARCHAR(1024)      NOT NULL,
        CoordLon            DECIMAL(10,6)       NOT NULL    DEFAULT 0,
        CoordLat            DECIMAL(10,6)       NOT NULL    DEFAULT 0,
        Country             NVARCHAR(3),
        PRIMARY KEY (Id)        
    );

    CREATE TABLE IF NOT EXISTS MeasurementType (
        Id                  INT                 NOT NULL,
        Name                NVARCHAR(32)        NOT NULL,
        Unit                NVARCHAR(16),
        PRIMARY KEY (Id)
    );

    CREATE TABLE IF NOT EXISTS Measurement (   
        Time                DATETIME            NOT NULL,
        Place               INT                 NOT NULL,
        Type                INT                 NOT NULL,
        Value               DECIMAL(10,6)       NOT NULL,
        PRIMARY KEY (Time, Place, Type),
        FOREIGN KEY (Type) REFERENCES MeasurementType(Id),
        FOREIGN KEY (Place) REFERENCES Place(Id)
    );      

    INSERT INTO Param (ParamName, ParamValue, ParamDesc) VALUES ('schema_version', '1', 'Database schema version');

    INSERT INTO MeasurementType VALUES (10, 'Temperature', 'Celsius');
    INSERT INTO MeasurementType VALUES (11, 'Temperature Min.', 'Celsius');
    INSERT INTO MeasurementType VALUES (12, 'Temperature Max.', 'Celsius');
    INSERT INTO MeasurementType VALUES (20, 'Pressure', 'hPa');
    INSERT INTO MeasurementType VALUES (21, 'Pressure (sea level)', 'hPa');
    INSERT INTO MeasurementType VALUES (22, 'Pressure (ground level)', 'hPa');
    INSERT INTO MeasurementType VALUES (30, 'Humidity', '%');
    INSERT INTO MeasurementType VALUES (40, 'Rain 3-hour cumulative', 'mm');
    INSERT INTO MeasurementType VALUES (50, 'Wind Speed', 'km/h');
    INSERT INTO MeasurementType VALUES (51, 'Wind Direction', 'degree');

"""