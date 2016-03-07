import json
import uuid
import inspect

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

class TSPayload:
    
    def __init__(self, messageId = None):
        self.messageId = messageId if messageId else TSPayload.gen_message_id()
        self.body = []

    @staticmethod
    def gen_message_id():
        """ Generates a random message id """
        return uuid.uuid4().hex

    def add_tag(self, tagname, datapoints, attributes = None):
        """ 
        Adds a body object to the message        
        """
        body = TSBody(tagname, datapoints, attributes)
        self.body.append(body)

    def get_json(self):
        """ Converts the payload to JSON object """
        return json.dumps(self, cls=ObjectEncoder)
            
class TSBody:
    
    def __init__(self, tagname, datapoints, attributes = None):
        self.name = tagname
        self.datapoints = datapoints if datapoints else []
        self.attributes = attributes if attributes else {}