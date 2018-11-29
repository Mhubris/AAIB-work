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


#print(Xtab)
#print(X)
#print(Y)


clf1 = DecisionTreeClassifier()
clf2 = KNeighborsClassifier()
clf3 = SVC(kernel="linear", C=0.025)
clf4 = SVC(gamma=2, C=1)
clf5 = RandomForestClassifier(max_depth=5, n_estimators=10, max_features=1)
clf6 = AdaBoostClassifier()
clf7 = RandomForestClassifier()

clf1.fit(X, Y)
clf2.fit(X, Y)
clf3.fit(X, Y)
clf4.fit(X, Y)
clf5.fit(X, Y)
clf6.fit(X, Y)
clf7.fit(X, Y)

x = []
new_example = 'je3.csv'
x.append(newdata.get_line(new_example)[0:-3].split('\t'))
print(x)
print(new_example)

print(clf1.classes_)

print("Decision Tree:")
print(clf1.predict(x))
print(clf1.predict_proba(x))

print("K-Nearest Neighbor:")
print(clf2.predict(x))
print(clf2.predict_proba(x))

print("Support Vector with linear kernel and C = 0.025:")
print(clf3.predict(x))

print("Support Vector with gamma = 2 and C = 0.025:")
print(clf4.predict(x))

print("Random Forest with max_depth = 5, n_estimators = 10, max_features = 1")
print(clf5.predict(x))
print(clf5.predict_proba(x))

print("AdaBoost")
print(clf6.predict(x))
print(clf6.predict_proba(x))

print("Random Forest (default)")
print(clf7.predict(x))
print(clf7.predict_proba(x))



# -------------------------------------

# Classify signals
'''
def class_RandomForest(Xtrain, Ytrain):
    clf = RandomForestClassifier()
    clf.fit(Xtrain, Ytrain)  # X sao features de cada amostra (feature tem de ser real), Y e classe de cada amostra
    Yestimado = clf.predict(Xtest)
    error = sum(Yestimado != Ytest)
    return Yestimado
'''



'''
def get_first_line():
    return '\t'.join((
        r'corrXY1',
        r'corrXZ1',
        r'corrYZ1',
        r'countCrossXZ',
        r'countCrossXY',
        r'countCrossYZ',
    # X data features
        r'muX',
        r'medianX',
        r'sigmaX',
        r'kurtosisX',
        r'skewX',
        r'vppX',
        r'maxX',
        r'minX',
        r'integralX',
        r'sumX',
        r'x_min_freq',
        r'x_max_freq',
        r'x_peak_freq',
    # Y data features
        r'muY',
        r'medianY',
        r'sigmaY',
        r'kurtosisY',
        r'skewY',
        r'vppY',
        r'maxY',
        r'minY',
        r'integralY',
        r'sumY',
        r'y_min_freq',
        r'y_max_freq',
        r'y_peak_freq',
    # Z data features
        r'muZ',
        r'medianZ',
        r'sigmaZ',
        r'kurtosisZ',
        r'skewZ',
        r'vppZ',
        r'maxZ',
        r'minZ',
        r'integralZ',
        r'sumZ',
        r'z_min_freq',
        r'z_max_freq',
        r'z_peak_freq',
    # target class
        r'goalClass' + '\n'
        ))
'''
# -------------------------------------
