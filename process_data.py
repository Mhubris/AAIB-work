import matplotlib
matplotlib.use('Agg')
from pylab import *
import matplotlib.pyplot as plt
import classify_example_randomforest_orange as classify_sample
import process_data_AAIB2018 as my_pd

# fit classifier
clf = classify_sample.get_fit()
# -------------------------------------
length_inches = 18.0
width_inches = 5.0
# -------------------------------------

tt, xx, yy, zz = my_pd.get_values_from_csv('bt002.csv')

t, x, y, z = my_pd.remove_duplicates(tt, xx, yy, zz)

uniformTime, newX, newY, newZ = my_pd.uniform_time(t, x, y, z)

t = uniformTime
x, y, z = my_pd.smooth_signal(newX, newY, newZ)

t = t[10:-10]
x = x[10:-10]
y = y[10:-10]
z = z[10:-10]
newX = newX[10:-10]
newY = newY[10:-10]
newZ = newZ[10:-10]

# x, y and z signal in time-domain
my_pd.get_signal_figure(t, x, y, z, newX, newY, newZ, save_fig=True, file_name="plot_signals.jpg")

# x, y and z spectrogram -----------------------------------------------------------------------------------------------
my_pd.get_spectrograms_figure(t, x, y, z, save_fig=True, file_name='spectrograms.jpg')

# histograms -----------------------------------------------------------------------------------------------------------
my_pd.get_histograms_figure(t, x, y, z, save_fig=True, file_name='histograms.jpg')

# extract features
str_features = my_pd.get_tab_separated_features(t, x, y, z)

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
