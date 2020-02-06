from flask import Flask, request, jsonify
import json
from grouping import *
from flask_cors import CORS



# to start the bert server
# bert-serving-start -cpu -model_dir models/uncased_L-12_H-768_A-12/ -num_worker=1


app = Flask(__name__)
CORS(app)


@app.route('/api/rankings', methods=['POST'])
def rankings():
    data = json.dumps(request.json)
    print(data)
    questions = request.json['questions']
    groups = group_questions(questions)
    return groups


if __name__ == "__main__":
    app.run('0.0.0.0', port=2000, debug=True)