# SimilarSentenceGrouping

### Installation

create virtual env then install the modules in requirements.txt file
`pip install requirements.txt`

Download Bert-Base Uncased model, a pretrained Bert model from [here](https://github.com/hanxiao/bert-as-service#1-download-a-pre-trained-bert-model)

### Usage

1. First start the bert server <br>
  `bert-serving-start -cpu -model_dir models/uncased_L-12_H-768_A-12/ -num_worker=1`

2. Then start the flask server.
    `python server.py`

3. Lastly, send a POST request to endpoint `http://127.0.0.1:2000/api/rankings`
  POST request format <br>
  `{
  "questions": [
    "fees for college",
    "documents are required for admission"
  ]
}`
