from scipy import *
from sklearn.ensemble import RandomForestClassifier

import getLinesFromCSV as info

from os import listdir
from os.path import isfile, join

# -----------------------------------------------------------


def get_fit(my_path='database_final\\'):
    """ Opens every file in the folder selected by my_path, gets data for classifier and fits classifier"""
    # get all the file names in that folder
    only_files = [f for f in listdir(my_path) if isfile(join(my_path, f))]

    # get line from the feature extraction algorithm used in data for each file
    features_matrix = [info.get_line(file_name) for file_name in only_files]

    # get data for classifier
    Y = [i[-2] for i in features_matrix]        # goal class
    Xtab = [i[0:-3] for i in features_matrix]   # string with features separated by \t
    X = []                                      # features
    for feature in Xtab:
        X.append(feature.split('\t'))           # features from each sample

    # best option according to Orange
    clf = RandomForestClassifier(
        max_depth=4,
        n_estimators=12,
        max_features=9)

    clf.fit(X, Y)

    return clf


def classify_ex(clf, xx):
    x = []
    x.append(xx[0:-3].split('\t'))
    return clf.predict(x)


def how_certain(clf1, x):
    print(clf1.classes_)
    print("Random Forest:")
    print(clf1.predict_proba(x))
    print(clf1.predict(x))
