import os

from flask import Flask
from flask import request
from cloudevents.http import from_http
import requests
from werkzeug.middleware.dispatcher import DispatcherMiddleware
from prometheus_client import make_wsgi_app
from prometheus_client import Counter
import json
import logging
import argparse
import time
import sys

counters = {}

def create_counter(json_data):
    # Extract relevant fields from JSON data and write them to the log file
    log_entry = f"CD_EVent: {json_data}"
    logging.info(log_entry)
    counter = None
    metricname = json_data["type"].replace(".","_")
    if metricname in counters:
        counter = counters[metricname]
    else:
        if metricname == "dev.cdevents.change.merged.0.1.0".replace(".","_"):
            counter = Counter(metricname, 'Counter for' + str(json_data["context"]["type"]),["source"])
        elif metricname == "dev.cdevents.testsuite.finished.0.1.0".replace(".","_"):
            counter = Counter(metricname, 'Counter for' + str(json_data["context"]["type"]),["source","outcome"])
        else:
            counter = Counter(metricname, 'Counter for' + str(json_data["type"]))
        counters[metricname] = counter

    if metricname == "dev.cdevents.change.merged.0.1.0".replace(".","_"):
        # print("json_data[\"subject\"][\"content\"][\"repository\"][\"id\"]" + str(json_data["subject"]["content"]["repository"]["id"]))
        counter.labels(source=json_data["subject"]["repository"]["id"]).inc()
    elif metricname == "dev.cdevents.testsuite.finished.0.1.0".replace(".","_"):
        # print("json_data[\"subject\"][\"content\"][\"repository\"][\"id\"]" + str(json_data["subject"]["content"]["repository"]["id"]))
        counter.labels(source=json_data["subject"]["source"],outcome=json_data["subject"]["outcome"]).inc()

    else:
        counter.inc()



app = Flask(__name__)

# @app.route('/',methods = ['POST', 'GET'])

#@app.route('/', defaults={'path': ''},methods = ['POST', 'GET'])
@app.route('/',methods = ['POST', 'GET'])
def hello_world():
#def hello_world(path):
    # create a CloudEvent
    event = from_http(request.headers, request.get_data())

    # you can access cloudevent fields as seen below
    #print(
    #    f" EVENT {event}"
    #    f" request.get_data() {request.get_data()}"
    #)
    eventattr=event.get_attributes()
    eventdict = dict(eventattr)
    create_counter(eventdict)
    return "", 204
    
#    target = os.environ.get('TARGET', 'World')
#    print ("request data" +str(request.data))
#    print ("request data" +str(request))
#    print ("request data" +str(path))
#    return 'AFR Hello {} {} !\n'.format(target,path)

if __name__ == "__main__":
    #start_http_server(8000)
    # time.sleep(60)
    # Add prometheus wsgi middleware to route /metrics requests
    logging.basicConfig(stream=sys.stdout, level=logging.INFO)

    app.wsgi_app = DispatcherMiddleware(app.wsgi_app, {
        '/metrics': make_wsgi_app()
    })
    app.run(debug=True,host='0.0.0.0',port=int(os.environ.get('PORT', 8080)))

