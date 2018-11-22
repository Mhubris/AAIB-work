import numpy as np
import matplotlib.pyplot as plt
from pylab import *
from scipy import *
import novainstrumentation as ni
import sklearn as sk


class BayesClassifier1d:    #   1dBayesClassifier

    def fit(self, x, y):
        self.classes = unique(y)
        self.mu = {}
        self.std = {}
        for c in self.classes:
            self.mu[c] = mean(x[y == c])
            self.std[c] = std(x[y == c])

    def predict(self, x):
        prob = [normpdf(x, self.mu[c], self.std[c]) for c in self.classes]
        return self.classes[argmax(prob)]

