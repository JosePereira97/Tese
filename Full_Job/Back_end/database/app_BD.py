import mimetypes
from multiprocessing import connection
from subprocess import IDLE_PRIORITY_CLASS
from tkinter.tix import Tree
from typing import Type
from flask import Flask, request, send_file, Response, make_response, jsonify, send_from_directory
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
import ast
from zipfile import ZipFile
from MY_zip_results import Get_my_Files
from werkzeug.security import generate_password_hash, check_password_hash
import jwt
import magic
import base64
from io import BytesIO
import base64
mime = magic.Magic(mime=True)

app = Flask(__name__)
app.config['SECRET_KEY'] = "\xfd{H\xe5<\x95\xf9\xe3\x96.5\xd1\x01O<!\xd5\xa2\xa0\x9fR\xa1\xa8"
app.config['SQLALCHEMY_DATABASE_URI'] = 'postgresql://postgres:password@localhost/Teses'
app.config['SEND_FILE_MAX_AGE_DEFAULT'] = -1
db = SQLAlchemy(app)
CORS(app, origins='*', supports_credentials=True)
User_id_seq = db.Sequence('The_seq')
id_Seq = db.Sequence('id_Seq')
file_path = os.path.abspath(os.path.dirname(__file__))
class Users(db.Model):
    __tablename__ = 'Users'
    __table_args__ = (db.UniqueConstraint("google_id"), db.UniqueConstraint("email"))
    id = db.Column(db.Integer,id_Seq, primary_key=True)
    google_id = db.Column(db.String, nullable=True)
    User_id = db.Column(db.String(45), nullable = False, primary_key = True, unique=True)
    _password = db.Column(db.String)
    given_name = db.Column(db.String, nullable=True)
    email = db.Column(db.String, nullable=True)
    picture = db.Column(db.String, nullable=True)
    last_login = db.Column(db.DateTime, nullable=True)
    children = db.relationship('Input_Files')
    children = db.relationship('Output_Files')

    @property
    def password(self):
        raise AttributeError("Can't read password")

    @password.setter
    def password(self, password):
        self._password = generate_password_hash(password)

    def verify_password(self, password):
        return check_password_hash(self._password, password)
    
    def __repr__(self):
        return f'User_id: {self.User_id}'


class Input_Files(db.Model):
    __tablename__ = 'Input_Files'
    id = db.Column(db.Integer, primary_key = True)
    Type = db.Column(db.String(45), nullable = False)
    parent_User_id = db.Column(db.String(45), db.ForeignKey("Users.User_id"), nullable = False)
    data = db.Column(db.DateTime, nullable = False, default =datetime.now)

    def __repr__(self):
        return {'id':f'{self.id}'}
    

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
        self.Rules_runned = Analyses_runned


def clear_output_files():
    delete_Output = Output_Files.query.filter(Output_Files.data <= (datetime.now() - timedelta(days=7))).all()
    for Output in delete_Output:
        Output_Files.query.filter_by(hashcode_output=Output.hashcode_output).delete()
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

@app.route('/Login/Watch_Cookies', methods = ['POST'])
def teste():
    if request.cookies.get('user') != None:
        return('sucess')
    return('User timedout')
    

@app.route('/Login/Save_User', methods = ['POST'])
def User():
    data = request.get_json()
    user = Users.query.filter(
        Users.email == data["email"]
    ).first()
    if user:
        return("This email address is already in use.")

    user = Users()
    user.email = data["email"].strip()
    user.User_id = data["email"].strip()
    user.password = data["password"].strip()
    user.last_login = datetime.now()
    user.given_name = data['name'].strip()

    db.session.add(user)
    db.session.commit()
    response = make_response("")
    response.set_cookie(
        "user",
        jwt.encode(
            {'id': user.id, 'email': user.email}, app.config["SECRET_KEY"], algorithm="HS256"
        ), httponly=True, expires= (datetime.now() + timedelta(hours=1)), samesite='None', secure=True
    )
    return response

@app.route('/Login/Check_Credentials', methods = ['POST'])
def check_login():
    data = request.get_json()
    user = Users.query.filter(
        Users.email == data["email"]
    ).first()
    if user:
        check = user.verify_password(data['password'])
        if not check:
            return('Wrong Password')
        user.last_login = datetime.now()
        response = make_response("")
        response.set_cookie("user", jwt.encode(
            {'id': user.id, 'email': user.email}, app.config["SECRET_KEY"], algorithm="HS256"
        ), httponly=True, expires= (datetime.now() + timedelta(hours=1)), samesite='None', secure=True, domain='127.0.0.1')
        return response
    return('No user with the correpondig User_Id')

