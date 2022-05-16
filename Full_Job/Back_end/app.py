from flask import Flask
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

@app.route('/')
def hello():
    return 'Hey!'

#Fuction to store the principle files in our database
@app.route('/Save_Primary_Files', methods = ['POST'])
def Save_Primary_Files():
    pass

if __name__ == '__name__':
    app.run()

