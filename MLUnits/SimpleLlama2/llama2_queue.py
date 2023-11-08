
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
import argparse
import yaml
from llama_cpp import Llama
import pika
if __name__ == '__main__':
    parser = argparse.ArgumentParser()
    parser.add_argument('--config_file',help='name of config file')
    args = parser.parse_args()
    service_config_file=args.config_file
    with open(service_config_file, "r",encoding="utf-8") as fp:
        service_config=yaml.load(fp, Loader=yaml.FullLoader)
    llm = Llama(model_path=service_config["llama2"]["model_path"])
    query_input_queue=service_config["amqp"]["query_queue_name"]
    answer_queue_name=service_config["amqp"]["answer_queue_name"]
    params = pika.URLParameters(service_config["amqp"]["url"])
    params.socket_timeout = 5
    connection = pika.BlockingConnection(params) # Connect to AMQP, We test with CloudAMQP
    channel = connection.channel() # start a channel
    result_queue=channel.queue_declare(queue=query_input_queue)
    channel.queue_bind(exchange="amq.direct",queue=query_input_queue)
    # create a call function for incoming message consisting of prompt and message id
    def callback(ch, method, properties, body):
        message=json.loads(body)
        answer=llm(message["prompt"], max_tokens=service_config["llama2"]["max_tokens"],echo=True)
        output={
            "message_id":message["message_id"],
            "answer":answer
        }
        output_msg=json.dumps(output)
        channel.basic_publish(exchange="amq.direct",routing_key=answer_queue_name,
                        body=output_msg)
    channel.basic_consume(queue=query_input_queue,on_message_callback=callback,auto_ack=True)
    channel.start_consuming()
    connection.close()
