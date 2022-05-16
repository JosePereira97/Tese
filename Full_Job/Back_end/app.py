from flask import Flask, request
from flask_sqlalchemy import SQLAlchemy
from datetime import datetime

app = Flask(__name__)
app.config['SQLALCHEMY_DATABASE_URI'] = 'postgresql://postgres:password@localhost/Result_Files'
db = SQLAlchemy(app)

class Result_Files(db.Model):
    id = db.Column(db.Integer, primary_key = True)
    User_id = db.Column(db.String(45), nullable = False)
    Analyses_name = db.Column(db.String(45), nullable = False)
    Type_Analyses_File = db.Column(db.String(45), nullable = False)
    Data = db.Column(db.LargeBinary, nullable = False)
    File_Name = db.Column(db.String(45), nullable = False)
    Created_on = db.Column(db.DateTime, nullable = False, default =datetime.now)
    mimetype = db.Column(db.String(45), nullable = False)

    def __repr__(self):
        return f'Result_Files: {self.File_Name}'

    def __init__(self, User_id, Analyses_name, Type_Analyses_File, Data, File_Name, mimetype):
        self.User_id = User_id
        self.Analyses_name = Analyses_name
        self.Type_Analyses_File = Type_Analyses_File
        self.Data = Data
        self.File_Name = File_Name
        self.mimetype = mimetype

#Function that tranform the data into a JSON file
def format_object(object):
    return {
        "id": object.id,
        "User_id": object.User_id,
        "Analyses_name": object.Analyses_name,
        "Type_Analyses_File": object.Type_Analyses_File,
        "Data":object.Data,
        "File_Name":object.File_Name,
        "Created_on":object.Created_on,
        "mimetype":object.mimetype
    }


@app.route('/')
def hello():
    return 'Hey!'

#Tabela dos Ficheiros Principais
#Fuction to store the principle files in our database
@app.route('/Save_Primary_Files', methods = ['POST'])
def Save_Primary_Files():
    User_id = 'Name_do_user'
    Analyses_name = request.json['Analyses_name']
    print(Analyses_name)
    Type_Analyses_File = request.json['Type_Analyses_File']
    print(Type_Analyses_File)
    Data = b'122345676765656565'
    File_Name = 'Cenas'
    mimetype = 'Nao_sei'
    #Data = request.file['file'].read() #comentado pois POSTMAN nao consegue enviar ficheiros e files doutra maneira
    #print(Data)
    #File_Name = request.file['file'].filename
    #mimetype = request.file['file'].mimetype
    Primary_Files = Result_Files(User_id, Analyses_name, Type_Analyses_File, Data, File_Name, mimetype)
    db.session.add(Primary_Files)
    db.session.commit()
    return "Primary_File saved"

#Fuction to retrieve all Analyses_name (estas nomes serao usados para o utilizador ver todos as suas analises realizadas)
@app.route('/get_all_user_files', methods = ['GET'])
def retrive_Analyses_name():
    get_names = Result_Files.query.order_by(Result_Files.Created_on.asc()).all()
    names = []
    for event in get_names:
        names.append(format_object(event)['Analyses_name'])
    return {'names': names}

#get the respective results from the respective file name and user
@app.route('/getfile/<name>')
def get_resuls(name):
    get_results = Result_Files.query.filter_by(Analyses_name = name).filter_by(User_id = 'Name_do_user').all()
    respective_results = []
    for result in get_results:
        respective_results.append(format_object(result)['File_Name'])
    return {"results": respective_results}#!TODO feedback para saber o que fazer com o retrive dos resultados. Depois layout no front_end. Eventualmente fazer diferentes tipos de gets
#Pode haver mais gets da tabela principal. se necessario adicionar codigo para que sempre que a funçao de add files correr podemos ver se existem ficheiros com mais de 30 dias e elemina-los da satabase.





if __name__ == '__name__':
    app.run()

