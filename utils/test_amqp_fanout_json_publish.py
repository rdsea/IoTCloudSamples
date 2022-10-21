import pika, time
import json
import argparse
if __name__ == '__main__':
    
    parser = argparse.ArgumentParser()
    parser.add_argument('--exchange', help='exchange name')
    parser.add_argument('--exchange_type',help='exchange type')
    parser.add_argument('--input_data',help='input file name')
    parser.add_argument('--url',help='url of the amqp')
    args = parser.parse_args()
    amqpLink=args.url
    params = pika.URLParameters(amqpLink)
    params.socket_timeout = 5
    connection = pika.BlockingConnection(params) # Connect to CloudAMQP
    channel = connection.channel() # start a channel
    channel.exchange_declare(exchange=args.exchange, exchange_type=args.exchange_type,durable=False)
    #simple load of all requests
    upload_data_records = json.load(open(args.input_data))
    for req_id in range(len(upload_data_records)):
        message = json.dumps(upload_data_records[req_id])
        print(f'Send a line: {message}')
        #we use the default exchange and route the message to the queuename
        #this essentially is a single queue model (direct queue)
        channel.basic_publish(exchange=args.exchange,routing_key='',
                        body=message)
        time.sleep(30)
    connection.close()
