from flask import Flask, request, jsonify


app = Flask(__name__)

@app.route("/")
def hello_world():
     args = request.params
     print(args)
     no1 = args['key1']
     no2 = args['key2']
     return jsonify(dict(data=[no1,no2]))

if __name__ == '__main__':
    app.run(host='0.0.0.0')
