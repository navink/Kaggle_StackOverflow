'''
Created on Oct 9, 2012

@author: navin.kolambkar
'''
from __future__ import division
import numpy as np
import load_data
from sklearn.cross_validation import StratifiedKFold
from sklearn.ensemble import RandomForestClassifier, ExtraTreesClassifier, GradientBoostingClassifier
from sklearn.linear_model import LogisticRegression
import competition_utilities as cu
import features
import pandas as pd
from pandas import DataFrame

full_train_file = "train.csv"
submission_file = "blendedPredictions.csv"
train_file = "train-sample.csv"
test_file = "public_leaderboard.csv"

#train_file = "train-sample-train.csv"
#test_file = "train-sample-test.csv"

#feature_names = [ "BodyLength"
#                , "NumTags"
#                , "OwnerUndeletedAnswerCountAtPostTime"
#                , "ReputationAtPostCreation"
#                , "TitleLength"
#                , "UserAge"
#                , "Title", "Tag1", "Tag2", "Tag3", "Tag4", "Tag5"
#                ]

feature_names = [ "BodyLength"                
                , "OwnerUndeletedAnswerCountAtPostTime"
                , "ReputationAtPostCreation"                
                , "UserAge"
                , "Title"
                , "Tag1"
                , "Tag2"
                , "Tag3"
                , "Tag4"
                , "Tag5"
                ]

if __name__ == '__main__':

    np.random.seed(0) # seed to shuffle the train set

    n_folds = 10
    verbose = True
    shuffle = False
    
#    print("Reading the data")
#    dataTrain = cu.get_dataframe(train_file)
#
#    print("Extracting features")
#    fea = features.extract_features(feature_names, dataTrain)
#    X = fea
#    y = dataTrain["OpenStatus"]
#    
#    dataTest = cu.get_dataframe(test_file)
#    test_features = features.extract_features(feature_names, dataTest)
#    X_submission = test_features
    
    X, y, X_submission = load_data.load()

    if shuffle:
        idx = np.random.permutation(y.size)
        X = X[idx]
        y = y[idx]

    skf = list(StratifiedKFold(y, n_folds))

    clfs = [RandomForestClassifier(n_estimators=50, n_jobs=1, criterion='gini', verbose=2, compute_importances=True),
            RandomForestClassifier(n_estimators=100, n_jobs=-1, criterion='entropy'),
            ExtraTreesClassifier(n_estimators=100, n_jobs=-1, criterion='gini'),
            ExtraTreesClassifier(n_estimators=100, n_jobs=-1, criterion='entropy'),
            GradientBoostingClassifier(learn_rate=0.05, subsample=0.5, max_depth=6, n_estimators=50)]

    print "Creating train and test sets for blending."
    
    dataset_blend_train = np.zeros((X.shape[0], len(clfs)))
    dataset_blend_test = np.zeros((X_submission.shape[0], len(clfs)))
    
    for j, clf in enumerate(clfs):
        print j, clf
        dataset_blend_test_j = np.zeros((X_submission.shape[0], len(skf)))
        for i, (train, test) in enumerate(skf):
            print "Fold", i
            X_train = X[train]
            y_train = y[train]
            X_test = X[test]
            y_test = y[test]
            clf.fit(X, y)
            y_submission = clf.predict_proba(X_test)[:,1]
            dataset_blend_train[test, j] = y_submission
            dataset_blend_test_j[:, i] = clf.predict_proba(X_submission)[:,1]
        dataset_blend_test[:,j] = dataset_blend_test_j.mean(1)

    print
    print "Blending."
    clf = LogisticRegression()
    clf.fit(dataset_blend_train, y)
    y_submission = clf.predict_proba(dataset_blend_test)[:,1]

    print "Linear stretch of predictions to [0,1]"
    y_submission = (y_submission - y_submission.min()) / (y_submission.max() - y_submission.min())
    probs = y_submission
    
    print("Calculating priors and updating posteriors")
    new_priors = cu.get_priors(full_train_file)
    old_priors = cu.get_priors(train_file)
    probs = cu.cap_and_update_priors(old_priors, probs, new_priors, 0.001)
    
    print "Saving Results."
    cu.write_submission(submission_file, probs)
        