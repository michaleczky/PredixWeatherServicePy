
import json
from os import environ

def _get_server_settings():    
    """Returns the host name from the environment variables or return localhost"""
    return {
        'server.host': environ.get('VCAP_APP_HOST', 'localhost'),
        'server.port': environ.get('VCAP_APP_PORT', '8080')
    }

def _get_db_settings():
    """Parse the database settings and return a dictionary"""
    dict = {}
    if environ.get('VCAP_SERVICES'):
        settings = json.loads(environ.get('VCAP_SERVICE'))
    else:
        str = """{
                "postgres": [
                    {
                    "credentials": {
                        "ID": 0,
                        "binding_id": "355c1ea9-63ae-4780-9770-fc5abe5317c3",
                        "database": "d53901827dfb24eeba89f3c28b7df28c4",
                        "dsn": "host=10.72.6.121 port=5432 user=u53901827dfb24eeba89f3c28b7df28c4 password=a8849e07f5e04df9bf0f25bd454c2a42 dbname=d53901827dfb24eeba89f3c28b7df28c4 connect_timeout=5 sslmode=disable",
                        "host": "10.72.6.121",
                        "instance_id": "4dacbf0d-af92-4ef1-a3fa-5895074b0a54",
                        "jdbc_uri": "jdbc:postgres://u53901827dfb24eeba89f3c28b7df28c4:a8849e07f5e04df9bf0f25bd454c2a42@10.72.6.121:5432/d53901827dfb24eeba89f3c28b7df28c4?sslmode=disable",
                        "password": "a8849e07f5e04df9bf0f25bd454c2a42",
                        "port": "5432",
                        "uri": "postgres://u53901827dfb24eeba89f3c28b7df28c4:a8849e07f5e04df9bf0f25bd454c2a42@10.72.6.121:5432/d53901827dfb24eeba89f3c28b7df28c4?sslmode=disable",
                        "username": "u53901827dfb24eeba89f3c28b7df28c4"
                    },
                    "label": "postgres",
                    "name": "WeatherDB",
                    "plan": "shared",
                    "tags": [
                        "rdpg",
                        "postgresql"
                    ]
                    }
                    ]
                }"""
        parsed = json.loads(str)    
    dict = {
        'db.dsn': parsed['postgres'][0]['credentials']['dsn'],
        'db.database': parsed['postgres'][0]['credentials']['database'],
        'db.host': parsed['postgres'][0]['credentials']['host'],
        'db.password': parsed['postgres'][0]['credentials']['password'],
        'db.port': parsed['postgres'][0]['credentials']['port'],
        'db.uri': parsed['postgres'][0]['credentials']['dsn'],
        'db.username': parsed['postgres'][0]['credentials']['dsn']
        }
    return dict

def get_as_dict():
    dict = {}
    dict.update(_get_db_settings())
    dict.update(_get_server_settings())
    return dict
