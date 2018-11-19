import csv
import numpy as np
import matplotlib.pyplot as plt
from pylab import *
from scipy import *
from scipy.stats import kurtosis
from scipy.stats import skew
from scipy.stats import pearsonr
from scipy.interpolate import spline
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
        t.append(tt[i]-tt[0])
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
class_n_for_hist = int(1+3.32*log(len(t)))

# X data
figX, (axX1) = plt.subplots()
muX = mean(x)
medianX = median(x)
sigmaX = std(x)
kurtosisX = kurtosis(x)
skewX = skew(x)
vppX = abs(max(x)-min(x))
maxX = max(x)
minX = min(x)

corrXX1, corrXX2 = pearsonr(x,x)
corrXY1, corrXY2 = pearsonr(x,y)
corrXZ1, corrXZ2 = pearsonr(x,z)
countCrossXZ = 0
for i in range(len(x)-1):
    if x[i] > z[i] and x[i+1] < z[i+1]:
        countCrossXZ += 1
    elif x[i] < z[i] and x[i+1] > z[i+1]:
        countCrossXZ += 1

sumX = sum(x)
period = 10000/len(t)
integralX = sumX*period

textstr = '\n'.join((
    r'        x-axis',
    r'$\mu=%.2f$' % (muX, ),
    r'$\mathrm{median}=%.2f$' % (medianX, ),
    r'$\sigma=%.2f$' % (sigmaX,),
    r'$\mathrm{kurtosis}=%.2f$' % (kurtosisX, ),
    r'$\mathrm{skewness}=%.2f$' % (skewX, ),
    #r'$\mathrm{correlationXX}=%.2f$' % (corrXX1,),
    r'$\mathrm{correlationXY}=%.2f$' % (corrXY1,),
    r'$\mathrm{correlationXZ}=%.2f$' % (corrXZ1, ),
    r'$\mathrm{crossXZ}=%.2f$' % (countCrossXZ,),
    r'$\mathrm{Vpp}=%.2f$' % (vppX,),
    r'$\mathrm{max}=%.2f$' % (maxX,),
    r'$\mathrm{min}=%.2f$' % (minX,),
    r'$\mathrm{sampleSize}=%.2f$' % (len(t),),
    r'$\mathrm{integral}=%.2f$' % (integralX,),
    r'$\mathrm{sum}=%.2f$' % (sumX,)
    ))
axX1.hist(x, alpha = 0.5)
# these are matplotlib.patch.Patch properties
props = dict(boxstyle='round', facecolor='wheat', alpha=0.5)

# place a text box in upper left in axes coords
axX1.text(0.05, 0.95, textstr, transform=axX1.transAxes, fontsize=14,
        verticalalignment='top', bbox=props)


# Filter signal to improve visualization and remove noise
uniformTime = []
for i in range(200):
    uniformTime.append(i*period)
newX = spline(t,x, uniformTime)
figure()
plot(newX)




# Classify signals with decision tree algorithm


# needs .show() to plot as image in pycharm
#plt.pyplot.show()
plt.show()