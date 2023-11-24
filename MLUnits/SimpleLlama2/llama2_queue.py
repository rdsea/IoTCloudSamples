
#!/usr/bin/env python3
"""
This simple service uses a basic, small Llama model and provides
a simple AMQP interface for calling the service. The scenario is that
the service has to running in a reasonable machine within a network
that cannot be access from outside. Another scenario is that we want
to test the ML using streaming protocol. So we use AMQP to enable the
communication.

Small Llama2 models can be obtained from:https://huggingface.co/TheBloke/Llama-2-7B-GGUF
"""
import json
from llama_cpp import Llama
import pika
class Llama2Queue:
    def __init__(self,service_config:dict):
        self.service_config=service_config
        self.llm = Llama(model_path=service_config["llama2"]["model_path"])
        self.query_input_queue=service_config["amqp"]["query_queue_name"]
        self.answer_queue_name=service_config["amqp"]["answer_queue_name"]
        params = pika.URLParameters(service_config["amqp"]["url"])
        params.socket_timeout = 5
        self.connection = pika.BlockingConnection(params) # Connect to AMQP, We test with CloudAMQP
        self.answer_channel = self.connection.channel() # start a channel
    def callback(self,ch, method, properties, body):
        message=json.loads(body)
        answer=self.llm(message["prompt"], max_tokens=self.service_config["llama2"]["max_tokens"],echo=True)
        output={
            "message_id":message["message_id"],
            "answer":answer
        }
        output_msg=json.dumps(output)
        self.answer(output_msg)
    def answer(self,response):
        self.answer_channel.basic_publish(exchange="amq.direct",routing_key=self.answer_queue_name,
                        body=response)
    def serving(self):
        query_channel = self.connection.channel() # start a channel
        result_queue=query_channel.queue_declare(queue=self.query_input_queue)
        query_channel.queue_bind(exchange="amq.direct",queue=self.query_input_queue)
        # create a call function for incoming message consisting of prompt and message id
        
        query_channel.basic_consume(queue=self.query_input_queue,on_message_callback=self.callback,auto_ack=True)
        query_channel.start_consuming()
        self.connection.close()
