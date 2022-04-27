from flask import Flask, request, jsonify, Request,json, send_file
import numpy
from PIL import Image as im
from werkzeug import Response
import requests


app = Flask(__name__)

@app.route("/", methods = ['POST'])
def hello_world():
     data = request.files['image']
     Type = 'Assembly_MG'
     analyses_name = 'Nome' #nome dado pelos utilizadoresa analise que vao realizar
     data = {'image':{'blob_data': data, 'Type': Type, 'analyses_name':analyses_name}}
     response = Response('The function started!')
     @response.call_on_close #responsavel por ser realizada depois de fechar o request da API de modo a nao deixar on hold ou fazer fila de espera, pois deve haver processos que demorem muito tempo.
     def real_function():
          requests.post('http://localhost:5002/get_Results', verify=False, files=data)
          
     return response
     
     

if __name__ == '__main__':
    app.run(host='0.0.0.0')
