import csv
from scipy import *
from scipy.stats import kurtosis
from scipy.stats import skew
from scipy.stats import pearsonr
import numpy as np
import process_data_AAIB2018 as my_pd

# -------------------------------------


def get_line(file_name):

    # get values
    tt, xx, yy, zz = my_pd.get_values_from_csv(file_name)

    # get target class
    goal_class = my_pd.get_target_class_from_csv(file_name)

    # remove samples with same time-stamp
    t, x, y, z = my_pd.remove_duplicates(tt, xx, yy, zz)

    uniform_time, new_x, new_y, new_z = my_pd.uniform_time(t, x, y, z)
    t = uniform_time
    x, y, z = my_pd.smooth_signal(new_x, new_y, new_z)

    # get features
    features = my_pd.get_tab_separated_features(t, x, y, z)

    # return features and target class (separated by tabs)
    return '\t'.join((features, str(goal_class) + '\n'))


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

# -------------------------------------
