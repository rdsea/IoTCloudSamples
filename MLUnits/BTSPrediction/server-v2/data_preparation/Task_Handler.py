from utilities.transceiver import Amqp_Transceiver, Zmq_Transceiver, Rest_Transceiver
import threading, json, queue, imp



class Task_Handler(object):
    def __init__(self, configuration, qoa_client):
        # Init the main process of the task
        self.task_conf = configuration["task_configuration"]
        self.heartbeat_time = configuration["heartbeat"]
        module = imp.load_source(self.task_conf['function']['package'], self.task_conf['function']['path'])
        self.processing_obj = getattr(module, self.task_conf['function']['module_name'])(self.task_conf["config"])
        self.method_to_call = getattr(self.processing_obj, self.task_conf['function']['function_name'])
        self.qoa_client = qoa_client

        

        # Init Task Queue
        self.task_queue = queue.Queue(configuration["queue_size"])

        # Init data downstream
        self.downstream_conf = configuration["downstream"][0]
        if (self.downstream_conf["protocol"] == "AMQP"):
            # self.downstream_conf["configuration"]["in_queue"] =  self.downstream_conf["configuration"]["in_queue"] + self.get_random_string(5)
            self.downstream = Amqp_Transceiver(self, self.downstream_conf["configuration"])
        elif (self.downstream_conf["protocol"] == "REST"):
            self.downstream = Rest_Transceiver(self, self.downstream_conf["configuration"])
        elif (self.downstream_conf["protocol"] == "ZMQ"):
            self.downstream = Zmq_Transceiver(self, self.downstream_conf["configuration"])
        

        # Init data upstream (to next task)
        self.upstream_conf = configuration["upstream"][0]
        if (self.upstream_conf["protocol"] == "AMQP"):
            self.upstream = Amqp_Transceiver(self, self.upstream_conf["configuration"])
        elif (self.upstream_conf["protocol"] == "REST"):
            self.upstream = Rest_Transceiver(self, self.upstream_conf["configuration"])
        elif (self.upstream_conf["protocol"] == "ZMQ"):
            self.upstream = Zmq_Transceiver(self, self.upstream_conf["configuration"])

        # Create a thread for receiving data
        self.mess_sub_thread = threading.Thread(target=self.upstream.run)
        
        # Init task monitor
        self.report = {}
        self.count_request = 0
        self.last_count = 0
        # self.report["waiting_request"] = self.task_queue.qsize()
        self.mess_received = 0


        # Init heartbeat to update task status
        self.heartbeat = threading.Timer(self.heartbeat_time,self.send_task_report)

        # Start - Stop Flag
        self.run_flag = True
    def attache_header(self, mess, metadata):
        try:
            data = {}
            data["header"] = {}
            data["header"]["routing_key"] = metadata["props"].reply_to
            data["header"]["corr_id"] = metadata["props"].correlation_id
            data["content"] = mess
            data["raw"] = mess
            return data
        except Exception as e:
            print("Error when adding header {}".format(e))
            return None

    # The call-back function when receiving message
    def message_processing(self, mess, metadata=None):
        # Format the message to json object
        format_mess = self.format_mess(mess)
        obj_mess = json.loads(format_mess)
        self.mess_received += 1
        # Adding the header if the message hasn't got any header.
        # The header is used to store info which is where return the result to client
        # Add the headered data to the Task Queue
        # if isinstance(obj_mess, list) == False:
        #     obj_mess = [obj_mess]
        # for i in range(len(obj_mess)):
        if "content" not in obj_mess:
            obj_mess = self.attache_header(obj_mess, metadata)
        self.task_queue.put_nowait(obj_mess)
        print("Current waiting queue: ", self.task_queue.qsize())


    def send(self, data):
        # Return result to client
        if (self.downstream_conf["protocol"] == "AMQP"): 
            metadata = {}
            metadata["routing_key"] = data["header"]["routing_key"]
            metadata["corr_id"] = data["header"]["corr_id"]
            metadata["exchange_name"] = ''
            mess = data["content"]
            mess["request"] = data["raw"]
            self.downstream.send(str(json.dumps(mess)),metadata)
        # Send data to the next task
        else:
            self.downstream.send(str(json.dumps(data)))
    
    def send_task_report(self):
        n_request = self.count_request - self.last_count
        self.last_count = self.count_request
        self.report["App-metric"] = {}
        self.report["App-metric"]["waiting_request"] = self.task_queue.qsize()
        self.report["App-metric"]["processing_frequency"] = n_request/self.heartbeat_time
        self.report["App-metric"]["count_request"] = self.count_request
        self.report["App-metric"]["mess_received"] = self.mess_received
        self.qoa_client.report(report=self.report)
        print("send report: ", self.report)
        self.heartbeat = threading.Timer(self.heartbeat_time,self.send_task_report)
        self.heartbeat.start()

        
    def run(self):
        # Start a thread for receiving data
        self.mess_sub_thread.start()
        self.heartbeat.start()
        # Take the request from task Queue to process
        while self.run_flag:
            if (self.task_queue.empty() == False):
                data = self.task_queue.get_nowait()
                self.count_request += 1
                data["content"] = self.processing(data["content"])
                if data != None:
                    self.send(data)
        

    def stop(self):
        self.run_flag = False
        self.heartbeat.cancel()
    
    def processing(self, data):
        # Invoke user processing application
        return self.method_to_call(data)
        # return self.method_to_call(data, self.task_conf)
        # return self.processing_task.process(data, self.task_conf)

    def format_mess(self, mess):
        # Format the message
        if isinstance(mess, str):
            return mess
        else:
            return str(mess.decode("utf-8"))
    # def get_random_string(self, length):
    #     # choose from all lowercase letter
    #     letters = string.ascii_lowercase
    #     return ''.join(random.choice(letters) for i in range(length))