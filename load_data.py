'''
Created on Oct 9, 2012

@author: navin.kolambkar
'''
"""
Functions to load the dataset.
"""

import numpy as np
import csv

def read_data(file_name, train):
    """This function is taken from:
    https://github.com/benhamner/BioResponse/blob/master/Benchmarks/csv_io.py
    """
    f = open(file_name)
    #ignore header
    f.readline()
    samples = []
    target = []
    infile = open(file_name)
    reader = csv.reader(infile, delimiter=",")
    reader.next()
    
    if(train):
        for (PostId,PostCreationDate,OwnerUserId,OwnerCreationDate,ReputationAtPostCreation,OwnerUndeletedAnswerCountAtPostTime,Title,BodyMarkdown,Tag1,Tag2,Tag3,Tag4,Tag5,PostClosedDate,OpenStatus) in reader:
            sample = [ReputationAtPostCreation,OwnerUndeletedAnswerCountAtPostTime,Title,Tag1,Tag2,Tag3,Tag4,Tag5,OpenStatus]
            samples.append(sample)
    else:
        for row in reader:
            sample = [row[4], row[5], row[6], row[8], row[9], row[10], row[11], row[12]]
            samples.append(sample)
#    for line in f:
#        line = line.strip().split(",")
#        #sample = [float(x) for x in line]
#        sample = [x for x in line]
#        samples.append(sample)

    return samples

def load():
    """Conveninence function to load all data as numpy arrays.
    """
    print "Loading data..."
    filename_train = 'data/train-sample.csv'
    filename_test = 'data/public_leaderboard.csv'

    train = read_data(filename_train, True)
    #y_train = np.array([x[14] for x in train])
    #X_train = np.array([x[0:13] for x in train])
    
    y_train = np.array([x[8] for x in train])
    X_train = np.array([x[0:7] for x in train])
    
    test = read_data(filename_test, False)
    X_test = np.array([x[0:7] for x in test])
    
    return X_train, y_train, X_test

if __name__ == '__main__':

    X_train, y_train, X_test = load()

