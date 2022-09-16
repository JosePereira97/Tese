from importlib.metadata import files
from unicodedata import name
from urllib import response
from flask import Flask, request, send_file, jsonify
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
CORS(app)

@app.route('/Submit_input_file', methods=['POST'])
def input():
    file = {}
    pic = request.files['el_file']
    file['el_file'] = (pic.filename, pic.stream, pic.content_type, pic.headers)
    print(file)
    resposta = requests.post('http://localhost:5000/Save_Input_Files', data=request.form.to_dict(), files=file)
    if resposta.text == 'The paste is full':
        return('No space') ##riderect the page to my inputs to show the space limit, and to let them delete input files.
    elif resposta.text == 'File already contain the name':
        return('File already Exists')
    return('File updated')
    #Ter atençao pois as respostas podes ser diferentes fazer alteraçoes

@app.route('/Get_my_inputs', methods=['POST'])
def all_inputs():
    resposta = requests.get('http://localhost:5000/all_inputs', data=request.form)
    if resposta.content == 'No input files':
        return []
    else:
        return resposta.content

@app.route('/Get_my_inputs/Delete_Files', methods=['POST'])
def delete_inputs():
    resposta = requests.delete('http://localhost:5000/delete_inputs', data = request.form)
    return resposta.content

@app.route('/Get_my_inputs/Download_Files', methods=['POST'])
def download_inputs():
    resposta = requests.post('http://localhost:5000//Download_Files', data = request.form)
    return resposta.content


@app.route('/Submit_for_analyses', methods=['POST'])
def start_analyses():
    config = request.form['config']
    Data_files = json.loads(request.form['Files'])
    workflow = request.form['Workflow']
    User = request.form['User_id']
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
    data['User'] = User
    data['config'] = config
    data['Workflow'] = workflow
    get_response = requests.post('http://127.0.0.1:5003/run_MOSCA full workflow',data=data,files=files_info )
    return(get_response.content)

@app.route('/Get_my_inputs/StartAnalyses', methods=['POST'])
def get_files():
    resposta = requests.post('http://localhost:5000/inputsType', data=request.form)
    return resposta.content


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

