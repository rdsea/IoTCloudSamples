import os 
from flask import Flask, request
from flask_restful import Resource, Api
from flask_restful import reqparse
from werkzeug.utils import secure_filename
from darknet import get_tiny_yolo_detection
import sys

UPLOAD_FOLDER = '/inference/temp'

app = Flask(__name__)
app.config['UPLOAD_FOLDER'] = UPLOAD_FOLDER
api = Api(app)

# curl -F "image=@dog.jpg" localhost:5000/inference
class MLInferenceService(Resource):
    def post(self):
        # check if the post request has the file part
        file = request.files['image']
        if file.filename == '':
            return {"error": "empty"}, 404
        if file and file.filename:
            try:
                filename = secure_filename(file.filename)
                file_path = os.path.join(app.config['UPLOAD_FOLDER'], filename)
                file.save(os.path.join(app.config['UPLOAD_FOLDER'], filename))
                result = get_tiny_yolo_detection(file_path)
                os.remove(file_path)
                return result, 200
            except Exception as e:
                print "error occured" + e
                sys.stdout.flush()
                return {"error": str(e)}, 404

api.add_resource(MLInferenceService, '/inference')
if __name__ == '__main__':    
    app.run(debug=True)