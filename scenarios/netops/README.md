## GPON Monitoring Scenario
This scenario provisions multiple providers and their units for the GPON monitoring pipeline.

This allows the develoeprs to vary the number of sensors and pipeline artefacts.

## Requirements
The code is developed in python3 and almost all the components are dockerized. To run this simulation, we will need, 
* Docker and docker-compose
* python3 (optional for some components)
* Kubernetes (They were tested on openshift k8s platform)

## Providers
The various providers and units are:

| Providers                         | Description                                                                                           | Units                                     |
|-----------------------------------|-------------------------------------------------------------------------------------------------------|-------------------------------------------|
| IotSensorPublishProvider          | IoT sensor service reading and published to edge sub-system at a controlled rate                      | SensorPublish, SensorSplit                |
| EdgeBrokerProvider                | Provides configurable edge MQTT broker                                                                | EdgeBroker, EdgeBrokerLogger              |
| EdgeBatchingAndIngestionProvider  | Provides multiple services to ingest the data from edge broker, batch it and pushlish it to the cloud | IngestionUnit                             |
| CloudKubernetesMonitoringProvider | Scalable kubernetes based artefact monitoring of the pipeline                                         | PrometheusMonitorUnit                     |
| CloudKubernetesAnalyticsProvider  | Kubernetes based cloud analytics services                                                             | SparkAnalyticsUnit                        |
| CloudDockerizedMonitoringProvider | Dockerized versions of monitoring artefacts                                                           | PrometheusMonitorUnit, GrafanaMonitorUnit |
| CloudIngestorProvider             | Consumers data from brokerprovider and ingests into databaseprovider                                  | CassandradatabaseIngestor                 |
| CloudDatabaseProvider             | Cloud database provider for ingestion of incoming data                                                | CassandraDatabaseUnit                     |
| CloudBrokerProvider               | Provides scalable cloud broker for cloud sub-system                                                   | KafkaBrokerUnit                           |

---

## Warning
It is up to the user to make sure that the configuration file is well defined (e.g. topic names match between ingestionClients and sensors)