from multiprocessing import connection
from subprocess import IDLE_PRIORITY_CLASS
from tkinter.tix import Tree
from typing import Type
from flask import Flask, request, send_file
from flask_sqlalchemy import SQLAlchemy
from datetime import datetime, timedelta
from flask_cors import CORS
import requests
import json
from io import BytesIO
import shutil
import copy
import os
import zipfile
import glob

app = Flask(__name__)
app.config['SQLALCHEMY_DATABASE_URI'] = 'postgresql://postgres:password@localhost/Teses'
db = SQLAlchemy(app)
CORS(app)
User_id_seq = db.Sequence('The_seq')
file_path = os.path.abspath(os.path.dirname(__file__))
class Users(db.Model):
    __tablename__ = 'Users'
    User_id = db.Column(db.String(45), nullable = False, primary_key = True, unique=True)
    Password = db.Column(db.String(45), nullable = False)
    children = db.relationship('Input_Files')
    children = db.relationship('Output_Files')

    def __repr__(self):
        return f'User_id: {self.User_id}'

    def __init__(self, User_id, Password):
        self.User_id = User_id
        self.Password = Password

class Input_Files(db.Model):
    __tablename__ = 'Input_Files'
    id = db.Column(db.Integer, primary_key = True)
    Type = db.Column(db.String(45), nullable = False)
    parent_User_id = db.Column(db.String(45), db.ForeignKey("Users.User_id"), nullable = False) #Parent que vai ser o nome onde os ficheiros vao ser guardados
    data = db.Column(db.DateTime, nullable = False, default =datetime.now)

    def __repr__(self):
        return {'id':f'{self.id}'}
    
    def __init__(self, Type, parent_User_id):
        self.Type = Type
        self.parent_User_id = parent_User_id

class Output_Files(db.Model):
    __tablename__ = 'Output_Files'
    Analyses_name = db.Column(db.String(45), nullable = False, primary_key = True)
    Rules_runned = db.Column(db.String(45), nullable = False)
    hashcode_output = db.Column(db.Integer(), User_id_seq,unique = True, nullable=False, default=User_id_seq.next_value()) #nao esquecer construit ciclo
    parent_User_id = db.Column(db.String(45), db.ForeignKey("Users.User_id"), nullable = False, primary_key = True)
    data = db.Column(db.DateTime, nullable = False, default =datetime.now)

    def __repr__(self):
        return f'{self.hashcode_output}'
    
    def __init__(self, Analyses_name, parent_User_id, Analyses_runned):
        self.Analyses_name = Analyses_name
        self.parent_User_id = parent_User_id
        self.Analyses_runned = Analyses_runned


def clear_output_files():
    delete_Output = Output_Files.query.filter_by(data <= (datetime.now - timedelta(days=7))).all()
    for Output in delete_Output:
        hashtag = Output.hashcode_output
        shutil.rmtree(f'Output_{hashtag}')
    return('Deleted with success')

def get_dir_size(path='.'):
    total = 0
    with os.scandir(path) as it:
        for entry in it:
            if entry.is_file():
                total += entry.stat().st_size
            elif entry.is_dir():
                total += get_dir_size(entry.path)
    return total

@app.route('/Save_User', methods = ['POST'])
def User():
    User_id = 'Great_user@tester.com'
    password = '1234567' #quando for implementado os users vai precisar de alteraçao
    User_add = Users(User_id, password)
    db.session.add(User_add)
    db.session.commit()
    return('Saved sucessfully')

@app.route('/Save_Input_Files', methods = ['POST'])
def Save_Input_Files():
    file = request.files['el_file']
    Type = request.form['type']
    parent_User_id = request.form['userId']
    if os.path.exists(f'{file_path}/{parent_User_id}') == False:
        os.makedirs(f'{file_path}/{parent_User_id}')
    if get_dir_size(f'{file_path}/{parent_User_id}') > 20000000000: #atualemte esta para 20 GB podemos alterar
        return('The paste is full')
    Input_info = Input_Files(Type, parent_User_id)
    db.session.add(Input_info)
    db.session.commit()
    id_info = Input_info.id
    file_name = file.filename.rsplit('.', 1)
    with open(f"{file_path}/{parent_User_id}/{file_name[0]}_{id_info}.{file_name[1]}","wb") as binary_file:
            binary_file.write(file.read())
            binary_file.close()
    return('saved with sucess')

@app.route('/Save_Output_Files', methods = ['POST'])
def Save_Output_Files():
    file = request.files['output_results']
    file_like_object = file.stream._file
    zipfile_ob = zipfile.ZipFile(file_like_object)
    Analyses_name = request.form['Analyses_name']
    parent_User_id = request.form['parent_User_id']
    Output_info = Output_Files(Analyses_name, parent_User_id)
    db.session.add(Output_info)
    db.session.commit()
    the_hashcode = (Output_info.hashcode_output)
    os.makedirs(f'{file_path}/Output_{the_hashcode}')
    zipfile_ob.extractall(f'{file_path}/Output_{the_hashcode}')
    clear_output_files()
    return('saved with sucess')

@app.route('/all_inputs')
def get_user_inputs():
    User = request.form['User_id']
    if os.path.exists(f'{file_path}/{User}') == False:
        return('No input files')
    Files = db.session.query(Input_Files).filter(Input_Files.parent_User_id==User)
    Response_data = {}
    myfiles = []
    obj = os.scandir(f'{file_path}/{User}')
    for entry in obj:
        myfiles.append(entry.name)
    for i in Files:
        for m in myfiles:
            file_name = m.rsplit('.', 1)
            file_name = file_name[0].rsplit('_',1)
            print(i.id)
            print(file_name[1])
            if int(i.id) == int(file_name[1]):
                Response_data[m] = (i.Type, i.id)
                break #ja encontramos o match do i usamos o break para n gastar mais recurso,e n existem ficheiros com o mesmo ID.
    print(Response_data)
    return(Response_data)

@app.route('/delete_inputs')
def delete_inputs():
    id = json.loads(request.data)
    for i in id:
        Input_Files.query.filter_by(id=i).delete()
    return('Files deleted sucessful')

@app.route('/get/<file_id>')
def get_files(file_id):
    file = Input_Files.query.filter_by(id=file_id)
    obj = os.scandir(f'{file_path}/{file.parent_User_id}')
    for entry in obj:
        id_check = entry.name.rsplit('_',1)
        if int(id_check) == int(file_id):
            return send_file(f'{file_path}/{file.parent_User_id}/{entry.name}', attachment_filename=entry.name)

@app.route('/results')
def get_resuls():
    #funçao que vais buscar a Analyses_names das analises realizadas pelo User.
    pass

@app.route('/get_Analyses_realizated/<hashcode>')
def get_Analyses_realizated(hashcode):
    #funçao usa hashcode para ir buscar todas as anlises realizadas.
    pass

@app.route('/get_Results/<hashcode><analyses_Name>')
def get_Files_realizated(hashcode, analyses_Name):
    #funçao usa hashcode para ir buscar os resultados da respetiva analise.
    pass


if __name__ == '__main__':
    app.run(host='0.0.0.0')

