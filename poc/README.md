# CDEvents Visualisation Reference Implementation

The CDEvents Proof of Concept is demonstrated by CDEvents contributors to show the interactions between different CI/CD tools Tekton, Keptn and Spinnaker. In the PoC Tekton executes the Pipeline to build the artifact, Keptn handles the business decision and Spinnaker running the Pipeline to deploy the artifact. More information about the PoC can be found on the [PoC GitHub page](https://github.com/cdfoundation/sig-events/tree/main/poc).

CDEvents Visualisation reference implementation helps to visualise the end-end workflow of the CDEvents Proof of Concept with different types of visualisations.

### CDEvents aware tool
CDEvents aware tool knows what exactly is CDEvent and it creates sequences and aggregation graph of the events produced by PoC.


## Generic tool (Prometheus/Grafana)
Generic tool like Prometheus/Grafana can consume a specific event format which is translated from CDEvents to show the tracking and monitoring of an end-end workflow of CDEvents PoC.

## Visualisation Reference Architecture


![Reference Architecture](visualisation_reference_architecture.jpg "Reference Architecture")
