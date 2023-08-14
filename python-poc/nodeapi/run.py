from flask import Flask, jsonify
from flask import request
import json
import logging
import os
from os import listdir
from os.path import isfile, join
from arangoclientquery import Arangoclientquery

app = Flask(__name__)


alledges = []
allnodes = []

lastsearchvalue = "*"

@app.route('/api/graph/fields')
def fetch_graph_fields():
    nodes_fields = [{"field_name": "id", "type": "string"},
                    {"field_name": "title", "type": "string",
                     },
                    {"field_name": "subTitle", "type": "string"},
                    {"field_name": "mainStat", "type": "string"},
                    {"field_name": "secondaryStat", "type": "number"},
                    {"field_name": "arc__failed",
                     "type": "number", "color": "red", "displayName": "Failed"},
                    {"field_name": "arc__passed",
                     "type": "number", "color": "green", "displayName": "Passed"},
                    {"field_name": "detail__role",
                     "type": "string", "displayName": "Role"}]
    edges_fields = [
        {"field_name": "id", "type": "string"},
        {"field_name": "source", "type": "string"},
        {"field_name": "target", "type": "string"},
        {"field_name": "mainStat", "type": "number"},
    ]
    result = {"nodes_fields": nodes_fields,
              "edges_fields": edges_fields}
    return jsonify(result)


def create_nodes(json_data):
    # Extract relevant fields from JSON data and write them to the log file
    nodes = []
    counter = 0
    edges = []
    if "paths" in json_data:
        for entry in json_data["paths"]:
            for dbedge in entry["edges"]:
                edge = {}

                counter = counter + 1            
                edge["id"] = dbedge["_id"]
                edge["source"] = dbedge["_from"]
                edge["target"] = dbedge["_to"]
                edge["mainStat"] = dbedge["linktype"]
                edges.append(edge)            

            for vertice in entry["vertices"]:
                node = {}
                print (vertice)
                node["id"] = vertice["_id"]
                node["title"] = vertice["type"]
                node["mainStat"] = vertice["source"]
                node["arc__failed"] = 0.1
                node["arc__passed"] = 0.9
                nodes.append(node)

    #print(edges)
    #print("\n\n\n\n")
    #print(nodes)
    return edges , nodes



@app.route('/api/graph/data')
def fetch_graph_data():
    searchkey=""
    searchvalue=""
    print ("request.args" + str(request.args))
    if request is None:
        print ("no request")
    else:
        query = request.args
        for key,value in query.items():
            print(key,value)
            searchkey=key # value.split('=')[0].replace("\"","")
            searchvalue=value # .split('=')[1].replace("\"","")
   
        # return

    print ("searchvalue " +  searchvalue  + " last searchvalue " + lastsearchvalue)
    dbresult = arangoclientquery.getNodes(searchvalue)
    alledges, allnodes  = create_nodes(dbresult)
    result = {"nodes": allnodes, "edges": alledges}
    return jsonify(result)


@app.route('/api/health')
def check_health():
    return "API is working well!"

lastsearchvalue = "*"
if __name__ == "__main__":
    #start_http_server(8000)
    # time.sleep(60)
    # Add prometheus wsgi middleware to route /metrics requests
    #app.wsgi_app = DispatcherMiddleware(app.wsgi_app, {
    #    '/metrics': make_wsgi_app()
    #})
    arangoclientquery = Arangoclientquery()

    app.run(host='0.0.0.0', port=5000)
