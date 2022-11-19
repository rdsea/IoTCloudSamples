import threading
import time
import pandas as pd
class Mess_Logging(object):
    def __init__(self, log_id, cap=500):
        column_names = ["id", "request", "response"]
        self.log = pd.DataFrame(index=range(cap),columns=column_names)
        self.capacity = cap
        self.log_request_count = 0
        self.log_response_count = 0
        self.log_id = log_id
        self.condition = threading.Condition()
        self.save_flag = True
    
    def log_request(self, data, uuid):
        with self.condition:
            self.log.loc[self.log_request_count] = [uuid, data, ""]
            self.log_request_count = (self.log_request_count+1)%self.capacity
            

    def log_response(self, data, uuid):
        with self.condition:
            self.log.loc[self.log["id"] == uuid] = data
            self.log_response_count = (self.log_response_count+1)%self.capacity
            if (self.log_response_count == (self.capacity/2)):
                self.save_to_file(0,self.capacity/2-1)
            elif (self.log_response_count == (self.capacity-1)):
                self.save_to_file(self.capacity/2,self.capacity-1)

    def save_to_file(self, bot_lim, top_lim):
        print(self.log)
        self.log.loc[bot_lim:top_lim,].to_csv("./log/log_{}_{}.csv".format(self.log_id,time.time()),index=False)

    def set_capacity(self,cap):
        self.capacity = cap