import numpy as np
class Data_Processing(object):
    def __init__(self, configuration):
        pass

    def transform_data(self, data):
        norm_1 = float(data["norm_1"])
        norm_2 = float(data["norm_2"]) 
        norm_3 = float(data["norm_3"]) 
        norm_4 = float(data["norm_4"]) 
        norm_5 = float(data["norm_5"]) 
        norm_6 = float(data["norm_6"]) 
        pas_series =np.array([[norm_1],[norm_2],[norm_3],[norm_4],[norm_5],[norm_6]])
        return pas_series

    def process(self, data):
        if isinstance(data, list):
            np_data = []
            for item in data:
                np_data.append(self.transform_data(item))
            data = np.rollaxis(np.dstack(np_data), -1)
            print(data.shape)
            return data.tolist()
        else:
            pas_series = self.transform_data(data)
            pas_series = np.array(pas_series)[np.newaxis,:,:]
            return pas_series.tolist()

    
