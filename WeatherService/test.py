import json

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
settings = json.loads(str)    
#dict['dsn'] = settings['postgres'][0]['credentials']['dsn']
dict = {
    'dsn': settings['postgres'][0]['credentials']['dsn'],
    'database': settings['postgres'][0]['credentials']['database'],
    'host': settings['postgres'][0]['credentials']['host'],
    'password': settings['postgres'][0]['credentials']['password'],
    'port': settings['postgres'][0]['credentials']['port'],
    'uri': settings['postgres'][0]['credentials']['dsn'],
    'username': settings['postgres'][0]['credentials']['dsn']
    }
print dict