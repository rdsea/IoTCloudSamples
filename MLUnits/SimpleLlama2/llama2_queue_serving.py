
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
import argparse
import yaml
from llama2_queue import Llama2Queue
if __name__ == '__main__':
    parser = argparse.ArgumentParser()
    parser.add_argument('--config_file',help='name of config file')
    args = parser.parse_args()
    service_config_file=args.config_file
    with open(service_config_file, "r",encoding="utf-8") as fp:
        service_config=yaml.load(fp, Loader=yaml.FullLoader)
    llama2queue=Llama2Queue(service_config) 
    llama2queue.serving()
