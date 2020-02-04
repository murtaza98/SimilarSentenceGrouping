from bert_serving.client import BertClient
from scipy import spatial
import numpy as np
from numpy.linalg import norm

bc = BertClient()

questions = ['fees for college', 
	'documents are required for admission',
	'college timings',
	'college fees',
	'much fees is to be paid for admission',
	'courses are offered by college',
	'courses does the college provide'
	]

# questions = ['what is fees for college', 
# 	'what documents are required for admission',
# 	'what is college timings?',
# 	'what is college fees?',
# 	'how much fees is to be paid for admission',
# 	'how much fees is to be paid for admission?',
# 	'what courses are offered by college',
# 	'what courses does the college provide'
# 	]

def calc_sim(sent1_str, sent2_str):
	global bc
	sent1 = bc.encode([sent1_str])
	sent2 = bc.encode([sent2_str])

	sim1 = 1 - spatial.distance.cosine(sent1, sent2)
	dist = np.linalg.norm(sent1-sent2)
	print("{}\n{}\n{}\n\n".format(sent1_str, sent2_str, sim1))


for i in range(len(questions)):
	for j in range(i+1, len(questions)):
		calc_sim(questions[i], questions[j])