@app.route('/Login/Logout', methods=['POST'])
def logOut():
    cookie = request.cookies.get("user")
    response = make_response("")
    response.set_cookie('user',expires=0,samesite='None', secure=True, domain='127.0.0.1' )
    return response

@app.route('/Save_Input_Files', methods = ['POST'])
def Save_Input_Files():
    print(request.data)
    print(request.form)
    file = request.files['el_file']
    Type = request.form['type']
    parent_User_id = request.form['User_id']
    if os.path.exists(f'{file_path}/{parent_User_id}') == False:
        os.makedirs(f'{file_path}/{parent_User_id}')
    if get_dir_size(f'{file_path}/{parent_User_id}') > 21474836480: #atualemte esta para 20 GB podemos alterar
        return('The paste is full')
    obj = os.scandir(f'{file_path}/{parent_User_id}')
    for i in obj:
        file_name_orig = i.name.rsplit('.', 1)
        file_name = file_name_orig[0].rsplit('_',1)
        if file_name[0] + '.' + file_name_orig[1] == file.filename:
            return('File already contain the name')
    Input_info = Input_Files()
    Input_info.Type = Type
    Input_info.parent_User_id = parent_User_id
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
    parent_User_id = request.form['User_id']
    Analyses_runed = request.form['Analyses_runed']
    print(Analyses_runed)
    Output_info = Output_Files(Analyses_name, parent_User_id, Analyses_runed)
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
    print(User)
    if os.path.exists(f'{file_path}/{User}') == False:
        return('No input files')
    Files = db.session.query(Input_Files).filter(Input_Files.parent_User_id==User)
    Response_data = []
    myfiles = []
    obj = os.scandir(f'{file_path}/{User}')
    for entry in obj:
        print(entry.name)
        myfiles.append(entry.name)
    for i in Files:
        for m in myfiles:
            file_name_orig = m.rsplit('.', 1)
            file_name = file_name_orig[0].rsplit('_',1)
            if int(i.id) == int(file_name[1]):
                Response_data.append({'file_name':file_name[0] + '.' + file_name_orig[1], 'file_type': i.Type, 'data': i.data , 'id': i.id})
                break
    
    return({'my_info':Response_data})

@app.route('/delete_inputs', methods=['DELETE'])
def delete_inputs():
    id = request.form['idDelete']
    User = request.form['User_id']
    obj = os.scandir(f'{file_path}/{User}')
    id = ast.literal_eval(id)
    for i in id:
        Input_Files.query.filter_by(id=i).delete()
        for entry in obj:
            file_name_orig = entry.name.rsplit('.', 1)
            file_name = file_name_orig[0].rsplit('_',1)
            if int(i) == int(file_name[1]):
                os.remove(f'{file_path}/{User}/{entry.name}')
        
    return('File deleted sucessful')

@app.route('/Download_Files', methods=['POST']) ##URL eventualmente vai ter de ser chamado diretamente para o /Download_Files devido ao send_file
def get_files():
    id = request.form['idDownload']
    User = request.form['User_id']
    obj = os.scandir(f'{file_path}/{User}')
    id = ast.literal_eval(id)
    if len(id) == 1:
        for entry in obj:
            file_name_orig = entry.name.rsplit('.', 1)
            id_check = file_name_orig[0].rsplit('_',1)
            if int(id_check[1]) == int(id[0]):
                return send_file(f'{file_path}/{User}/{entry.name}', download_name=id_check[0] + '.' + file_name_orig[1], as_attachment=True, mimetype= mime.from_file(f'{file_path}/{User}/{entry.name}'))
    else:
        ZipObj = ZipFile(f'{file_path}/Input_MOSCA.zip', 'w')
        for i in id:
            for entry in obj:
                file_name_orig = entry.name.rsplit('.', 1)
                id_check = file_name_orig[0].rsplit('_',1)
                if int(id_check[1]) == int(i):
                    ZipObj.write(f'{file_path}/{User}/{entry.name}', arcname= id_check[0] + '.' + file_name_orig[1])
        ZipObj.close()
        response = Response()
        @response.call_on_close
        def close_zip():
            os.remove(f'{file_path}/Input_MOSCA.zip')
        return send_file(f'{file_path}/Input_MOSCA.zip' , download_name='MOSCA.zip', mimetype= mime.from_file(f'{file_path}/Input_MOSCA.zip'),as_attachment=True)

