import time
import argparse
from LSTM_Prediction_Client import LSTM_Prediction_Client
import json,random
from threading import Thread





parser = argparse.ArgumentParser(description="Sent request to Rabbit broker")
parser.add_argument('--file', default="../data/1161114002_122_norm.csv")
parser.add_argument('--batch', default=15, type=int)
parser.add_argument('--sl', help='time sleep', default=-1.0)
parser.add_argument('--th', help='number concurrent thread', default=50)
parser.add_argument('--clientInfo',help='client information file', default="./client.json")
args = parser.parse_args()
time_sleep = int(args.sl)


def sender(num_thread):
    # prometheus_client.start_http_server(int(args.prometheus))
    # Define a client for publising data
    start_time = time.time()
    with open(args.clientInfo, "r") as f:
        client_conf = json.load(f)
    lstm_predition_client = LSTM_Prediction_Client(client_conf)
    lstm_predition_client.start()
    while (time.time() - start_time < 300):
        lstm_predition_client.publish_message(args.file, args.batch, time_sleep)
    if time_sleep == -1:
        time.sleep(random.uniform(0.0, 0.95))
    else:
        time.sleep(time_sleep)
concurrent = int(args.th)
for i in range(concurrent):
    t = Thread(target=sender,args=[i])
    t.start()