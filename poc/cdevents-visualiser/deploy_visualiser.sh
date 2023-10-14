#!/bin/sh

./mvnw spring-boot:build-image
docker tag visualiser:0.0.1-SNAPSHOT localhost:5000/cdevents/visualiser
docker push localhost:5000/cdevents/visualiser:latest

kubectl delete -f visualiser-deployment.yaml
kubectl apply -f visualiser-deployment.yaml

kubectl delete trigger cdevents-visualiser-receiver || true

kubectl create -f - <<EOF || true
apiVersion: eventing.knative.dev/v1
kind: Trigger
metadata:
  name: cdevents-visualiser-receiver
  annotations:
    knative-eventing-injection: enabled
spec:
  broker: events-broker
  subscriber:
    uri: http://cdevents-visualiser-service.default:8099/cdevents/visualiser
EOF
