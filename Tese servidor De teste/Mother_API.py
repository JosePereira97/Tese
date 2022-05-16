
import requests
from flask import Flask,request, Response, jsonify, json, send_file, render_template
from PIL import Image as im
from flask_mysqldb import MySQL
from datetime import datetime
from werkzeug.utils import secure_filename
import os

app = Flask(__name__)

app.config['MYSQL_HOST'] = 'localhost' #adicionar link
app.config['MYSQL_USER'] = 'root' #user_database
app.config['MYSQL_PASSWORD'] =  'Lolada12!' #password_database
app.config['MYSQL_DB'] = 'my_files_schema' #respective table

mysql = MySQL(app)
UPLOAD_FOLDER = 'C:\\Users\josep\OneDrive\Documentos\GitHub\Tese\Tese servidor\Files_DB'
app.config['UPLOAD_FOLDER'] = UPLOAD_FOLDER
ALLOWED_EXTENSIONS = set(['png', 'jpg', 'jpeg', 'gif'])


@app.route("/Annotation_MG")
def Annotation():
     data = {'name': 'Jose', 'Idade': '15'}
     response = requests.post('http://192.168.1.99:5000/', verify=False,data=json.dumps(data), headers={'Content-Type':'application/json'})
     return(response.text)
     

@app.route("/Assembly_MG", methods=['POST'])
def Assembly():
     pic = request.files['pic']
     print(pic)
     if not pic:
          return 'no pic uploaded',400
     files = {'image':(pic.filename, pic.stream, pic.content_type, pic.headers)}
     response = requests.post('http://192.168.1.99:5000/', files=files)
     print(response.text)
     return render_template('index.html')
     
@app.route('/get_Results', methods = ['GET', 'POST'])
def my_results():
     con = mysql.connection
     cur = con.cursor()
     print('entrou')
     if request.method == 'POST':
          file = request.files['image']
          filename = secure_filename(file.filename)
          file.save(os.path.join(app.config['UPLOAD_FOLDER'], filename))
          print(file)
          User_id = 'Teste_Teste'
          Analyses_name = request.form['analyses_name']
          Type_AnalysisFile = request.form['Type']
          mimetype = file.content_type
          name = file.filename
          data = file.read()
          created = datetime.now()
          sequence = (User_id, Analyses_name, Type_AnalysisFile, data, name, created, mimetype)
          formula = "INSERT INTO principle_Files VALUES (%s,%s,%s,%s,%s,%s,%s)"
          print('its fucked up')
          cur.execute(formula, sequence)
          con.commit()
          print('sucesso')
          return('Saved with sucess')

          ##!TODO amanha, testar funcinamento de upload e de save das imagens e dar debug, de modo a que na sexta se va realizar a funçao GET disposta em baixo.
               


     elif request.method == 'GET':
          File_name = request.data['File_name']
          cur.execute("SELECT * FROM principle_Files WHERE Analyses_Name = %s", (File_name,))
          list_files = cur.fetchone()
          print(list_files)


     
if __name__ == '__main__':
    app.run(host='0.0.0.0',port=5002,debug=True)