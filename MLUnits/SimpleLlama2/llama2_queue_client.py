"""
This simple client calls a remote small Llama service via a simple AMQP interface.
The idea is that the LLM service (e.g., based on Llama model) has to run in a reasonable 
machine within a network that cannot be access from outside using REST. Furthermore, it also 
demonstrates  a simple way to integrate LLMs via messaging so we use messaging protocols to 
enable the communication.
"""
import logging
import sys
import threading
import time
import uuid
import yaml
import pika
import json
import argparse
if __name__ == '__main__':
    parser = argparse.ArgumentParser()
    parser.add_argument('--config_file',help='name of config file') 
    args = parser.parse_args()
    service_config_file=args.config_file
    with open(service_config_file, "r",encoding="utf-8") as fp:
        service_config=yaml.load(fp, Loader=yaml.FullLoader) 
    answer_queue_name=service_config["amqp"]["answer_queue_name"]
    query_queue_name=service_config["amqp"]["query_queue_name"]
    params = pika.URLParameters(service_config["amqp"]["url"])
    params.socket_timeout = 5
    
    def start_consumer():
        connection = pika.BlockingConnection(params) # Connect to AMQP, We test with CloudAMQP
        channel = connection.channel() # start a channel
        result_queue=channel.queue_declare(queue=answer_queue_name)
        channel.queue_bind(exchange="amq.direct",queue=answer_queue_name)
        # create a call function for incoming message consisting of prompt and message id
        def callback(ch, method, properties, body):
            message=json.loads(body)
            #print(f'Message id {message["message_id"]}')
            logging.debug(f'Answer: {message["answer"]}')
            print(f'Message id {message["message_id"]}')
            if ("choices" in message["answer"]):
                for choice in message["answer"]["choices"]:
                    print(choice["text"])
        channel.basic_consume(queue=answer_queue_name,on_message_callback=callback,auto_ack=True)
        channel.start_consuming()
    consumer_thread = threading.Thread(target=start_consumer)
    consumer_thread.start()
    
    ##making the input via another thread
    connection = pika.BlockingConnection(params) # Connect to AMQP, We test with CloudAMQP
    channel = connection.channel() # start a channel
    result_queue=channel.queue_declare(queue=query_queue_name)
    channel.queue_bind(exchange="amq.direct",queue=query_queue_name)
    # read input and send to LLM
    while True:
        prompt = input("Q:")
        if (prompt=="exit"):
            consumer_thread.join()
            sys.exit(1)
        output={
            "message_id":str(uuid.uuid4()),
            "prompt":prompt
        }
        output_msg=json.dumps(output)
        channel.basic_publish(exchange="amq.direct",routing_key=query_queue_name,
                        body=output_msg)
        #delay a bit to see the answer
        time.sleep(10)
    
    