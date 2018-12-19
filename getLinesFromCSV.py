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
    x, y, z = my_pd.smooth_signal(new_x, new_y, new_z , window_len=4)

    # get features
    features = my_pd.get_tab_separated_features(t, x, y, z)
    # return features and target class (separated by tabs)
    return '\t'.join((features, str(goal_class) + '\n'))


def get_first_line():
    return '\t'.join((
        r'abs_mean_x',
        r'abs_mean_y',
        r'abs_mean_z',
        r'complexity_x',
        r'complexity_y',
        r'complexity_z',
        r'signal_power_x',
        r'signal_power_y',
        r'signal_power_z',
        r'spectral_entropy_x',
        r'spectral_entropy_y',
        r'spectral_entropy_z',
        # r'spectral_centroid_x',
        # r'spectral_centroid_y',
        # r'spectral_centroid_z',
        r'corr_xy1',
        # r'corr_xz1',
        r'corr_yz1',
        # r'count_cross_xz',
        r'count_cross_xy',
        # r'count_cross_yz',
        # ----- X data features
        r'mu_x',
        # r'median_x',
        r'sigma_x',
        r'kurtosis_x',
        # r'skew_x',
        # r'vpp_x',
        r'max_x',
        # r'min_x',
        r'sum_x',
        # r'max_f_x',
        r'max_fs_x',
        # ----- Y data features
        # r'mu_y',
        # r'median_y',
        r'sigma_y',
        # r'kurtosis_y',
        # r'skew_y',
        # r'vpp_y',
        # r'max_y',
        # r'min_y',
        r'sum_y',
        # r'max_f_y',
        r'max_fs_y',
        # ----- Z data features
        # r'mu_z',
        # r'median_z',
        # r'sigma_z',
        # r'kurtosis_z',
        # r'skew_z',
        r'vpp_z',
        # r'max_z',
        r'min_z',
        r'sum_z',
        # r'max_f_z',
        r'max_fs_z',
        # ----- new features
        # r'count_x_up',
        # r'count_y_up',
        # r'count_z_up',
        # ----- target class
        r'goalClass' + '\n'
        ))

# -------------------------------------