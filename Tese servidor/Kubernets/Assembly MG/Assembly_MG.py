from cv2 import FileStorage
from flask import Flask, request, jsonify, Request,json, send_file
import numpy
from PIL import Image as im
from sqlalchemy import JSON
from werkzeug import Response, datastructures
import requests
import cv2
import os


app = Flask(__name__)

@app.route("/", methods = ['POST'])
def hello_world():
     data = request.files['image']
     print(data)
     data = {'image':(data.filename, data.stream, data.content_type, data.headers)}
     Type = 'Assembly_MG'
     analyses_name = 'Nome' #nome dado pelos utilizadoresa analise que vao realizar
     Characteristics = {'Type': Type, 'analyses_name':analyses_name}
     #@response.call_on_close #responsavel por ser realizada depois de fechar o request da API de modo a nao deixar on hold ou fazer fila de espera, pois deve haver processos que demorem muito tempo.
     #def real_function():
     print(data)
     requests.post('http://localhost:5002/get_Results', verify=False, files=data, data=Characteristics)
     
     response = Response('The function started!')
     return response
     
     

if __name__ == '__main__':
    app.run(host='0.0.0.0')
