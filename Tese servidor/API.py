
import requests
from flask import Flask,request, Response

app = Flask(__name__)



@app.route("/Annotation_MG")
def Annotation():
     response = requests.get('https://kubernetes.docker.internal:6443/api/v1/namespaces/default/services/hello-python-service/proxy', verify=False)
     return(response.text)

@app.route("/Assembly_MG", methods=['POST'])
def Assembly():
     pic = request.files['pic']
     if not pic:
          return 'no pic uploaded',400
     mimetype = pic.mimetype
     data = {'image':pic.read(), 'mimetype':mimetype}
     response = requests.get('https://kubernetes.docker.internal:6443/api/v1/namespaces/default/services/hello-python-service/proxy', verify=False, params=data)
     return response.json()
     #return Response()
if __name__ == '__main__':
    app.run(host='0.0.0.0',port=5002,debug=True)