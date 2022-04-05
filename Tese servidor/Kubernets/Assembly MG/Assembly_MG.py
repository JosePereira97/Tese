from flask import Flask, request, jsonify, Request,json, send_file
import numpy
from PIL import Image as im


app = Flask(__name__)

@app.route("/", methods = ['POST'])
def hello_world():
     data = request.files['image']
     print('------------')
     print(data.read())
     
     

if __name__ == '__main__':
    app.run(host='0.0.0.0')
