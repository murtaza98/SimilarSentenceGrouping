#!/home/murtaza/PycharmProjects/SentenceSimilarity/venv/bin/python

from flask import Flask, request, jsonify
import json
from grouping import *
from flask_cors import CORS


# to start the bert server
# bert-serving-start -cpu -model_dir models/uncased_L-12_H-768_A-12/ -num_worker=1


app = Flask(__name__)
CORS(app)


@app.route('/api/rankings', methods=['POST'])
# @cross_origin(origin='*',supports_credentials=True,headers=['Content- Type','Authorization'])
def rankings():
    # data = json.dumps(request.json)
    # data = request.get_json()
    # # print(data)
    # questions = request.json['questions']
    # groups = group_questions(questions)
    questions = request.form.getlist('questions[]')
    groups = group_questions(questions)
    response = jsonify(groups)
    response.headers.add('Access-Control-Allow-Origin',"*")
    # return groups
    return response

if __name__ == "__main__":
    app.run('127.0.0.1', port=2000, debug=True)