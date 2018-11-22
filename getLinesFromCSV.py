import csv
from scipy import *
from scipy.stats import kurtosis
from scipy.stats import skew
from scipy.stats import pearsonr

# -------------------------------------

def get_line(file_name):
    csvFileName = file_name
    goalClass = str(csvFileName)[1].upper()

    with open('database_final\\' + csvFileName) as csvfile:
        # get comma separated values from file
        data = list(csv.reader(csvfile, delimiter=';'))

    # get time vector (x-axis)
    tt = [float(i[0].replace(',', '.')) for i in data]

    # get X acceleration (replace comma with dot for numeric parsing)
    xx = [float(i[1].replace(',', '.')) for i in data]

    # get Y acceleration (replace comma with dot for numeric parsing)
    yy = [float(i[2].replace(',', '.')) for i in data]

    # get Z acceleration (replace comma with dot for numeric parsing)
    zz = [float(i[3].replace(',', '.')) for i in data]

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

    '''
    # plot accelerations in X, Y and Z
    plt.figure(file_name)
    step = 1  # to decrease aquisition rate if needed
    plot(t[::step], x[::step], 'r.-')
    plot(t[::step], y[::step], 'g.-')
    plot(t[::step], z[::step], 'b.-')
    legend(['x', 'y', 'z'])  # to label the plotted lines
    plt.show()
    '''

    # number of classes for histograms
    class_n_for_hist = int(1 + 3.32 * log(len(t)))

    # X data
    muX = mean(x)
    medianX = median(x)
    sigmaX = std(x)
    kurtosisX = kurtosis(x)
    skewX = skew(x)
    vppX = abs(max(x) - min(x))
    maxX = max(x)
    minX = min(x)

    # corrXX1, corrXX2 = pearsonr(x, x) # autocorrelation without time-delay is useless (always 1)
    corrXY1, corrXY2 = pearsonr(x, y)
    corrXZ1, corrXZ2 = pearsonr(x, z)
    countCrossXZ = 0
    for i in range(len(x) - 1):
        if x[i] > z[i] and x[i + 1] < z[i + 1]:
            countCrossXZ += 1
        elif x[i] < z[i] and x[i + 1] > z[i + 1]:
            countCrossXZ += 1

    sumX = sum(x)
    totalTime = t[-1] - t[0]
    period = totalTime / len(t)
    integralX = sumX * period

    return '\t'.join((
    r'%.2f' % (muX, ),
    r'%.2f' % (medianX, ),
    r'%.2f' % (sigmaX,),
    r'%.2f' % (kurtosisX, ),
    r'%.2f' % (skewX, ),
    r'%.2f' % (corrXY1,),
    r'%.2f' % (corrXZ1, ),
    r'%.2f' % (countCrossXZ,),
    r'%.2f' % (vppX,),
    r'%.2f' % (maxX,),
    r'%.2f' % (minX,),
    r'%.2f' % (len(t),),
    r'%.2f' % (integralX,),
    r'%.2f' % (sumX,),
    r'' + str(goalClass) + '\n'
    ))

# -------------------------------------
