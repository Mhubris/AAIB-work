import csv
from scipy import *
from scipy.stats import kurtosis
from scipy.stats import skew
from scipy.stats import pearsonr
import numpy as np
import novainstrumentation as ni
import matplotlib.pyplot as plt
from matplotlib.colors import ListedColormap
from sklearn.model_selection import train_test_split
from sklearn.preprocessing import StandardScaler
from sklearn.datasets import make_moons, make_circles, make_classification
from sklearn.neural_network import MLPClassifier
from sklearn.neighbors import KNeighborsClassifier
from sklearn.svm import SVC
from sklearn.gaussian_process import GaussianProcessClassifier
from sklearn.gaussian_process.kernels import RBF
from sklearn.tree import DecisionTreeClassifier
from sklearn.ensemble import RandomForestClassifier, AdaBoostClassifier
from sklearn.naive_bayes import GaussianNB
from sklearn.discriminant_analysis import QuadraticDiscriminantAnalysis
from sklearn.ensemble import RandomForestClassifier
from sklearn.datasets import make_classification

import getLinesFromCSV as info
import getLinesFromNewData as newdata

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
    print(clf1.predict(x))
    print(clf1.predict_proba(x))
