# -*- coding: utf-8 -*-
"""
Evaluation metric for the CIKM CUP 2014 
F-score

@author: Michael Liu 
Created: Thu July 22 2014
"""

import os
import csv
import math

def create_solution_dictionary(solution):
    """
    """
    
    solnDict = {}
    with open(solution, 'rb') as f:
        for line in f:
            query, labels = line.strip().split('\t')
            label_list = labels.split(' | ')
            solnDict[query] = label_list
    return solnDict

def check_submission(submission, solutionDict):
    """
    """

    submissionDict = {}
    with open(submission, 'rb') as f:
        for line in f:
            query, labels = line.strip('\n').split('\t')
            if query in submissionDict:
                print 'duplicate id in submission'
                return False
            if query not in solutionDict:
                print 'submission id must in solution'
                return False
            label_list = labels.split(' | ')
            submissionDict[query] = label_list

    if len(submissionDict) != len(solutionDict):
        print 'size of submission and solution must be the same'
        return False
    return submissionDict

def F1_metric(solution, submission):
    """
    """

    solutionDict = create_solution_dictionary(solution)
    submissionDict = check_submission(submission, solutionDict)

    if submissionDict:
        true_positive = {}
        all_positive = {}
        groundtruth = {}

        for query in solutionDict:
            label_list = set(submissionDict[query])
            truth_list = set(solutionDict[query])
            for label in label_list: 
                if label in truth_list:
                    true_positive[label] = true_positive.get(label, 0) + 1.
                all_positive[label] = all_positive.get(label, 0) + 1
            for label in truth_list:
                groundtruth[label] = groundtruth.get(label, 0) + 1

        precision_list = []
        recall_list = [] 
        for label in groundtruth:
            precision = 0
            if label in all_positive:
                precision = true_positive.get(label, 0) / all_positive.get(label, 0)
            print label, 'precision', precision 

            recall = true_positive[label] / groundtruth[label]
            print label, 'recall', recall 

            precision_list.append(precision)
            recall_list.append(recall)

        ap = sum(precision_list) / len(recall_list)
        ar = sum(recall_list) / len(recall_list)
        F1 = 2*ap*ar / (ap + ar)
        print 'ap', ap
        print 'ar', ar
        print 'F1', F1

if __name__ == "__main__":
    solutionFile = ""
    submissionFile = ""

    import sys
    if len(sys.argv) < 3:
        print '<usage> solution submission'
        exit(-1)
    solutionFile = sys.argv[1]
    submissionFile = sys.argv[2]
    
    F1_metric(solutionFile, submissionFile)
    
    
