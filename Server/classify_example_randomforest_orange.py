from scipy import *
from sklearn.ensemble import RandomForestClassifier
from sklearn.ensemble import RandomForestClassifier
from sklearn.model_selection import train_test_split
from sklearn import metrics
from sklearn.metrics import confusion_matrix
import pickle
import getLinesFromCSV as info

from os import listdir
from os.path import isfile, join
from joblib import dump, load
# -----------------------------------------------------------


def get_fit(my_path='//home//pi//Desktop//AAIB_Project//database_final//'):

    X, Y = get_x_y(my_path)

    # best option according to Orange
    clf = RandomForestClassifier(
        max_depth=5,
        n_estimators=60,
        max_features=7,
        min_samples_leaf=5)

    clf.fit(X, Y)
    dump(clf, '//home//pi//Desktop//AAIB_Project//training.joblib')
    return clf


def classify_ex(clf, xx):
    x = []
    x.append(xx[0:-3].split('\t'))
    return clf.predict(x)

def classify_ex_phone(clf, xx):
    x = []
    x.append(xx.split('\t'))
    return clf.predict(x)

def get_x_y (my_path='//home//pi//Desktop//AAIB_Project//database_final//'):
    """ Opens every file in the folder selected by my_path, gets data for classifier"""
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

    return X,Y


def get_confusion_matrix(clf,my_path='//home//pi//Desktop//AAIB_Project//database_final//'):
    X,Y = get_x_y(my_path)
    # Split the datset into training and testing dataset
    x_train, x_test, y_train, y_test = train_test_split(X, Y, test_size=.25)
    # Test the just trained classifier
    predictions = clf.predict(x_test)
    # Print the confusion matrix
    print(confusion_matrix(y_test, predictions))
    # Print the accuracy
    print("Accuracy: " + str(metrics.accuracy_score(y_test, predictions)))



def how_certain(clf1, x):
    print(clf1.classes_)
    print("Random Forest:")
    print(clf1.predict_proba(x))
    print(clf1.predict(x))
