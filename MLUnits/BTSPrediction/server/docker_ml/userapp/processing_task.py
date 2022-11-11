from userapp.ML_Loader import ML_Loader
import numpy as np

class LSTM_Prediction(object):
    def __init__(self, configuration):
        # Init the queue for ML request and load the ML model
        self.model_info = configuration["model"]
        self.model = ML_Loader(self.model_info)


    def init(self, configuration):
        # Init the queue for ML request and load the ML model
        model_info = configuration["model"]
        model = ML_Loader(model_info)
        return model
        
    def ML_prediction(self,pas_series):
        # Making prediciton using loader
        result = self.model.prediction(pas_series)
        # result = result.reshape(result.shape[0],result.shape[1])
        # Load the result into json format
        data_js = {
            "LSTM": result[:,0,:].tolist()
        }
        self.print_result(data_js)
        return data_js

    def process(self, data):
        # model = init(conf)
        pas_series = np.asarray(data)

        # Call back the ML prediction server for making prediction
        response = self.ML_prediction(pas_series)
        return response

    def print_result(self, data):
        prediction = ""
        for key in data:
            prediction += "\n# {} : {} ".format(key,data[key])

        prediction_to_str = f"""{'='*40}
        # Prediction Server:{prediction}
        {'='*40}"""
        print(prediction_to_str.replace('  ', ''))
    
