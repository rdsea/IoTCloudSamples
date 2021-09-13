from flask import Flask
from flask import request
from flask import Response
import requests as rq
import json 
import os
from helpers.custom_logger import CustomLogger

app = Flask(__name__)
logger = CustomLogger().get_logger()

service_name = None
port= None
def init_env_variables():
    service_name = os.environ.get('SERVICE_NAME')
    port = os.environ.get("PREPROCESSOR_SERVICE_PORT")
    if not service_name:
        logger.error("SERVICE_NAME is not defined")
        raise Exception("SERVICE_NAME is not defined")
    if not port:
        logger.error("PREPROCESSOR_SERVICE_PORT is not defined")
        raise Exception("PREPROCESSOR_SERVICE_PORT is not defined")



@app.route("/inference", methods = ['GET', 'POST'])
def inference():
    if request.method == 'GET':
        logger.info("Received a a GET request!")
        return Response('{"error":"use POST"}', status=200, mimetype='application/json')

    elif request.method == 'POST':

        try:
            r = rq.post(url=f"http://{service_name}:{port}/process", files = {'image' : request.files['image']})
            json_data = json.loads(r.text)
            uid = json_data['uid']
            
            return Response(f'{{"success":"true", "job_uuid":"{uid}"}}', status=200, mimetype='application/json')
        except Exception:
            logger.exception("Some Error occurred") 
            return Response('{"error":"some error occurred in downstream service"}', status=200, mimetype='application/json')


    else:
        return Response('{"error":"method not allowed"}', status=405, mimetype='application/json')

init_env_variables()

if __name__ == '__main__': 
    app.run(debug=True, port=4000)