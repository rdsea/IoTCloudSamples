import yaml
import os, errno
import json

def load_config(path):
    config = None
    with open(path, 'r') as config_file:
        config = yaml.load(config_file)
    return config

def createIngestionClientConfigs(ingestionConfigs):
    config = {}
    config['brokers'] = []
    config['data'] = ingestionConfigs['data']
    count = 0
    for broker in ingestionConfigs['brokers']:
        brokerConfig = {}
        brokerConfig['username'] = 'xxx'
        brokerConfig['password'] = 'xxx'
        brokerConfig['clientId'] = broker['brokerId']+'_'+str(count) 
        brokerConfig['host'] = broker['brokerId']
        brokerConfig['port'] = 1883
        brokerConfig['topics'] = broker['topics'][:]
        config['brokers'].append(brokerConfig)
        count += 1
    return config

def write_config_files(ingestionClients):
    try:
        os.makedirs('ingestionClients')
    except OSError as e:
        if e.errno != errno.EEXIST:
            raise

    for i in range(len(ingestionClients)):
        with open('ingestionClients/ingestionclient_'+str(i)+'.yml', 'w') as outfile:
            yaml.dump(ingestionClients[i], outfile)

def write_big_query_config(config, topics):
    for table in config['tables']:
        table['topics'] = list(topics)
    with open('ingestionClients/config.bigQuery.yml', 'w') as outfile:
        yaml.dump(config, outfile)


def write_compose(ingestionClients):
    command_base = ['npm', 'start']
    services = {}
    for i in range(len(ingestionClients)):
        service = {}
        command = command_base[:]
        name = 'ingestionclient_'+str(i)
        
        service['environment'] = ['CONFIG='+name+'.yml']
        service['command'] = command
        service['build'] = './ingestionClients'
        services[name] = service
    return services



def provision (config):
    ingestionClients = []
    topics = set()

    for ingestionConfigs in config['ingestionClients']:
        ingestionClients.append(createIngestionClientConfigs(ingestionConfigs))
        for broker in ingestionConfigs['brokers']:
            topics.update(broker['topics'][:])

    write_big_query_config(config['bigQuery'], topics)
    
    write_config_files(ingestionClients)
    return write_compose(ingestionClients)
