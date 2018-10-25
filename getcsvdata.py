import csv
from numpy import *
from pylab import *
import matplotlib as plt
import novainstrumentation as ni

# open csv file
with open('datafiles\\myfile.csv') as csvfile:
    # get comma separated values from file
    data = list(csv.reader(csvfile, delimiter=';'))

# get time vector (x-axis)
t = [float(i[0].replace(',','.')) for i in data]

# get X acceleration (replace comma with dot for numeric parsing)
x = [float(i[1].replace(',','.')) for i in data]

# get Y acceleration (replace comma with dot for numeric parsing)
y = [float(i[2].replace(',','.')) for i in data]

# get Z acceleration (replace comma with dot for numeric parsing)
z = [float(i[3].replace(',','.')) for i in data]

# plot accelerations in X, Y and Z
plot(t, x)
plot(t, y)
plot(t, z)

plt.pyplot.show()