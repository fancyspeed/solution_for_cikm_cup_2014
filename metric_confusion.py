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
            solnDict[query] = labels
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
            submissionDict[query] = labels

    if len(submissionDict) != len(solutionDict):
        print 'size of submission and solution must be the same'
        return False
    return submissionDict

def confusion(solution, submission):
    """
    """

    solutionDict = create_solution_dictionary(solution)
    submissionDict = check_submission(submission, solutionDict)

    if submissionDict:
        matrix = {}
        for query in solutionDict:
            label = submissionDict[query]
            truth = solutionDict[query]
            matrix[truth] = matrix.get(truth, {})
            matrix[truth][label] = matrix[truth].get(label, 0) + 1

        confusion = []
        for truth in matrix:
            label_list = sorted(matrix[truth].items(), key=lambda d:-d[1])
            confusion.append( (truth, label_list) )
        for truth, label_list in sorted(confusion, key=lambda d:-d[1][1][1] if len(d[1])>=2 else 0):
            label_list_str = ['%s:%s' % (k, v) for k, v in label_list]
            print truth, ' ==>> ', '   '.join(label_list_str)

if __name__ == "__main__":
    solutionFile = ""
    submissionFile = ""

    import sys
    if len(sys.argv) < 3:
        print '<usage> solution submission'
        exit(-1)
    solutionFile = sys.argv[1]
    submissionFile = sys.argv[2]
    
    confusion(solutionFile, submissionFile)
    
    
