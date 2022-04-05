
from flask import Flask, request, jsonify, json, make_response

app = Flask(__name__)

@app.route("/", methods=['POST'])
def hello_world():
     args = json.loads(request.data)
     return "Meu nome e " + args['name'] + " e tenho " + args['Idade'] + " anos."

if __name__ == '__main__':
    app.run(host='0.0.0.0')
