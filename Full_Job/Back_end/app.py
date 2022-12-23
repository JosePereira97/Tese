from importlib.metadata import files
from unicodedata import name
from urllib import response
from flask import g,Flask, request, send_file, jsonify
from flask_sqlalchemy import SQLAlchemy
from datetime import datetime
from flask_cors import CORS
import requests
import json
from io import BytesIO
import tempfile
import ast
from ChangeNames import ChangeFileName
from check_Login import decode_cookie

app = Flask(__name__)
app.before_request_funcs.setdefault(None, [decode_cookie])
CORS(app, supports_credentials=True, origins='*')

@app.route('/Submit_input_file', methods=['POST'])
def input():
    file = {}
    pic = request.files['el_file']
    file['el_file'] = (pic.filename, pic.stream, pic.content_type, pic.headers)
    data = request.form.to_dict()
    data['User_id']= g.cookie['email']
    resposta = requests.post('http://localhost:5000/Save_Input_Files', data=data, files=file)
    if resposta.text == 'The paste is full':
        return('No space')
    elif resposta.text == 'File already contain the name':
        return('File already Exists')
    return('File updated')

@app.route('/Get_my_inputs', methods=['POST'])
def all_inputs():
    resposta = requests.get('http://localhost:5000/all_inputs', data={'User_id':g.cookie['email']})
    if resposta.content == 'No input files':
        return []
    else:
        return resposta.content

@app.route('/Get_my_inputs/Delete_Files', methods=['POST'])
def delete_inputs():
    data = request.form
    data['User_id']= g.cookie['email']
    resposta = requests.delete('http://localhost:5000/delete_inputs', data = data)
    return resposta.content

@app.route('/Get_my_inputs/Download_Files', methods=['POST'])
def download_inputs():
    data = request.form.to_dict()
    print(data)
    data['User_id']= g.cookie['email']
    resposta = requests.post('http://localhost:5000//Download_Files', data = data)
    return resposta.content


@app.route('/Submit_for_analyses', methods=['POST'])
def start_analyses():
    config = request.form['config']
    print(config)
    Data_files = json.loads(request.form['Files'])
    workflow = request.form['Workflow']
    User = g.cookie['email']
    files_info = {}
    data = {}
    for row in Data_files:
        for file in Data_files[row]:
            name = ChangeFileName(file, row, workflow[0], config)
            get_file = requests.post('http://localhost:5000/getFileForAnalyses', data={'User_id':User, 'File_Name':file})
            f = tempfile.SpooledTemporaryFile()
            f.write(get_file.content)
            f.seek(0)
            files_info[name] = (f)
    data['User_id'] = User
    data['config'] = config
    data['Workflow'] = workflow
    get_response = requests.post('http://127.0.0.1:5003/run_MOSCA full workflow',data=data,files=files_info )
    return(get_response.content)

@app.route('/Get_my_inputs/StartAnalyses', methods=['POST'])
def get_files():
    data = request.form.to_dict()
    data['User_id']= g.cookie['email']
    resposta = requests.post('http://localhost:5000/inputsType', data=data)
    return resposta.content


@app.route('/Get_my_analyses',methods=['POST']) ##falta construir funçoes para ir buscar os resultados
def my_analyses():
    resposta = requests.post('http://localhost:5000/all_outputs', data={'User_id':g.cookie['email']})
    if resposta.content == 'No output Files':
        return []
    else:
        return resposta.content

@app.route('/Get_my_analyses/Download_Results')
def my_outputs():
    data = request.form.to_dict()
    data['User_id']= g.cookie['email']
    resposta = requests.post('http://localhost:5000/downloadResults', data=data)
    pass

@app.route('/Get_my_analyses/Get_Diferent_Outputs/results', methods=['POST'])
def my_results():
    data = request.form.to_dict()
    data['User_id']= g.cookie['email']
    resposta = requests.post('http://localhost:5000/GetVisualizatedResults', data=data)
    print(type(resposta.content))
    return resposta.content






if __name__ == '__main__':
    app.run(port=5002)

