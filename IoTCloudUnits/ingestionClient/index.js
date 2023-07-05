import yaml from 'js-yaml'
import fs from 'fs'
import logger from './logger.mjs'

import mqttFactory from './mqttFactory.mjs'

// load config
let config_file =process.env.INGESTION_CLIENT_CONFIG; 
let config = null;
try{
    config = yaml.safeLoad(fs.readFileSync(config_file, 'utf8'));
    logger.info('valid configuration accepted');
}catch(err){
    logger.error(err);
    logger.error('no valid configuration received, exiting...');
    process.exit(1);
}

let clients = [];

logger.info(`loading ${config.data} data plugin`)
let data_plugin_source =`./dataPlugins/${config.data}/dataPlugin.js`
logger.info(`source: ${data_plugin_source}`)
//using dynamic loading to load the module 
let dataPluginModule =await import(data_plugin_source) 
let dataPlugin =dataPluginModule.default
dataPlugin.init().then(() => {
    config.brokers.forEach((broker) => {
        broker.remoteDataLocation = config.remoteDataLocation
        clients.push(mqttFactory.createMqttClient(broker, dataPlugin.insert));
    })
})
  

logger.info('ingest client listening for connections...')

// gracefully handle interruption and exit
function clean(){
    for(let i=0;i<clients.length;i++){
        clients[i].end();
    }
    process.exit();
}

// WARNING this might not work on windows as signals are a unix thig
process.on('SIGINT', () => {
    logger.info('terminating client...');
    clean();
})

// gracefully handle exit
process.on('uncaughtException', (err) => {
    logger.error(err.message);
    logger.error('terminating client due to exception...');
    clean();
})


