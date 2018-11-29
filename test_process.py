from scipy.stats import kurtosis
from scipy.stats import skew
from scipy.stats import pearsonr
from scipy.interpolate import spline
from scipy import signal
from pylab import *
import numpy as np
import matplotlib.pyplot as plt
import novainstrumentation as ni

import classify1Example

# -------------------------------------

a = [(0.0, 1.1, 2.2, 3.3), (0.2, 1.2, 2.3, 3.4),
     (0.3, 1.3, 2.4, 3.5), (1.5, 1.4, 2.5, 3.6),
     (2.3, 1.5, 2.6, 3.7), (2.5, 1.6, 2.7, 3.8),
     (3.0, 1.7, 2.8, 3.9), (3.2, 1.2, 2.3, 3.4),
     (3.4, 1.3, 2.4, 3.5), (3.6, 1.4, 2.5, 3.6),
     (4.0, 1.5, 2.6, 3.7), (5.5, 1.6, 2.7, 3.8),
     (5.7, 1.7, 2.8, 3.9), (6.0, 1.8, 2.9, 3.10)]

# get time vector (x-axis)
tt = [(i[0]) for i in a]

# get X acceleration (replace comma with dot for numeric parsing)
xx = [(i[1]) for i in a]

# get Y acceleration (replace comma with dot for numeric parsing)
yy = [(i[2]) for i in a]

# get Z acceleration (replace comma with dot for numeric parsing)
zz = [(i[3]) for i in a]

# create lists that will store the data values
t = []
x = []
y = []
z = []
# to make sure there aren't any samples with the same timestamp
for i in range(len(tt) - 1):
    if tt[i] != tt[i + 1]:
        t.append(tt[i] - tt[0])
        x.append(xx[i])
        y.append(yy[i])
        z.append(zz[i])

# plot accelerations in X, Y and Z
plt.figure('test')
step = 1  # to decrease aquisition rate if needed
plot(t[::step], x[::step], 'r.-')
plot(t[::step], y[::step], 'g.-')
plot(t[::step], z[::step], 'b.-')
legend(['x', 'y', 'z'])  # to label the plotted lines


# signal with constant time
plt.figure('uniform time')
uniformTime = np.linspace(t[0], t[-1], len(t))
newX = spline(t, x, uniformTime)
newY = spline(t, y, uniformTime)
newZ = spline(t, z, uniformTime)
step = 1 # to decrease aquisition rate if needed
plot(uniformTime[::step], newX[::step], 'r.-')
plot(uniformTime[::step], newY[::step], 'g.-')
plot(uniformTime[::step], newZ[::step], 'b.-')


t = uniformTime
# plot smooth accelerations in X, Y and Z
plt.figure('smooth')
x = array(ni.smooth(newX, window_len=5))
y = array(ni.smooth(newY))
z = array(ni.smooth(newZ))
step = 1  # to decrease aquisition rate if needed
plot(t[::step], x[::step], 'r.-')
plot(t[::step], y[::step], 'g.-')
plot(t[::step], z[::step], 'b.-')
legend(['x', 'y', 'z'])  # to label the plotted lines

# extract features
total_time = t[-1] - t[0]
period = total_time / len(t)

# X data
mu_x = mean(x)
median_x = median(x)
sigma_x = std(x)
kurtosis_x = kurtosis(x)
skew_x = skew(x)
vpp_x = abs(max(x) - min(x))
max_x = max(x)
min_x = min(x)
sum_x = sum(x)
integral_x = sum_x * period

# Y data
mu_y = mean(y)
median_y = median(y)
sigma_y = std(y)
kurtosis_y = kurtosis(y)
skew_y = skew(y)
vpp_y = abs(max(y) - min(y))
max_y = max(y)
min_y = min(y)
sum_y = sum(y)
integral_y = sum_y * period

# Z data
mu_z = mean(z)
median_z = median(z)
sigma_z = std(z)
kurtosis_z = kurtosis(z)
skew_z = skew(z)
vpp_z = abs(max(z) - min(z))
max_z = max(z)
min_z = min(z)
sum_z = sum(z)
integral_z = sum_z * period

