import sqlite3 as db
import settings
from lib import database
from WeatherService import app
import logging

DDE_SCRIPT = """

    CREATE TABLE IF NOT EXISTS Params (
        ParamObjType        NVARCHAR(32)        NOT NULL    DEFAULT '__GLOBAL__',
        ParamObject         INT                 NOT NULL    DEFAULT -1,
        ParamName           NVARCHAR(32)        NOT NULL,
        ParamValue          NVARCHAR(1024)      NOT NULL,
        ParamDesc           NVARCHAR(1024)
    );

    INSERT INTO Params (ParamName, ParamValue, ParamDesc) VALUES ('SchemaVersion', '1', 'Database schema version');

"""

logFormatStr = '[%(asctime)s] p%(process)s {%(pathname)s:%(lineno)d} %(levelname)s - %(message)s'
logging.basicConfig(format = logFormatStr, filename = "weatherservice.log", level=logging.DEBUG)
formatter = logging.Formatter(logFormatStr,'%m-%d %H:%M:%S')
streamHandler = logging.StreamHandler()
streamHandler.setLevel(logging.DEBUG)
streamHandler.setFormatter(formatter)
app.logger.addHandler(streamHandler)

try:
    conn = db.connect(settings.DB_DATABASE)
except:
    app.logger.error('Can''t connect to the database (%s)' % settings.DB_DATABASE)
    
try:
    sql = DDE_SCRIPT.split(';')
    for stmnt in sql:
        print stmnt
        cur = conn.cursor()
        cur.execute(stmnt)
except:
    app.logger.error('Error executing DDE script.')