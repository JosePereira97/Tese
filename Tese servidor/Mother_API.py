
import requests
from flask import Flask,request, Response, jsonify, json, send_file, render_template
from PIL import Image as im
from flask_mysqldb import MySQL
from datetime import date
app = Flask(__name__)

app.config['MYSQL_HOST'] = 'localhost' #adicionar link
app.config['MYSQL_USER'] = 'root' #user_database
app.config['MYSQL_PASSWORD'] = 'password' #password_database
app.config['MYSQL_DB'] = 'MyDB' #respective table

mysql = MySQL(app)

@app.route("/Annotation_MG")
def Annotation():
     data = {'name': 'Jose', 'Idade': '15'}
     response = requests.post('http://192.168.1.99:5000/', verify=False,data=json.dumps(data), headers={'Content-Type':'application/json'})
     return(response.text)
     

@app.route("/Assembly_MG", methods=['POST'])
def Assembly():
     print(request.files)
     pic = request.files['pic']
     if not pic:
          return 'no pic uploaded',400
     data = {'image':pic}
     response = requests.post('http://192.168.1.99:5000/', verify=False, files=data)
     return('Sucesss')
     
@app.route('/get_Results', methods = ['GET', 'POST'])
def my_results():
     cur = mysql.connection.cursor()
     if request.method == 'POST':
          file = request.files
          for i in file:
               User_id = 'Teste'
               Analyses_name = i['analyses_name']
               Type_AnalysisFile = i['Type']
               mimetype = i['blob_data'].mimetype()
               name = i['blob_data'].read()
               data = file['blob_data']
               created = date.today()
               sequence = (User_id, Analyses_name, Type_AnalysisFile, mimetype, name, data, created)
               formula = "INSERT INTO Principle_Files (User_id, Analyses_name, Type_AnalysisFile, mimetype, File_name, Data, Created) VALUES (%s,%s,%s,%s,%s,%s,%s)"
               cur.execute(formula, sequence)
          return('Saved with sucess')

          ##!TODO amanha, testar funcinamento de upload e de save das imagens e dar debug, de modo a que na sexta se va realizar a funçao GET disposta em baixo.
               


     elif request.method == 'GET':
          File_name = request.data['File_name']
          cur.execute("SELECT * FROM Principle_Files WHERE Analyses_Name = %s", (File_name,))
          list_files = cur.fetchone()
          print(list_files)


     
if __name__ == '__main__':
    app.run(host='0.0.0.0',port=5002,debug=True)