corr_xy1, corr_xy2 = pearsonr(x, y)
corr_xz1, corr_xz2 = pearsonr(x, z)
corr_yz1, corr_yz2 = pearsonr(y, z)
count_cross_xz = 0
count_cross_xy = 0
count_cross_yz = 0
for i in range(len(x) - 1):
    # cross between X and Z
    if x[i] > z[i] and x[i + 1] < z[i + 1]:
        count_cross_xz += 1
    elif x[i] < z[i] and x[i + 1] > z[i + 1]:
        count_cross_xz += 1
    # cross between X and Y
    if x[i] > y[i] and x[i + 1] < y[i + 1]:
        count_cross_xy += 1
    elif x[i] < y[i] and x[i + 1] > y[i + 1]:
        count_cross_xy += 1
    # cross between Y and Z
    if y[i] > z[i] and y[i + 1] < z[i + 1]:
        count_cross_yz += 1
    elif y[i] < z[i] and y[i + 1] > z[i + 1]:
        count_cross_yz += 1

# spectral domain auxiliar funtions to get spectral features from X data
x_fft = np.fft.fft(x)
x_freqs = np.fft.fftfreq(len(x_fft))
x_peak_freq_index = np.argmax(np.abs(x_fft))
# spectral domain auxiliar funtions to get spectral features from Y data
y_fft = np.fft.fft(y)
y_freqs = np.fft.fftfreq(len(y_fft))
y_peak_freq_index = np.argmax(np.abs(y_fft))
# spectral domain auxiliar funtions to get spectral features from Z data
z_fft = np.fft.fft(z)
z_freqs = np.fft.fftfreq(len(z_fft))
z_peak_freq_index = np.argmax(np.abs(z_fft))

# spectral features from X data
x_min_freq = x_freqs.min()
x_max_freq = x_freqs.max()
x_peak_freq = x_freqs[x_peak_freq_index]  # not in Hertz
# spectral features from Y data
y_min_freq = y_freqs.min()
y_max_freq = y_freqs.max()
y_peak_freq = y_freqs[x_peak_freq_index]  # not in Hertz
# spectral features from Z data
z_min_freq = y_freqs.min()
z_max_freq = y_freqs.max()
z_peak_freq = y_freqs[x_peak_freq_index]  # not in Hertz


# spectrograms -----------------------------

fs = (t[-1]/len(t))

figure('x spect')
fx, tx, Sxx = signal.spectrogram(x, fs)
plt.pcolormesh(tx, fx, Sxx)
plt.ylabel('Frequency [Hz]')
plt.xlabel('Time [sec]')

figure('y spect')
fy, ty, Syy = signal.spectrogram(y, fs)
plt.pcolormesh(ty, fy, Syy)
plt.ylabel('Frequency [Hz]')
plt.xlabel('Time [sec]')

figure('z spect')
fz, tz, Szz = signal.spectrogram(z, fs)
plt.pcolormesh(tz, fz, Szz)
plt.ylabel('Frequency [Hz]')
plt.xlabel('Time [sec]')


# histograms --------------------------------
figX, (axX1) = plt.subplots()
figY, (axY1) = plt.subplots()
figZ, (axZ1) = plt.subplots()

# number of classes for histograms
class_n_for_hist = int(1 + 3.32 * log(len(t)))

# these are matplotlib.patch.Patch properties
props = dict(boxstyle='round', facecolor='wheat', alpha=0.5)

# x data
textstr_x = '\n'.join((
    r'        x-axis',
    r'$\mu=%.2f$' % (mu_x, ),
    r'$\mathrm{median}=%.2f$' % (median_x, ),
    r'$\sigma=%.2f$' % (sigma_x,),
    r'$\mathrm{kurtosis}=%.2f$' % (kurtosis_x, ),
    r'$\mathrm{skewness}=%.2f$' % (skew_x, ),
    r'$\mathrm{V_{pp}}=%.2f$' % (vpp_x,),
    r'$\mathrm{max}=%.2f$' % (max_x,),
    r'$\mathrm{min}=%.2f$' % (min_x,),
    r'$\mathrm{integral}=%.2f$' % (integral_x,),
    r'$\mathrm{sum}=%.2f$' % (sum_x,),
    r'$\mathrm{x_{min.freq}}=%.2f$' % (x_min_freq,),
    r'$\mathrm{x_{max.freq}}=%.2f$' % (x_max_freq,),
    r'$\mathrm{x_{peak.freq}}=%.2f$' % (x_peak_freq,),
    ))
axX1.hist(x, alpha=0.5)

# place a text box in upper left in axes coords
axX1.text(0.05, 0.95, textstr_x, transform=axX1.transAxes, fontsize=14, verticalalignment='top', bbox=props)

# y data

