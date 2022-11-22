import Sensor from './data/models/sensor.js';

import child_process from 'child_process';
import fs from 'fs';
import { promisify } from 'util';
import deployTemplate from './configTemplates/sensorDeployTemplate.js';
import * as sensorTypes from './data/models/sensorTypes.js';
import * as configTemplates from './configTemplates/sensorConfigTemplate.js';

const exec = promisify(child_process.exec);
const writeFile = promisify(fs.writeFile);


export function getSampleConfigs(){
    let configs = [];
    Object.keys(sensorTypes).forEach((sensorType) => {
        let configTemplate = configTemplates[sensorType];
        let config  = {
            name: sensorType,
            url:`/sensor/${sensorType}`,
            sampleConfiguration: {
                uri: configTemplate.uri,
                ...configTemplate.protocolOptions,
            },
            communication:configTemplate.protocol,
            format: configTemplate.format,
            measurement: configTemplate.measurement,
            unit: configTemplate.unit,
        }
        configs.push(config);
    });
    return configs;
}

export function provision(config, type){
    return createSensor(config, type);
}

function createSensor(config, type){
    let sensorId = `sensor${(new Date()).getTime()}`;
    config.clientId = sensorId;
    return createSensorConfigMap(config, type).then((sensorConfig) => {
        return provisionSensor(sensorConfig);
    }).then((sensor) => {
        let dbSensor = new Sensor({
            type: config.type,
            clientId: sensorId,
            uri: config.uri,
            topic: config.topic,
            createdAt: Math.floor((new Date()).getTime()/1000),
            type: type,
        });
        return dbSensor.save();
    });
}

export function findSensors(type){
    let query = {
        type,
    }
    return Sensor.find(query).catch((err) => {
        console.log(err);
        return null;
    });
}

export function deleteSensor(sensorId){
    return exec(`kubectl delete configmap config-${sensorId}`).then((res) => {
        console.log(res.stdout);
        console.log(res.stderr);
        return exec(`kubectl delete deployment ${sensorId}`)
    }).then((res) => {
        console.log(res.stdout) ;
        console.log(res.stdin);
        return Sensor.remove({ clientId: sensorId });
    })
}

function createSensorConfigMap(config, type){
    //map dataset to sensor or map type to container?
    let sensorConfig = {
        ...configTemplates[type],
        uri: config.uri,
        protocolOptions:{
            topic: config.topic,
            username: config.username,
            password: config.password,
        },
        clientId: config.clientId,
        type:type
    };
    console.log(JSON.stringify(sensorConfig));

    return writeFile(`/tmp/config.json`, JSON.stringify(sensorConfig), 'utf8').then(() => {
        return exec(`kubectl create configmap config-${sensorConfig.clientId} --from-file=/tmp/config.json`);
    }).then((res) => {
        if(res.stderr) throw new Error('error occurred creating sensor config');
        console.log(res.stdout);
        return sensorConfig;
    });
}

function provisionSensor(sensor){
    let sensorDeploy = JSON.parse(JSON.stringify(deployTemplate));
    sensorDeploy.metadata.name = sensor.clientId,
    sensorDeploy.spec.template.metadata.labels.app = sensor.clientId;
    sensorDeploy.spec.template.spec.volumes.push({
        name: "config",
        configMap: { name: `config-${sensor.clientId}`}
    });

    sensorDeploy.spec.template.spec.containers[0].volumeMounts.push({
        name: "config",
        mountPath: "/simplesensor/config.json",
        subPath: "config.json"
    });

    sensorDeploy.spec.template.spec.containers[0].image = 'rdsea/'+sensor.type;
    console.log(JSON.stringify(sensorDeploy));
    return writeFile(`/tmp/deploy-${sensor.clientId}.json`, JSON.stringify(sensorDeploy), 'utf8').then(() => {
        return exec(`kubectl create -f /tmp/deploy-${sensor.clientId}.json`);
    }).then((res) => {
        if(res.stderr) {
            console.log(res.stderr);
            throw new Error('error occurred provisioning sensor');
        }
        console.log(res.stdout);
        return sensor;
    });
}

export function getLogs(sensorId){
    let logs = {}
    console.log(`kubectl logs -l app=${sensorId} --since=1h`)
    return exec(`kubectl logs -l app=${sensorId} --since=1h`).then((res) => {
        if(res.stderr) {
            console.log(res.stderr);
            logs.logs = `error fetching logs for ${sensorId}`;
        }
        logs.logs = res.stdout;
        return exec(`kubectl get pods -l app=${sensorId} -o json`)
    }).then((res) => {
        if(res.stderr) {
            console.log(res.stderr);
            logs.status = `error fetching ${sensorId} status`;
        }

        let raw = JSON.parse(res.stdout);
        try{
            logs.status = {
                deployment: "kubernetes.io",
                cpu: raw.items[0].spec.containers[0].resources.requests.cpu,
                memory: raw.items[0].spec.containers[0].resources.requests.memory,
                statuses:raw.items[0].status.containerStatuses.phase,
                startTime:  raw.items[0].status.containerStatuses.startTime
            }
        }catch(err){
            console.err(err);
            logs.status = "could not retrieve resource status"
        }

        return {
            status: logs.status,
            logs: {
                output: logs.logs,
                since: "1 hour"
            }
        };
    })
}
