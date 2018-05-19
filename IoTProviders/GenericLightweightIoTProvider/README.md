# Generic Lightweight IoT Function Provider

In many cases, an IoT function (e.g., Gateway, Broker, firewall, etc) has to be executed in a lightweight machine. It means the machine can only run with basic operating system features, VMs, or dockers but the machine cannot have a complex distributed system, like Kubernetes.

For such a case, a function is wrapped into a unit which will be run as a process within the machine.

This provider will support this kind of units in a generic way.

## Prepare the function

The function can be written in Java, python, etc. or a Docker. But the function must be provided by scripts with actions, such as

* start_script:  for starting the function

* stop_script: for stopping the function

* restart_script: for restart the function

In our current design, we just support start_script. Other features will be added later.

Currently, each function will have a name and start_script. The information will be specified in configTemplates/deployTemplate.js

### Example with docker

 "functions": [    
     {
       "functionname":"simpledocker",
       "start_script": "docker run hello-world"
     },

### Example with Python

 Define a python script name with a functiona name:

 "functions": [
     {
       "functionname":"simplels",
       "start_script": "ls -al"
     },
     {
       "functionname":"simplepython",
       "start_script": "/usr/bin/python &"
     }

## APIs

POST /gliot with the body of {functionname:[name]} where name is the functionname in the configuration

GET /gliot/list get all running functions

DETELE /gliot/:gliotId remove the running function with the id gliotId.

###  Test examples

Call a function whose name is simplypython.

$curl --header "Content-Type: application/json"   --request POST  --data '{"functionname":"simplepython"}'    http://localhost:3002/gliot

List all running functions

$curl -X GET --url   http://localhost:3002/gliot/list

## Authors

Hong-Linh Truong
Lingfan Gao