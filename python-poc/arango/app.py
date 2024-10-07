import os
from arangoclientgraph import Arangoclientgraph
from flask import Flask
from flask import request
from cloudevents.http import from_http
import requests
import json
import logging
import argparse
import time



app = Flask(__name__)
linkTarget = None
# @app.route('/',methods = ['POST', 'GET'])

#@app.route('/', defaults={'path': ''},methods = ['POST', 'GET'])
@app.route('/',methods = ['POST', 'GET'])
def hello_world():
#def hello_world(path):
    # create a CloudEvent
    global linkTarget
    print(request)
    print(request.headers)
    print(request.get_data())
    event = from_http(request.headers, request.get_data())
    eventdict = {}
    eventdictdata=json.loads(request.get_data())
    #eventdict=json.loads(str(event.get_attributes()))
    eventattr=event.get_attributes()
    print("eventattr")
    print(eventattr)
    eventdict = dict(eventattr)
    print("eventdict")
    print(eventdict)
    if "pipelinerun.queued" not in eventdict["type"]:
        print("Creating link for " + eventdict["type"])
        eventdict['linktarget'] = linkTarget

    linkTarget = eventdict["id"]

    print("eventdict after")
    print(eventdict)
    #arangoclientgraph.printoutput(eventdict["id"])    
    arangoclientgraph.insert_event(eventdict)
    # you can access cloudevent fields as seen below
    if "id" in eventdict:
        arangoclientgraph.printoutput(eventdict["id"])    
    
#    target = os.environ.get('TARGET', 'World')
#    print ("request data" +str(request.data))
#    print ("request data" +str(request))
#    print ("request data" +str(path))
    return "", 204

if __name__ == "__main__":
    #start_http_server(8000)
    # time.sleep(60)
    # Add prometheus wsgi middleware to route /metrics requests
    #app.wsgi_app = DispatcherMiddleware(app.wsgi_app, {
    #    '/metrics': make_wsgi_app()
    #})
    arangoclientgraph = Arangoclientgraph()

    app.run(debug=True,host='0.0.0.0',port=int(os.environ.get('PORT', 8080)))

