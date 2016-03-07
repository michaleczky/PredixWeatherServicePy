import uuid
import json
import inspect
import websocket
import time, thread
import logging, sys
import settings

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


# setup the logging    
logging.basicConfig(format = settings.LOG_FORMAT, stream = sys.stdout, level = settings.LOG_LEVEL)


def job(ws):
    payload = TS_Payload()
    payload.add_tag('TEMPERATURE', [ [1, 12, 3], [2, 15, 3], [3, 13, 3] ], {"location" : "Budapest"})
    payload.add_tag('PRESSURE', [ [1, 980, 3], [2, 1010, 3], [3, 1030, 3] ], {"location" : "Budapest"})
    payload_json = json.dumps(payload, cls=ObjectEncoder)    
    ws.send(payload_json)

def ws_on_message(ws, message):
    logging.info(message)

def ws_on_error(ws, error):
    logging.error, error

def ws_on_close(ws):
    logging.info("WebSocket closed")

def ws_on_open(ws):
    
    def run(*args):
        for i in range(3):
            time.sleep(1)
            job(ws)
        time.sleep(1)
        ws.close()
    
    logging.info("WebSocket to %s opened", ws.url)
    thread.start_new_thread(run, ())

if __name__ == "__main__":
    #ws_header = "Authorization: Bearer <%s>\nPredix-Zone-Id: <%s>Origin: %s\n" % (settings.BEARER_TOKEN, settings.PREDIX_ZONE_ID, settings.ORIGIN)
    ws_header = [
        "Authorization: Bearer %s" % settings.BEARER_TOKEN,
        "Predix-Zone-Id: %s" % settings.PREDIX_ZONE_ID,
        #"Origin: %s" % settings.ORIGIN
    ]
    websocket.enableTrace(True)
    ws = websocket.WebSocketApp(settings.DI_ENDPOINT, on_message = ws_on_message, on_error = ws_on_error, on_close = ws_on_close, on_open = ws_on_open, header = ws_header)
    ws.run_forever()