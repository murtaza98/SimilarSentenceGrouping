#!/bin/sh
LOGS="/tmp/chatbot_server_logs.txt"
########### SENTENCE SIMILARITY MODEL PART ###############
# start bert server
nohup /home/murtaza/PycharmProjects/SentenceSimilarity/venv/bin/bert-serving-start -cpu -model_dir /home/murtaza/PycharmProjects/SentenceSimilarity/models/uncased_L-12_H-768_A-12 -num_worker=1 >> $LOGS 2>&1 &
# start flask server
nohup /home/murtaza/PycharmProjects/SentenceSimilarity/server.py >> $LOGS 2>&1 &
#
#
########### SAHEB MODEL PART ###################
nohup /home/murtaza/PycharmProjects/SAHEB/app.py >> $LOGS 2>&1 &