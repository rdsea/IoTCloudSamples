'''
A very simple python program to subscribe data from a queue
'''
import pika
import os
import argparse
if __name__ == '__main__':

    parser = argparse.ArgumentParser()
    parser.add_argument('--queuename', help='queue name')
    args = parser.parse_args()
    # get amqpurl from environment variable
    url = os.environ.get('AMQPURL')
    if url is None:
        # a local test one
        url = "amqp://guest:guest@pisamba"

    params = pika.URLParameters(url)
    params.socket_timeout = 5
    connection = pika.BlockingConnection(params)  # Connect to AMQP
    channel = connection.channel()  # start a channel
    # call back do nothing, just print the result
    def callback(ch, method, properties, body):
        print(f'Received: {body}')

    channel.basic_consume(args.queuename, callback)
    try:
        channel.start_consuming()
    except Exception:
        channel.stop_consuming()
    connection.close()
