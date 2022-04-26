
import requests
from flask import Flask,request, Response, jsonify, json, send_file, render_template
from PIL import Image as im
from flask_mysqldb import MySQL
app = Flask(__name__)

app.config['MYSQL_HOST'] = '...' #adicionar link
app.config['MYSQL_USER'] = 'root' #user_database
app.config['MYSQL_PASSWORD'] = 'Lolada12!' #password_database
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
     if request.method == 'POST':
          pass #delete or change file name
     elif request.method == 'GET':
          pass #get the list of all the files with the respective keys passed in the arguments

     
if __name__ == '__main__':
    app.run(host='0.0.0.0',port=5002,debug=True)