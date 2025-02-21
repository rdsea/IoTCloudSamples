"""
use some basic mqtt code from mqtt examples.

This proram reads CVS file of BTS and sends to MQTT

"""
import paho.mqtt.client as paho
import time
import csv
import json
import argparse
import polars as pl

if __name__ == '__main__':
    
	parser = argparse.ArgumentParser()
	parser.add_argument('--mqttconf', help='mqtt configuration. see sample configuration')
	parser.add_argument('--sleeping_time', default=5 ,help='sleep in seconds')
	parser.add_argument('--input_file', help='BTS CVS inputfile')
	args = parser.parse_args()
	input_file = args.input_file
	#--------------- network server can be selected based on zone or pre-defined
	# it is important to have fault tolerance
	# simulating with mqtt from cloudmqtt
	#mqtt is used to connect to network server
	#amqp can also be used to connect to network server
	def on_connect(mosq, obj, rc):
		print(f'rc:{rc}')

	def on_publish(mosq, obj, mid):
		print(f'mid: {mid}')

	with open(args.mqttconf,"r") as mc_file:
		mqttconfig =json.load(mc_file)

	mqttc = paho.Client()
	# Set call back
	mqttc.on_connect = on_connect
	mqttc.on_publish = on_publish

	mqttc.username_pw_set(mqttconfig['username'], mqttconfig['password'])
	mqttc.connect(mqttconfig['host'], mqttconfig['port'])
	#start sending data
	# using pandas to read data by chunk
	df = pl.read_csv(input_file, ignore_errors = True)
	for row in df.iter_rows(named =True):
		message =json.dumps(row)
		print(message)
		mqttc.publish(mqttconfig['topic'], message)
		time.sleep(int(args.sleeping_time))
