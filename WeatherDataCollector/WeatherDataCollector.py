import uuid
import json
import inspect
import websocket
import time, thread
import logging, sys
import settings
from PredixLib import timeseries


# setup the logging    
logging.basicConfig(format = settings.LOG_FORMAT, stream = sys.stdout, level = settings.LOG_LEVEL)

def job(ws):    
    payload = timeseries.TSPayload()
    ts = int(time.time())
    payload.add_tag('TEMPERATURE', [ [ts, 12, 3], [ts, 15, 3], [ts, 13, 3] ], {"location" : "Budapest"})
    ts = int(time.time())
    payload.add_tag('PRESSURE', [ [ts, 980, 3], [ts, 1010, 3], [ts, 1030, 3] ], {"location" : "Budapest"})
    payload_json = payload.get_json()
    ws.send(payload_json)
    print ws

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
        "Predix-Zone-Id: %s" % settings.PREDIX_ZONE_ID
    ]
    websocket.enableTrace(True)
    ws = websocket.WebSocketApp(settings.DI_ENDPOINT, on_message = ws_on_message, on_error = ws_on_error, on_close = ws_on_close, on_open = ws_on_open, header = ws_header)
    ws.run_forever()