@app.route('/inputsType', methods=['POST'])
def getfiles():
    User = request.form['User_id']
    tipe = json.loads(request.form['Types'])
    if os.path.exists(f'{file_path}/{User}') == False:
        return('No input files')
    Files = []
    for i in tipe:
        Teste = db.session.query(Input_Files).filter(Input_Files.parent_User_id==User).filter(Input_Files.Type==i)
        Files.append(Teste)
    Response_data = []
    myfiles = []
    obj = os.scandir(f'{file_path}/{User}')
    for entry in obj:
        myfiles.append(entry.name)
    for i in Files:
        for z in i:
            for m in myfiles:
                file_name_orig = m.rsplit('.', 1)
                file_name = file_name_orig[0].rsplit('_',1)
                if int(z.id) == int(file_name[1]):
                    Response_data.append({'file_name':file_name[0] + '.' + file_name_orig[1], 'file_type': z.Type})
                    break
    return({'my_info':Response_data})

@app.route('/getFileForAnalyses', methods=['POST'])
def get_Files():
    User = request.form['User_id']
    file_name = request.form['File_Name']
    obj = os.scandir(f'{file_path}/{User}')
    for entry in obj:
        file_name_orig = entry.name.rsplit('.', 1)
        file_nameWithoutMimeType = file_name_orig[0].rsplit('_',1)
        if file_name == file_nameWithoutMimeType[0] + '.' + file_name_orig[1]:
            return send_file(f'{file_path}/{User}/{entry.name}', download_name=f'{file_name}', mimetype= mime.from_file(f'{file_path}/{User}/{entry.name}'))


@app.route('/get_Analyses_realizated', methods=['POST'])
def get_Analyses_realizated():
    User = request.form['User_id']
    Analyses = db.session.query(Output_Files).filter(Output_Files.parent_User_id==User)
    All_analyses = []
    for i in Analyses:
        All_analyses.append({'analyses_name':i.Analyses_name, 'id':i.hashcode_output, 'workflow': i.Rules_runned})
    return({'my_Analyses': All_analyses})

@app.route('/downloadResults', methods=['POST']) ##enviar diretamente para o Results responsavel por fazer o zip de todos os resultados
def download_my_results():
    User = request.form['User_id']
    hashcODE = request.form['ID']
    Output_File = db.session.query(Output_Files).filter(Output_Files.parent_User_id==User).filter(Output_Files.hashcode_output==hashcODE)
    Analyses_Name = Output_File.Analyses_name
    shutil.make_archive(f'{file_path}/{Analyses_Name}RESULTS', 'zip', f'{file_path}/Output_{hashcODE}')
    response = Response()
    @response.call_on_close
    def delete_archive():
        os.remove(f'{file_path}/{Analyses_Name}RESULTS.zip')
    return send_file(f'{file_path}/{Analyses_Name}RESULTS.zip', as_attachment=True, mimetype= mime.from_file(f'{file_path}/{Analyses_Name}RESULTS.zip'))

@app.route('/GetVisualizatedResults', methods=['POST'])
def get_visual_results():
    hashcODE = request.form['ID']
    User = request.form['User_id']
    Output_File = db.session.query(Output_Files).filter(Output_Files.parent_User_id==User).filter(Output_Files.hashcode_output==hashcODE).first()
    workflow = Output_File.Rules_runned
    if 'all' in workflow:
        with open(f'{file_path}/MOSGUITO.zip', "rb") as fh:
            buf = BytesIO(fh.read())
        return buf
        return send_file(f'{file_path}/MOSGUITO.zip', as_attachment=True, mimetype= mime.from_file(f'{file_path}/MOSGUITO.zip'))
    else:
        Get_my_Files(workflow) #funçao que vamos criar para construir o zip file de resultados visiveis no MOSGUITO
        response = Response()
        @response.call_on_close
        def delete_archive():
            os.remove() ##Remove o archive criado na Get_my_Files
        with open(f'{file_path}/MOSGUITO.zip', "rb") as fh2:
            buf2 = BytesIO(fh2.read())
        return buf2
        return send_file(f'{file_path}/MOSGUITO.zip', as_attachment=True, mimetype= mime.from_file(f'{file_path}/MOSGUITO.zip')) ##send_file provavelmente direto para o MOSGUITO. ou senao so o download faz isso

@app.route('/all_outputs', methods=['POST'])
def get_outputs():
    User = request.form['User_id']
    Files = db.session.query(Output_Files).filter(Output_Files.parent_User_id==User)
    count = db.session.query(Output_Files).filter(Output_Files.parent_User_id==User).count()
    if count == 0:
        return('No output Files')
    Response_data = []
    for i in Files:
        Response_data.append({'Analyses_name': i.Analyses_name, 'data': i.data , 'id': i.hashcode_output})
    return({'my_info':Response_data})



if __name__ == '__main__':
    app.run(host='0.0.0.0')

