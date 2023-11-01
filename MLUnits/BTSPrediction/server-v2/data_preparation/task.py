import argparse
import json, os, uuid
from Task_Handler import Task_Handler
from qoa4ml.reports import Qoa_Client
import qoa4ml.utils as qoa_utils

def get_node_name():
    node_name = os.environ.get('NODE_NAME')
    if not node_name:
        print("NODE_NAME is not defined")
        node_name = "Empty"
    return node_name
def get_instance_id():
    pod_id = os.environ.get('POD_ID')
    if not pod_id:
        print("POD_ID is not defined")
        pod_id = "Empty"
    return pod_id

if __name__ == '__main__':
    # Parse the input args
    parser = argparse.ArgumentParser(description="Data processing")
    parser.add_argument('--conf', help='configuration file', default='./conf/task_config.json')
    parser.add_argument('--next_ip', help='next destination ip', required=False)
    parser.add_argument('--next_port', help='next destination ip', required=False)
    args = parser.parse_args()
    config_data = json.load(open(args.conf))
    if args.next_ip != None:
        config_data["sender"][0]["configuration"]["url"] = "tcp://" + args.next_ip + ":"+args.next_port

    ######################################################################################################################################################
    # ------------ QoA Report ------------ #

    client = "./conf/client.json"
    connector = "./conf/connector.json"
    metric = "./conf/metrics.json"
    client_conf = qoa_utils.load_config(client)
    client_conf["node_name"] = get_node_name()
    client_conf["instance_id"] = get_instance_id()
    connector_conf = qoa_utils.load_config(connector)
    metric_conf = qoa_utils.load_config(metric)

    qoa_client = Qoa_Client(client_conf, connector_conf)
    qoa_client.add_metric(metric_conf["App-metric"], "App-metric")
    metrics = qoa_client.get_metric(category="App-metric")
    qoa_utils.proc_monitor_flag = True
    qoa_utils.process_monitor(client=qoa_client,interval=client_conf["interval"], metrics=metric_conf["Process-metric"],category="Process-metric")
    ######################################################################################################################################################
    print(config_data)
    task = Task_Handler(config_data,qoa_client)

    print("start the loop")
    task.run()