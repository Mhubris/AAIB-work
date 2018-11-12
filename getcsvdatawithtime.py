import csv
import numpy as np
import matplotlib.pyplot as plt
from pylab import *
from scipy import *
import novainstrumentation as ni
import sklearn

# open csv file
with open('datafiles\\I001_esq.csv') as csvfile:
    # get comma separated values from file
    data = list(csv.reader(csvfile, delimiter=';'))

# get time vector (x-axis)
tt = [float(i[0].replace(',','.')) for i in data]

# get X acceleration (replace comma with dot for numeric parsing)
xx = [float(i[1].replace(',','.')) for i in data]

# get Y acceleration (replace comma with dot for numeric parsing)
yy = [float(i[2].replace(',','.')) for i in data]

# get Z acceleration (replace comma with dot for numeric parsing)
zz = [float(i[3].replace(',','.')) for i in data]

# create lists that will store the data values
t = []
x = []
y = []
z = []
# to make sure there aren't any samples with the same timestamp
for i in range(len(tt)-1):
    if tt[i] != tt[i+1]:
        t.append(tt[i])
        x.append(xx[i])
        y.append(yy[i])
        z.append(zz[i])

# plot accelerations in X, Y and Z
plt.figure(1)
step = 1 # to decrease aquisition rate if needed
plot(t[::step], x[::step], 'r.-')
plot(t[::step], y[::step], 'g.-')
plot(t[::step], z[::step], 'b.-')
legend(['x','y','z']) # to label the plotted lines


# number of classes for histograms
class_n_for_hist = int(len(t)/10)
# parameters for spectrogram
NFFT = 128
Fs = len(t)/10
noverlap = 64

# X data
figX, (axX1, axX2) = plt.subplots(nrows = 2)
mu = mean(x)
median = median(x)
sigma = std(x)
textstr = '\n'.join((
    r'x-axis',
    r'$\mu=%.2f$' % (mu, ),
    r'$\mathrm{median}=%.2f$' % (median, ),
    r'$\sigma=%.2f$' % (sigma, )))
axX1.hist(x,class_n_for_hist)
# these are matplotlib.patch.Patch properties
props = dict(boxstyle='round', facecolor='wheat', alpha=0.5)

# place a text box in upper left in axes coords
axX1.text(0.05, 0.95, textstr, transform=axX1.transAxes, fontsize=14,
        verticalalignment='top', bbox=props)

Pxx, freqs, bins, im = axX2.specgram(x, NFFT=NFFT, Fs=Fs, noverlap=noverlap)
# The `specgram` method returns 4 objects. They are:
# - Pxx: the periodogram
# - freqs: the frequency vector
# - bins: the centers of the time bins
# - im: the matplotlib.image.AxesImage instance representing the data in the plot


'''
# Y data
figY, axY = plt.subplots()
mu = mean(y)
median = median(y)
sigma = std(y)
textstr = '\n'.join((
    r'y-axis',
    r'$\mu=%.2f$' % (mu, ),
    r'$\mathrm{median}=%.2f$' % (median, ),
    r'$\sigma=%.2f$' % (sigma, )))
axY.hist(y,class_n_for_hist)
# these are matplotlib.patch.Patch properties
props = dict(boxstyle='round', facecolor='wheat', alpha=0.5)

# place a text box in upper left in axes coords
axY.text(0.05, 0.95, textstr, transform=axY.transAxes, fontsize=14,
        verticalalignment='top', bbox=props)

# Z data
fig, axZ = plt.subplots()
mu = mean(z)
median = median(z)
sigma = std(z)
textstr = '\n'.join((
    r'z-axis',
    r'$\mu=%.2f$' % (mu, ),
    r'$\mathrm{median}=%.2f$' % (median, ),
    r'$\sigma=%.2f$' % (sigma, )))
axZ.hist(z,class_n_for_hist)
# these are matplotlib.patch.Patch properties
props = dict(boxstyle='round', facecolor='wheat', alpha=0.5)

# place a text box in upper left in axes coords
axZ.text(0.05, 0.95, textstr, transform=axZ.transAxes, fontsize=14,
        verticalalignment='top', bbox=props)

'''

# Filter signal to improve visualization and remove noise

# Classify signals with decision tree algorithm


# needs .show() to plot as image in pycharm
#plt.pyplot.show()
plt.show()