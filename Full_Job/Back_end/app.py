from urllib import response
from flask import Flask, request, send_file
from flask_sqlalchemy import SQLAlchemy
from datetime import datetime
from flask_cors import CORS
import requests
import json
from io import BytesIO

app = Flask(__name__)
CORS(app)

@app.route('/Submit_input_file', methods=['POST'])
def input():
    file = {}
    pic = request.files['el_file']
    file['el_file'] = (pic.filename, pic.stream, pic.content_type, pic.headers)
    resposta = requests.post('http://localhost:5000/Save_Input_Files', data=request.form.to_dict(), files=file)
    if resposta.content == 'The paste is full':
        return('No space') ##riderect the page to my inputs to show the space limit, and to let them delete input files.
    return('done')
    #Ter atençao pois as respostas podes ser diferentes fazer alteraçoes

@app.route('/Get_my_inputs', methods=['POST'])
def all_inputs():
    resposta = requests.get('http://localhost:5000/all_inputs', data=request.form)
    print(resposta.content)
    if resposta.content == 'No input files':
        return []
    else:
        return resposta.content

@app.route('/Get_my_inputs/Delete_Files')
def delete_inputs():
    resposta = requests.delete('http://localhost:5000/delete_inputs', data = request.data)
    return resposta.content

@app.route('/Submit_for_analyses')
def start_analyses():
    config = request.data['Config_file']
    Data_files = request.data['Files']
    files_info = {}
    count = 0
    for file in Data_files:
        get_file = requests.get(f'http://localhost:5000/get/{file.id}') #Fazer na BD get file By_ID
        #if file.type is #fazer com tipos de files que podem ser scafolds etc. Para dar o nome da sample.
            #dar o nome ao ficheiro e adicionar ao files_info
        files_info[count] = get_file.content
        count += 1
    get_response = request.post() #Meter URL do servidor para começar analise.
    return(get_response.content)

@app.route('/Get_my_analyses')
def my_analyses():
    #fuction to retrive all analyses names from the user.
    pass

@app.route('/Get_my_analyses/Get_Diferent_Outputs')
def my_outputs():
    #fuction to retrieve steps made in the analyse
    pass

@app.route('/Get_my_analyses/Get_Diferent_Outputs/results')
def my_results():
    #fuction that get the files and show them in front_end
    pass






if __name__ == '__main__':
    app.run(port=5002)

