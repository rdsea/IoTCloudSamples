from flask import Flask, request
from flask.helpers import send_file
import requests, json, pika, zmq
from .mess_logging import Mess_Logging
headers = {
        'Content-Type': 'application/json'
    }
class Transceiver(object):
    def __init__(self, host):
        # To do
        self.host = host
    def run(self):
        pass
    def send(self):
        pass

class Amqp_Transceiver(Transceiver):
    def __init__(self, host, config):
        self.config = config
        self.exchange_name = config["exchange_name"]
        self.exchange_type = config["exchange_type"]
        self.client_id = config["client_id"] 
        self.mess_logging = Mess_Logging(self.client_id)
        self.log_flag = eval(config["log"])
        self.connection = pika.BlockingConnection(pika.ConnectionParameters(config["url"]))
        self.channel = self.connection.channel()
        self.channel.exchange_declare(exchange=self.exchange_name, exchange_type=self.exchange_type)
        super().__init__(host)


    def on_request(self, ch, method, props, body):
        # Process the data on request: sending back to host object
        if self.log_flag:
            self.mess_logging.log_response(body,props.correlation_id)
        metadata = {}
        metadata["ch"] = ch
        metadata["method"] = method
        metadata["props"] = props
        self.host.message_processing(mess=body, metadata=metadata)

    def run(self):
        # Start rabbit MQ
        self.in_routing_key = self.config["in_routing_key"]
        self.queue = self.channel.queue_declare(queue=self.config["in_queue"], exclusive=False)
        self.queue_name = self.queue.method.queue
        # Binding the exchange to the queue with specific routing
        self.channel.queue_bind(exchange=self.exchange_name, queue=self.queue_name, routing_key=self.in_routing_key)
        self.channel.basic_qos(prefetch_count=1)
        self.channel.basic_consume(queue=self.queue_name,on_message_callback=self.on_request,auto_ack=True)
        self.channel.start_consuming()

    def stop(self):
        self.channel.close()

    def send(self, mess, metadata=None):
        # Sending data to desired destination
        # if sender is client, it will include the "reply_to" attribute to specify where to reply this message
        # if sender is server, it will reply the message to "reply_to" via default exchange 
        try:
            corr_id = metadata["corr_id"]
            routing_key = metadata["routing_key"]
            exchange_name = metadata["exchange_name"]
            self.sub_properties = pika.BasicProperties(correlation_id=corr_id)
            self.channel.basic_publish(exchange=exchange_name,routing_key=routing_key,properties=self.sub_properties,body=mess)
            if self.log_flag:
                self.mess_logging.log_request(mess,corr_id)
        except Exception as e:
            print("Amqp sending data unsuccessful {}".format(e))

class Rest_Transceiver(Transceiver):
    def __init__(self, host, config):
        self.url = config["url"]
        self.route = config["route"]
        self.method = config["method"]
        self.port = config["port"]
        super().__init__(host)
    
    def create_app(self, route, method):
        # create and configure the app
        app = Flask(__name__)
        
        @app.route('/')
        def hello():
            return "This is BTS Server"
        @app.route(route, methods=method)
        def on_request():
            req_data = request.get_json()
            try:
                self.host.message_processing(mess=req_data)
            except Exception as e:
                print("Call host processing unsuccessful {}".format(e))
            return "the data is {}".format(req_data)
        return app

    def run(self):
        self.app=self.create_app(self.route,self.method)
        self.app.run(host="0.0.0.0", port=self.port)

    def send(self,data, metadata=None):
        try:
            if (metadata!=None):
                url = metadata["url"]
            else:
                url = self.url
            return requests.request("POST", url, headers=headers, data=json.dumps(data), timeout=0.1)
        except Exception as e:
            print("Error while sending data via REST: {}".format(e))

class Zmq_Transceiver(Transceiver):
    def __init__(self, host, config):
        self.context = zmq.Context()
        self.url = config["url"]
        self.run_flag = True
        super().__init__(host)
    
    def on_request(self, receiver):
        while self.run_flag:
            mess = receiver.recv_json()
            self.host.message_processing(mess=mess)

    def run(self):
        self.receiver = self.context.socket(zmq.PULL)
        self.receiver.bind(self.url)
        self.on_request(self.receiver)

    def send(self,data, metadata=None):
        try:
            if (metadata!=None):
                url = metadata["url"]
            else:
                url = self.url
            sender = self.context.socket(zmq.PUSH)
            sender.connect(url)
            sender.send_json(data)
        except Exception as e:
            print("Error while sending data via Zmq: {}".format(e))

    def stop(self):
        self.run_flag = False