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


print(Xtab)
print(X)
print(Y)


clf = DecisionTreeClassifier()
#clf = KNeighborsClassifier()
#clf = SVC()

clf.fit(X, Y)
x = []
x.append(newdata.get_line('ms2.csv')[0:-3].split('\t'))
print(x)

result = clf.predict(x)
print(result)
prob = clf.predict_proba(x)
print(prob)






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
