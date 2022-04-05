
from isort import file
from io import BytesIO
import numpy
import requests
from flask import Flask,request, Response, jsonify, json, send_file
from PIL import Image as im
from base64 import b64encode
app = Flask(__name__)



@app.route("/Annotation_MG")
def Annotation():
     data = {'name': 'Jose', 'Idade': '15'}
     response = requests.post('http://192.168.1.99:5000/', verify=False,data=json.dumps(data), headers={'Content-Type':'application/json'})
     print(response.status_code)
     print(response.content)
     print(response.text)
     print(response.url)
     print(response.headers)
     return(response.text)
     

@app.route("/Assembly_MG", methods=['POST'])
def Assembly():
     print(request.files)
     pic = request.files['pic']
     if not pic:
          return 'no pic uploaded',400
     data = {'image':pic}
     print(data)
     response = requests.post('http://192.168.1.99:5000/', verify=False, files=data)
     print('---------------------')
     return('Sucesss')
     

     
if __name__ == '__main__':
    app.run(host='0.0.0.0',port=5002,debug=True)