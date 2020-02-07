# -*- coding: utf-8 -*-
"""
This is a simple implementation of DBSCAN intended to explain the algorithm.

@author: Chris McCormick
"""

import numpy
from scipy import spatial
from bert_serving.client import BertClient
from pprint import pprint
import json
from nltk.corpus import stopwords 
from nltk.tokenize import word_tokenize

bc = BertClient()

# setup stopwords stopwords.words('english')
stop_words = set() 
# add extra question words to list as well
question_words = ['what', 'why', 'how', 'when', 'where', 'which', 'who', 'whom', 'whose', 'will', 'is']
stop_words.update(question_words)

def MyDBSCAN(D, eps, MinPts):
    """
    Cluster the dataset `D` using the DBSCAN algorithm.

    MyDBSCAN takes a dataset `D` (a list of vectors), a threshold distance
    `eps`, and a required number of points `MinPts`.

    It will return a list of cluster labels. The label -1 means noise, and then
    the clusters are numbered starting from 1.
    """

    # This list will hold the final cluster assignment for each point in D.
    # There are two reserved values:
    #    -1 - Indicates a noise point
    #     0 - Means the point hasn't been considered yet.
    # Initially all labels are 0.
    labels = [0] * len(D)

    # C is the ID of the current cluster.
    C = 0

    # This outer loop is just responsible for picking new seed points--a point
    # from which to grow a new cluster.
    # Once a valid seed point is found, a new cluster is created, and the
    # cluster growth is all handled by the 'expandCluster' routine.

    # For each point P in the Dataset D...
    # ('P' is the index of the datapoint, rather than the datapoint itself.)
    for P in range(0, len(D)):

        # Only points that have not already been claimed can be picked as new
        # seed points.
        # If the point's label is not 0, continue to the next point.
        if not (labels[P] == 0):
            continue

        # Find all of P's neighboring points.
        NeighborPts = regionQuery(D, P, eps)

        # If the number is below MinPts, this point is noise.
        # This is the only condition under which a point is labeled
        # NOISE--when it's not a valid seed point. A NOISE point may later
        # be picked up by another cluster as a boundary point (this is the only
        # condition under which a cluster label can change--from NOISE to
        # something else).
        if len(NeighborPts) < MinPts:
            labels[P] = -1
        # Otherwise, if there are at least MinPts nearby, use this point as the
        # seed for a new cluster.
        else:
            C += 1
            growCluster(D, labels, P, NeighborPts, C, eps, MinPts)

    # All data has been clustered!
    return labels


def growCluster(D, labels, P, NeighborPts, C, eps, MinPts):
    """
    Grow a new cluster with label `C` from the seed point `P`.

    This function searches through the dataset to find all points that belong
    to this new cluster. When this function returns, cluster `C` is complete.

    Parameters:
      `D`      - The dataset (a list of vectors)
      `labels` - List storing the cluster labels for all dataset points
      `P`      - Index of the seed point for this new cluster
      `NeighborPts` - All of the neighbors of `P`
      `C`      - The label for this new cluster.
      `eps`    - Threshold distance
      `MinPts` - Minimum required number of neighbors
    """

    # Assign the cluster label to the seed point.
    labels[P] = C

    # Look at each neighbor of P (neighbors are referred to as Pn).
    # NeighborPts will be used as a FIFO queue of points to search--that is, it
    # will grow as we discover new branch points for the cluster. The FIFO
    # behavior is accomplished by using a while-loop rather than a for-loop.
    # In NeighborPts, the points are represented by their index in the original
    # dataset.
    i = 0
    while i < len(NeighborPts):

        # Get the next point from the queue.
        Pn = NeighborPts[i]

        # If Pn was labelled NOISE during the seed search, then we
        # know it's not a branch point (it doesn't have enough neighbors), so
        # make it a leaf point of cluster C and move on.
        if labels[Pn] == -1:
            labels[Pn] = C

        # Otherwise, if Pn isn't already claimed, claim it as part of C.
        elif labels[Pn] == 0:
            # Add Pn to cluster C (Assign cluster label C).
            labels[Pn] = C

            # Find all the neighbors of Pn
            PnNeighborPts = regionQuery(D, Pn, eps)

            # If Pn has at least MinPts neighbors, it's a branch point!
            # Add all of its neighbors to the FIFO queue to be searched.
            if len(PnNeighborPts) >= MinPts:
                NeighborPts = NeighborPts + PnNeighborPts
            # If Pn *doesn't* have enough neighbors, then it's a leaf point.
            # Don't queue up it's neighbors as expansion points.
            # else:
            # Do nothing
            # NeighborPts = NeighborPts

        # Advance to the next point in the FIFO queue.
        i += 1

        # We've finished growing cluster C!


def regionQuery(D, P, eps):
    """
    Find all points in dataset `D` within distance `eps` of point `P`.

    This function calculates the distance between a point P and every other
    point in the dataset, and then returns only those points which are within a
    threshold distance `eps`.
    """
    neighbors = []

    # For each point in the dataset...
    for Pn in range(0, len(D)):

        # If the distance is below the threshold, add it to the neighbors list.
        if calc_dist(D[P], D[Pn]) > eps:
            neighbors.append(Pn)

    return neighbors


def calc_dist(vec1, vec2):
    sim1 = 1 - spatial.distance.cosine(vec1, vec2)
    dist = numpy.linalg.norm(vec1 - vec2)

    return sim1


def group_questions(questions):
    filtered_questions, ques_map = remove_stopwords_n_question_words(questions)
    D = bc.encode(filtered_questions)
    labels = MyDBSCAN(D, float(0.80), 2)

    # print(labels)

    groups = dict()
    ctr = max(labels)+1

    for i in range(len(labels)):
        if labels[i] == -1:
            groups[f'group{ctr}'] = [ques_map[filtered_questions[i]]]
            ctr += 1
        elif f'group{labels[i]}' in groups:
            groups[f'group{labels[i]}'].append(ques_map[filtered_questions[i]])
        else:
            groups[f'group{labels[i]}'] = [ques_map[filtered_questions[i]]]

    # pprint(groups)
    groups_json = json.dumps(groups)
    return groups_json


def remove_stopwords_n_question_words(questions):
    filtered_questions = []
    ques_map = dict()
    for question in questions:
        word_tokens = word_tokenize(question) 
        filtered_question = [w for w in word_tokens if not w in stop_words]
        filtered_questions.append(' '.join(filtered_question))
        ques_map[' '.join(filtered_question)] = question
    # print('---------')
    # print(ques_map)
    return filtered_questions, ques_map



def test():
    questions = ["what is fees for college",
                 "what documents are required for admission",
                 "what is college timings",
                 "what is college fees",
                 "How much fees is to be paid for admission",
                 "What courses are offered by college",
                 "What courses does the college provide",
                 "what are the documents required for admission through Minority Quota",
                 "what is admission procedure for computer engineering",
                 "what is admission procedure for mechanical engineering",
                 "what is admission procedure for electrical engineering",
                 "what documents are required for obc",
                 "what timing for office",
                 "How can I apply as NRI",
                 "what will be the charge for application form",
                 "what time is it open today"
                 ]
    # questions = remove_stopwords_n_question_words(questions)
    # print(group_questions(questions))


# test()
