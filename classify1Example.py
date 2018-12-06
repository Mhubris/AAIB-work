from scipy import *
from sklearn.tree import DecisionTreeClassifier

import getLinesFromCSV as info

from os import listdir
from os.path import isfile, join

# -----------------------------------------------------------


def get_fit():

    # folder with csv files
    mypath = 'database_final\\'

    # get all the file names in that folder
    onlyfiles = [f for f in listdir(mypath) if isfile(join(mypath, f))]

    # get line from the feature extraction algorithm used in data for each file
    featuresmatrix = [info.get_line(name) for name in onlyfiles]

    # get data for classifier
    Y = [i[-2] for i in featuresmatrix]         # goal class
    Xtab = [i[0:-3] for i in featuresmatrix]    # string with features separated by \t
    X = []                                      # features
    for feature in Xtab:
        X.append(feature.split('\t'))           # features from each sample

    clf = DecisionTreeClassifier()

    clf.fit(X, Y)

    return clf


def classify_ex(clf, xx):
    x = []
    x.append(xx[0:-3].split('\t'))
    return clf.predict(x)


def how_certain(clf1, x):
    print(clf1.classes_)
    print("Decision Tree:")
    print(clf1.predict_proba(x))
    print(clf1.predict(x))