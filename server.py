from flask import Flask, request, jsonify
import json
from grouping import *
from flask_cors import CORS, cross_origin

# to start the bert server
# bert-serving-start -cpu -model_dir models/uncased_L-12_H-768_A-12/ -num_worker=1


app = Flask(__name__)
CORS(app)
# app.config['SECRET_KEY'] = 'the quick brown fox jumps over the lazy   dog'
# app.config['CORS_HEADERS'] = 'Content-Type'

# cors = CORS(app, resources={r"/api/rankings": {"origins": "http://localhost:3000"}})


@app.route('/api/rankings', methods=['POST'])
# @cross_origin(origin='*',supports_credentials=True,headers=['Content- Type','Authorization'])
def rankings():
    # data = json.dumps(request.json)
    # data = request.get_json(force=True)
    # print(data)
    # questions = request.json['questions']
    # print(request.form)
    questions = request.form.getlist('questions[]')
    groups = group_questions(questions)
    response = jsonify(groups)
    response.headers.add('Access-Control-Allow-Origin',"*")
    # return groups
    return response

if __name__ == "__main__":
    app.run('127.0.0.1', port=2000, debug=True)