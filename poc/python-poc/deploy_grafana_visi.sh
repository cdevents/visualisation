#!/bin/sh

# Build the Docker image
docker build python-reciever/ -t cdeventreciever-python:latest

# load the docker image into kind
kind load docker-image cdeventreciever-python:latest

# create a deployment and service and trigger
kubectl apply -f python-reciever/cdeventreciever.yaml
kubectl apply -f python-reciever/cdeventtrigger.yaml

# create a Promethues service monor to scrape the metrics
kubectl apply -f python-reciever/service-monitor.yaml

# A second service is created to also listen to all the events and this stores the events into an
# aranngodb graph DB
docker build arango/ -t arangoclient:latest

kind load docker-image arangoclient:latest
kubectl apply -f arango/storage.yaml
kubectl apply -f arango/storage-trigger.yaml

# A thrid service reads from the ArangoDB and exposes and API based on
# Node Graph API (https://grafana.com/grafana/plugins/hamedkarbasi93-nodegraphapi-datasource/) for consumption in grafana

docker build nodeapi/ -t nodeapi:latest

kind load docker-image nodeapi:latest
kubectl apply -f nodeapi/nodeapi.yaml

git clone git@github.com:prometheus-operator/kube-prometheus.git

kubectl apply --server-side -f kube-prometheus/manifests/setup
kubectl wait 	--for condition=Established 	--all CustomResourceDefinition 	--namespace=monitoring
kubectl apply -f kube-prometheus/manifests/


helm install --values loki/loki-values.yaml loki grafana/loki
helm upgrade --install  promtail grafana/promtail
