import csv
from scipy import *
from scipy.stats import kurtosis
from scipy.stats import skew
from scipy.stats import pearsonr
import numpy as np
import novainstrumentation as ni

# -------------------------------------


def get_line(file_name):
    csv_file_name = file_name
    goal_class = str(csv_file_name)[1].upper()

    with open('database_final\\' + csv_file_name) as csv_file:
        # get comma separated values from file
        data = list(csv.reader(csv_file, delimiter=';'))

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
    # class_n_for_hist = int(1 + 3.32 * log(len(t)))

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

    # corrXX1, corrXX2 = pearsonr(x, x) # autocorrelation without time-delay is useless (always 1)
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



    return '\t'.join((
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
        r'%.2f' % (z_peak_freq,),
        # target class
        r'' + str(goal_class) + '\n'
        ))


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
