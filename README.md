
# IoT Cloud Samples for Ensembles of IoT, Edge, Network Functions, and Cloud

## Introduction

This collection includes different types of IoT, edge services, network functions and cloud units, as well as samples of IoT Cloud Systems, data, and testing scenarios for different **research and teaching purposes**. Our goal  is to provide open source samples that one can use for different purposes in research and development of [ensembles of IoT, Network functions and clouds](https://link.springer.com/article/10.1007/s11761-018-0228-2).

Note: *Our code is currently being updated and uploaded.*

Pls. cite this paper if you use the IoTCloudSamples:

Hong-Linh Truong,[Using IoTCloudSamples as a Software Framework for Simulations of Edge Computing Scenarios](https://research.aalto.fi/files/61274956/Truong_Using.1_s2.0_S2542660521000275_main.pdf), Internet of Things: Engineering Cyber Physical Human Systems, 14, [100383]. https://doi.org/10.1016/j.iot.2021.100383.
```
@article{TRUONG2021100383,
title = {Using IoTCloudSamples as a software framework for simulations of edge computing scenarios},
journal = {Internet of Things},
volume = {14},
pages = {100383},
year = {2021},
issn = {2542-6605},
doi = {https://doi.org/10.1016/j.iot.2021.100383},
url = {https://www.sciencedirect.com/science/article/pii/S2542660521000275},
author = {Hong-Linh Truong}
}
```

## IoT Cloud Units

They include units for IoT, Edge and Cloud. The code is under IoTCloudUnits directory. A unit mostly is a microservice, a single program or a component that offers a set of functions for a tenant.

### IoT units

IoT units are components for IoT. Examples are sensors, actuators, and even IoT gateways. They can also be just user-defined scripts/programs that model some IoT behaviors.


#### Sensors

See genericsdsensor  and simplesensor. They are used for:

- emulated sensors and real sensors
- sensors using Things-specific APIs to monitor Things
- sensors using Software-defined Gateways API to monitor Things
- sensors using different cloud connectivity types to send data to Cloud/Gateways
- sensors running in different environments (bare OS, docker, vagrant, etc.)
- sensors running in a single node (emulated or real)
- sensors running within a topology (creating a network of sensors)

We also have complex IoT providers, such as camera provider in IoTCameraDataProvider:

- provide a service through which one can obtain real public camera video.

#### IoT data transformation and ingestion units

They are for processing, transforming and ingesting data,
for example from CVS to JSON (see csvToJson), ingestionClient, mqttbridge, etc.

#### IoT control

they are for testing controlling features in IoT. For example, the testRig is used to emulate a real testRig which can be used to obtain and control sensors.

### Cloud units

Most Cloud units are based on real cloud services, such as from Google, Amazon, Azure. However, we build some wrappers to them for illustrating our concepts. Furthermore we also build some cloud services for specific purposes.

### Network Functions units

They are for network function features. For example, firewall control is network feature that can be deployed for a specific system.

## Machine Learning units

Mostly a ML unit is a model that can be encapsulated into a single ML sevice instance. ML units implement ML models that can be deployed as a service unit.
- [BTS Prediction](MLUnits/BTSPrediction/): a set of ML units for dynamic prediction of alarms and other problems within a telco base transceiver station.
- [Llama2](MLUnits/SimpleLlama2/): a simple deployment of a llama2 small model, using AMQP API.

## IoT, Cloud and Network Function providers

Units provide basic functions. We provide Providers which can be used to provision and manage resources, which are instances of units, for different purposes. A provider will provide IoT, network functions and cloud resources.

Examples:

- BTS Sensor Provider
- MQTT Provider
- NODE-RED Provider
- Firewall Provider

There are specific code for specific providers but there are also generic code for generic providers that can be adapted easy for other purposes.

## Data

We provide some sample of data collected from real systems. Examples are Base Transceiver Stations (BTS) data from monitoring real BTS

## IoT-Edge-Cloud scenarios

From existing units, providers and data, for specific research and development purposes, one can create various different scenarios. Each scenario describes a system to be designed and it might be used for different purposes. A scenario might be simple (e.g., just ingesting data from IoT sensors to a broker) or complex (e.g., and end-to-end IoT sensors-edge broker - cloud database). We provide some scenarios but other scenarios can also be found in other places, such as:

- for interoperability and slice management (https://github.com/SINCConcept/HINC)
- for testing uncertainty (https://github.com/rdsea/T4UME)
- for testing incidents (https://github.com/rdsea/bigdataincidentanalytics)

#### BTS Monitoring scenario
The [BTS monitoring scenario](scenarios/simpleBTSEdgeCloudIngestion) illustrates monitoring and data analytics for BTS.

#### Network Operations Monitoring scenario

The [network operations analytics scenario](scenarios/netops) is used to study elasticity and elasticity of edge-cloud systems for network monitoring.

#### IoT Machine Learning Predictive Maintenance scenario

The [machine learning predictive maintenance scenario](scenarios/IoTMLPredictiveMaintenance) is used to study dynamic ML serving and IoT data inference. 

## Supporting Edge Cloud Technologies

IoTCloudSamples utilizes different programming languages and frameworks. Generally, code can be run with
* Docker container systems
* Kubernetes (mainly tested with Google Kubernetes and minukube)

## Relevant publications

The following papers are relevant to the development of the IoTCloudSamples:

- Hong-Linh Truong,[Using IoTCloudSamples as a Software Framework for Simulations of Edge Computing Scenarios](https://research.aalto.fi/files/61274956/Truong_Using.1_s2.0_S2542660521000275_main.pdf), Internet of Things: Engineering Cyber Physical Human Systems, 14, [100383]. https://doi.org/10.1016/j.iot.2021.100383.
- Hong-Linh Truong, Lingfan Gao, Michael Hammerer, Service Architectures and Dynamic Solutions for Interoperability of IoT, Network Functions and Cloud Resources [Preprint](https://bit.ly/2LEYoIz), 12th European Conference on Software Architecture, September 24-28, 2018, Madrid, Spain
- Hong-Linh Truong, Luca Berardinelli, Ivan Pavkovic and Georgiana Copil, Modeling and Provisioning IoT Cloud Systems for Testing Uncertainties, [Pre-print PDF](https://users.aalto.fi/~truongh4/publications/2017/truong-mobiquitous2017.pdf), 14th EAI International Conference on Mobile and Ubiquitous Systems: Computing, Networking and Services (MobiQuitous 2017), November 7–10, 2017,Melbourne, Australia.
- Hong-Linh Truong, Georgiana Copil, Schahram Dustdar, Duc-Hung Le, Daniel Moldovan, Stefan Nastic, On Engineering Analytics for Elastic IoT Cloud Platforms [PDF](https://users.aalto.fi/~truongh4/publications/2016/truong-icsoc2016.pdf), (c)Springer-Verlag,14th International Conference on Service Oriented Computing (ICSOC 2016), Oct 10-13, 2016. Banff, Canada.

## Contact
Code is currently being updated and uploaded.
Contact Hong-Linh Truong (linh.truong@aalto.fi) for further information

## Acknowledgment

The work is dated back from 2015. The work was partially supported by the [H2020 U-test project](http://www.u-test.eu) and the [H2020 Inter-IoT](http://www.inter-iot-project.eu/). The work has been contributed by a lot of in-kind effort from students and also has been benefited from our collaboration with industries, who share use cases and data.