textstr_y = '\n'.join((
    r'        y-axis',
    r'$\mu=%.2f$' % (mu_y, ),
    r'$\mathrm{median}=%.2f$' % (median_y, ),
    r'$\sigma=%.2f$' % (sigma_y,),
    r'$\mathrm{kurtosis}=%.2f$' % (kurtosis_y, ),
    r'$\mathrm{skewness}=%.2f$' % (skew_y, ),
    r'$\mathrm{V_{pp}}=%.2f$' % (vpp_y,),
    r'$\mathrm{max}=%.2f$' % (max_y,),
    r'$\mathrm{min}=%.2f$' % (min_y,),
    r'$\mathrm{integral}=%.2f$' % (integral_y,),
    r'$\mathrm{sum}=%.2f$' % (sum_y,),
    r'$\mathrm{y_{min.freq}}=%.2f$' % (y_min_freq,),
    r'$\mathrm{y_{max.freq}}=%.2f$' % (y_max_freq,),
    r'$\mathrm{y_{peak.freq}}=%.2f$' % (y_peak_freq,),
    ))
axY1.hist(y, alpha=0.5)

# place a text box in upper left in axes coords
axY1.text(0.05, 0.95, textstr_y, transform=axY1.transAxes, fontsize=14, verticalalignment='top', bbox=props)

# z data

textstr_z = '\n'.join((
    r'        z-axis',
    r'$\mu=%.2f$' % (mu_z, ),
    r'$\mathrm{median}=%.2f$' % (median_z, ),
    r'$\sigma=%.2f$' % (sigma_z,),
    r'$\mathrm{kurtosis}=%.2f$' % (kurtosis_z, ),
    r'$\mathrm{skewness}=%.2f$' % (skew_z, ),
    r'$\mathrm{V_{pp}}=%.2f$' % (vpp_z,),
    r'$\mathrm{max}=%.2f$' % (max_z,),
    r'$\mathrm{min}=%.2f$' % (min_z,),
    r'$\mathrm{integral}=%.2f$' % (integral_z,),
    r'$\mathrm{sum}=%.2f$' % (sum_z,),
    r'$\mathrm{z_{min.freq}}=%.2f$' % (z_min_freq,),
    r'$\mathrm{z_{max.freq}}=%.2f$' % (z_max_freq,),
    r'$\mathrm{z_{peak.freq}}=%.2f$' % (z_peak_freq,),
    ))
axZ1.hist(z, alpha=0.5)

# place a text box in upper left in axes coords
axZ1.text(0.05, 0.95, textstr_z, transform=axZ1.transAxes, fontsize=14, verticalalignment='top', bbox=props)


# show everything
# plt.show()

str_features = '\t'.join((
    r'%.2f' % (corr_xy1,),
    r'%.2f' % (corr_xz1, ),
    r'%.2f' % (corr_yz1, ),
    r'%.2f' % (count_cross_xz,),
    r'%.2f' % (count_cross_xy,),
    r'%.2f' % (count_cross_yz,),

    # X data features
    r'%.2f' % (mu_x, ),
    r'%.2f' % (median_x, ),
    r'%.2f' % (sigma_x,),
    r'%.2f' % (kurtosis_x, ),
    r'%.2f' % (skew_x, ),
    r'%.2f' % (vpp_x,),
    r'%.2f' % (max_x,),
    r'%.2f' % (min_x,),
    r'%.2f' % (integral_x,),
    r'%.2f' % (sum_x,),
    r'%.2f' % (x_min_freq,),
    r'%.2f' % (x_max_freq,),
    r'%.2f' % (x_peak_freq,),

    # Y data features
    r'%.2f' % (mu_y, ),
    r'%.2f' % (median_y, ),
    r'%.2f' % (sigma_y,),
    r'%.2f' % (kurtosis_y, ),
    r'%.2f' % (skew_y, ),
    r'%.2f' % (vpp_y,),
    r'%.2f' % (max_y,),
    r'%.2f' % (min_y,),
    r'%.2f' % (integral_y,),
    r'%.2f' % (sum_y,),
    r'%.2f' % (y_min_freq,),
    r'%.2f' % (y_max_freq,),
    r'%.2f' % (y_peak_freq,),

    # Z data features
    r'%.2f' % (mu_z, ),
    r'%.2f' % (median_z, ),
    r'%.2f' % (sigma_z,),
    r'%.2f' % (kurtosis_z, ),
    r'%.2f' % (skew_z, ),
    r'%.2f' % (vpp_z,),
    r'%.2f' % (max_z,),
    r'%.2f' % (min_z,),
    r'%.2f' % (integral_z,),
    r'%.2f' % (sum_z,),
    r'%.2f' % (z_min_freq,),
    r'%.2f' % (z_max_freq,),
    r'%.2f' % (z_peak_freq,)
    ))


# classify example

clf = classify1Example.get_fit()

est_y = classify1Example.classify_ex(clf, str_features)

print(est_y)




# -------------------------------------


