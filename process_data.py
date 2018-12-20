import matplotlib
#matplotlib.use('Agg')
from pylab import *
import matplotlib.pyplot as plt
import classify_example_randomforest_orange as classify_sample
import process_data_AAIB2018 as my_pd
from joblib import dump, load

# fit classifier -------------------------------------------------------------------------------------------------------
#clf = load('teste.joblib')
clf= classify_sample.get_fit()
classify_sample.get_confusion_matrix(clf)

# -------------------------------------
# suggested values for figure size (functions that create figures already have pre-defined default values)
length_inches = 18.0
width_inches = 5.0
# -------------------------------------

# process acquired data ------------------------------------------------------------------------------------------------

# when analysing data post-acquisition without the raspberrypi, raw data is extracted from a .csv file
tt, xx, yy, zz = my_pd.get_values_from_csv('cc.csv', '')

# duplicates are removed from the raw data, to make sure there aren't any samples with the same timestamp
t, x, y, z = my_pd.remove_duplicates(tt, xx, yy, zz)

# as the acquisition frequency may vary, it's necessary to interpolate values between the first and last timestamp
# and re-sample the signal in order to have a constant time interval between samples
uniformTime, newX, newY, newZ = my_pd.uniform_time(t, x, y, z)

# the time vector used for the rest of the program is the linear spaced one
t = uniformTime

# a smoothing filter (low-pass filter) is applied to reduce the effect of artifacts caused by the previous interpolation
# we decided to use a window length of 4 (empirically found that value to produce the best results)
x, y, z = my_pd.smooth_signal(newX, newY, newZ, window_len=4)


# x, y and z signals in time-domain ------------------------------------------------------------------------------------
my_pd.get_signal_figure(t, x, y, z, newX, newY, newZ, save_fig=False, file_name="plot_signals.jpg")

# x, y and z spectrograms ----------------------------------------------------------------------------------------------
my_pd.get_spectrograms_figure(t, x, y, z, save_fig=False, file_name='spectrograms.jpg')

# x, y and z histograms ------------------------------------------------------------------------------------------------
my_pd.get_histograms_figure(t, x, y, z, save_fig=False, file_name='histograms.jpg')

# extract features
str_features = my_pd.get_tab_separated_features(t, x, y, z)
# for debugging purposes, print the extracted features
print(str_features)

# classify example -----------------------------------------------------------------------------------------------------
est_y = classify_sample.classify_ex(clf, str_features)
class_number = my_pd.get_class_number_from_letter(est_y)
print(class_number)


'''
0 - P - Parado
1 - I - Teste inválido (não andou em linha reta)
2 - S - Sim, precisa de cadeira elétrica
3 - N - Não, não precisa de cadeira elétrica (pode usar cadeira manual)
4 - E - Foi empurrado
5 - T - Andou para trás
6 - X - O telemóvel não está colocado no suporte
'''
