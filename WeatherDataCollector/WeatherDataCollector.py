import uuid
import json
import inspect

# Data Ingestion endpoint in the PX Cloud
DI_ENDPOINT = "wss://gateway-predix-data-services.run.aws-usw02-pr.ice.predix.io/v1/stream/messages"

PREDIX_ZONE_ID = "565348bc-eda6-4a7b-b72d-e272351e06a1"

class ObjectEncoder(json.JSONEncoder):
    def default(self, obj):
        if hasattr(obj, "to_json"):
            return self.default(obj.to_json())
        elif hasattr(obj, "__dict__"):
            d = dict(
                (key, value)
                for key, value in inspect.getmembers(obj)
                if not key.startswith("__")
                and not inspect.isabstract(value)
                and not inspect.isbuiltin(value)
                and not inspect.isfunction(value)
                and not inspect.isgenerator(value)
                and not inspect.isgeneratorfunction(value)
                and not inspect.ismethod(value)
                and not inspect.ismethoddescriptor(value)
                and not inspect.isroutine(value)
            )
            return self.default(d)
        return obj


class TS_Payload:
    
    def __init__(self, messageId = None):
        self.messageId = messageId if messageId else TS_Payload.gen_message_id()
        self.body = []

    @staticmethod
    def gen_message_id():
        """ Generates a random message id """
        return uuid.uuid4().hex

    def add_tag(self, tagname, datapoints, attributes = None):
        """ Adds a body object to the message """
        body = TS_Body(tagname, datapoints, attributes)
        self.body.append(body)
            
class TS_Body:
    
    def __init__(self, tagname, datapoints, attributes = None):
        self.name = tagname
        self.datapoints = datapoints if datapoints else []
        self.attributes = attributes if attributes else {}


payload = TS_Payload()
payload.add_tag('TEMPERATURE', [ [1, 12, 3], [2, 15, 3], [3, 13, 3] ], {"location" : "Budapest"})
payload.add_tag('PRESSURE', [ [1, 980, 3], [2, 1010, 3], [3, 1030, 3] ], {"location" : "Budapest"})
print json.dumps(payload, cls=ObjectEncoder)