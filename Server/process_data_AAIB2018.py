import matplotlib
import csv
import re
import os
matplotlib.use('Agg')
from scipy.stats import kurtosis
from scipy.stats import skew
from scipy.stats import pearsonr
from scipy.interpolate import spline
from pylab import *
import numpy as np
import matplotlib.pyplot as plt
import smooth
# import classify_example_randomforest_orange as classify_sample


def get_values_from_csv(file_name, path='//home/pi//Desktop//AAIB_Project//database_final//'):
    """ Extracts the time vector, and accelerations in x, y, and z
        from a csv file obtained using phone accelerometers.
        Returns tt, xx, yy, zz. """
    with open(path + file_name) as csv_file:
        # get comma separated values from file
        data = list(csv.reader(csv_file, delimiter=';'))

    # get time vector (x-axis)
    tt = [float(i[0].replace(',', '.')) for i in data]

    # get X acceleration (replace comma with dot for numeric parsing)
    xx = [int(round(float(i[1].replace(',', '.'))*100)) for i in data]

    # get Y acceleration (replace comma with dot for numeric parsing)
    yy = [int(round(float(i[2].replace(',', '.'))*100)) for i in data]
    # get Z acceleration (replace comma with dot for numeric parsing)
    zz = [int(round(float(i[3].replace(',', '.'))*100)) for i in data]
    return tt, xx, yy, zz


def get_target_class_from_csv(file_name):
    """ Returns the target class (second char from file_name.
        The letter representing the target class is always upper-case. """
    return str(file_name)[1].upper()


def get_values_from_phone(phone_array):
    """ Extracts the time vector, and accelerations in x, y, and z
        from an array obtained using phone accelerometers.
        Returns tt, xx, yy, zz. """
    # get time vector (x-axis)
    tt = [(i[0]) for i in phone_array]

    # get X acceleration (replace comma with dot for numeric parsing)
    xx = [(i[1]) for i in phone_array]

    # get Y acceleration (replace comma with dot for numeric parsing)
    yy = [(i[2]) for i in phone_array]

    # get Z acceleration (replace comma with dot for numeric parsing)
    zz = [(i[3]) for i in phone_array]

    return tt, xx, yy, zz


def remove_duplicates(tt, xx, yy, zz):
    """ Removes samples with the same time-stamp.
        Returns t, x, y, z. """
    # create lists that will store the data values
    t = []
    x = []
    y = []
    z = []
    # to make sure there aren't any samples with the same timestamp
    for i in range(len(tt) - 1):
        if tt[i] != tt[i + 1]:
            t.append(tt[i] - tt[0])  # making sure the first sample has t = 0
            x.append(xx[i])
            y.append(yy[i])
            z.append(zz[i])

    return t, x, y, z


def uniform_time(t, x, y, z):
    """ Adjust samples to have a constant time interval between samples.
        Returns uniform_t, uniform_x, uniform_y, uniform_z. """
    uniform_t = np.linspace(t[0], t[-1], len(t))
    uniform_x = spline(t, x, uniform_t)
    uniform_y = spline(t, y, uniform_t)
    uniform_z = spline(t, z, uniform_t)
    return uniform_t, uniform_x, uniform_y, uniform_z


def smooth_signal(x, y, z, window_len=5):
    """ Smooth signal (low-pass filter).
        Returns new values for x, y, z."""
    x = array(smooth.smooth(x, window_len=window_len))
    y = array(smooth.smooth(y, window_len=window_len))
    z = array(smooth.smooth(z, window_len=window_len))
    return x, y, z


def get_tab_separated_features(t, x, y, z):
    """ Returns string with features separated by tabs. """
    # t is in milliseconds
    n = len(t)  # length of the signal
    Fs = (n / t[-1]) * pow(10, 3)  # sampling frequency
    # period = 1.0 / Fs               # sampling interval

    # ------- New_Features
    abs_mean_x = sum(abs(x)) / n
    abs_mean_y = sum(abs(y)) / n
    abs_mean_z = sum(abs(z)) / n

    signal_power_x = sum(log(x ** 2))
    signal_power_y = sum(log(y ** 2))
    signal_power_z = sum(log(z ** 2))

    complexity_x = 0
    complexity_y = 0
    complexity_z = 0

    spectral_centroid_x = 0
    spectral_centroid_y = 0
    spectral_centroid_z = 0

    spectral_entropy_x = -sum((x ** 2 / sum(x ** 2)) * log((x ** 2 / sum(x ** 2))))
    spectral_entropy_y = -sum((y ** 2 / sum(y ** 2)) * log((y ** 2 / sum(y ** 2))))
    spectral_entropy_z = -sum((z ** 2 / sum(z ** 2)) * log((z ** 2 / sum(z ** 2))))

    # ----- X data
    mu_x = mean(x)
    median_x = median(x)
    sigma_x = std(x)
    kurtosis_x = kurtosis(x)
    skew_x = skew(x)
    vpp_x = abs(max(x) - min(x))
    max_x = max(x)
    min_x = min(x)
    sum_x = sum(x)
    # integral_x = sum_x * period

    # ----- Y data
    mu_y = mean(y)
    median_y = median(y)
    sigma_y = std(y)
    kurtosis_y = kurtosis(y)
    skew_y = skew(y)
    vpp_y = abs(max(y) - min(y))
    max_y = max(y)
    min_y = min(y)
    sum_y = sum(y)
    # integral_y = sum_y * period

    # ----- Z data
    mu_z = mean(z)
    median_z = median(z)
    sigma_z = std(z)
    kurtosis_z = kurtosis(z)
    skew_z = skew(z)
    vpp_z = abs(max(z) - min(z))
    max_z = max(z)
    min_z = min(z)
    sum_z = sum(z)
    # integral_z = sum_z * period

    # ----- data obtained from more than one axis
    corr_xy1, corr_xy2 = pearsonr(x, y)
    corr_xz1, corr_xz2 = pearsonr(x, z)
    corr_yz1, corr_yz2 = pearsonr(y, z)

    '''
    count_cross_xz = 0
    count_cross_yz = 0
    x_up = False
    count_x_up = 0
    y_up = False
    count_y_up = 0
    z_up = False
    count_z_up = 0
    threshold_percent = 0.3
    '''
    count_cross_xy = 0

    # Features that need for loop
    for i in range(len(x) - 1):

        # cross between X and Y
        if x[i] > y[i] and x[i + 1] < y[i + 1]:
            count_cross_xy += 1
        elif x[i] < y[i] and x[i + 1] > y[i + 1]:
            count_cross_xy += 1

        complexity_x += abs(x[i + 1] - x[i])
        complexity_y += abs(y[i + 1] - y[i])
        complexity_z += abs(z[i + 1] - z[i])

        spectral_centroid_x += (x[i] * i)
        spectral_centroid_y += (y[i] * i)
        spectral_centroid_z += (z[i] * i)

        '''
        # cross between X and Z
        if x[i] > z[i] and x[i + 1] < z[i + 1]:
            count_cross_xz += 1
        elif x[i] < z[i] and x[i + 1] > z[i + 1]:
            count_cross_xz += 1

        # cross between Y and Z
        if y[i] > z[i] and y[i + 1] < z[i + 1]:
            count_cross_yz += 1
        elif y[i] < z[i] and y[i + 1] > z[i + 1]:
            count_cross_yz += 1

        # count number of times x goes above threshold_percent
        if not x_up and x[i] > mu_x + threshold_percent * mu_x:
            x_up = True
            count_x_up += 1
        if x_up and x[i] < mu_x + threshold_percent * mu_x:
            x_up = False

        # count number of times y goes above threshold_percent
        if not y_up and y[i] > mu_y + threshold_percent * mu_y:
            y_up = True
            count_y_up += 1
        if y_up and y[i] < mu_y + threshold_percent * mu_y:
            y_up = False

        # count number of times z goes above threshold_percent
        if not z_up and x[i] > mu_z + threshold_percent * mu_z:
            x_up = True
            count_z_up += 1
        if z_up and x[i] < mu_z + threshold_percent * mu_z:
            z_up = False
        '''
    spectral_centroid_x = spectral_centroid_x / sum_x
    spectral_centroid_y = spectral_centroid_y / sum_y
    spectral_centroid_z = spectral_centroid_z / sum_z

    # frequency domain features - X
    fs_x = abs(np.fft.fft(x))
    f_x = linspace(0, Fs / 2, n / 2)
    max_f_x = argmax(f_x)
    max_fs_x = argmax(fs_x)

    # frequency domain features - Y
    fs_y = abs(np.fft.fft(y))
    f_y = linspace(0, Fs / 2, n / 2)
    max_f_y = argmax(f_y)
    max_fs_y = argmax(fs_y)

    # frequency domain features - Z
    fs_z = abs(np.fft.fft(z))
    f_z = linspace(0, Fs / 2, n / 2)
    max_f_z = argmax(f_z)
    max_fs_z = argmax(fs_z)

    return '\t'.join((
        r'%.2f' % (abs_mean_x,),
        r'%.2f' % (abs_mean_y,),
        r'%.2f' % (abs_mean_z,),
        r'%.2f' % (complexity_x,),
        r'%.2f' % (complexity_y,),
        r'%.2f' % (complexity_z,),
        r'%.2f' % (signal_power_x,),
        r'%.2f' % (signal_power_y,),
        r'%.2f' % (signal_power_z,),
        r'%.2f' % (spectral_entropy_x,),
        r'%.2f' % (spectral_entropy_y,),
        r'%.2f' % (spectral_entropy_z,),
        #r'%.2f' % (spectral_centroid_x,),
        #r'%.2f' % (spectral_centroid_y,),
        #r'%.2f' % (spectral_centroid_z,),
        r'%.2f' % (corr_xy1,),
        # r'%.2f' % (corr_xz1,),
        r'%.2f' % (corr_yz1,),
        # r'%.2f' % (count_cross_xz,),
        r'%.2f' % (count_cross_xy,),
        # r'%.2f' % (count_cross_yz,),
        # ----- X data features
        r'%.2f' % (mu_x,),
        # r'%.2f' % (median_x,),
        r'%.2f' % (sigma_x,),
        r'%.2f' % (kurtosis_x,),
        # r'%.2f' % (skew_x,),
        # r'%.2f' % (vpp_x,),
        r'%.2f' % (max_x,),
        # r'%.2f' % (min_x,),
        r'%.2f' % (sum_x,),
        #r'%.2f' % (max_f_x,),
        r'%.2f' % (max_fs_x,),
        # ----- Y data features
        # r'%.2f' % (mu_y,),
        # r'%.2f' % (median_y,),
        r'%.2f' % (sigma_y,),
        # r'%.2f' % (kurtosis_y,),
        # r'%.2f' % (skew_y,),
        # r'%.2f' % (vpp_y,),
        # r'%.2f' % (max_y,),
        # r'%.2f' % (min_y,),
        r'%.2f' % (sum_y,),
        #r'%.2f' % (max_f_y,),
        r'%.2f' % (max_fs_y,),
        # ----- Z data features
        # r'%.2f' % (mu_z,),
        # r'%.2f' % (median_z,),
        # r'%.2f' % (sigma_z,),
        # r'%.2f' % (kurtosis_z,),
        # r'%.2f' % (skew_z,),
        r'%.2f' % (vpp_z,),
        # r'%.2f' % (max_z,),
        r'%.2f' % (min_z,),
        r'%.2f' % (sum_z,),
        #r'%.2f' % (max_f_z,),
        r'%.2f' % (max_fs_z,),
        # ----- new features
        # r'%.2f' % (count_x_up,),
        # r'%.2f' % (count_y_up,),
        # r'%.2f' % (count_z_up,)
        # target class
        # r'' + str(goal_class) + '\n'
    ))

def get_class_number_from_letter(est_y):
    if est_y == 'P':
        return 0
    elif est_y == 'I':
        return 1
    elif est_y == 'S':
        return 2
    elif est_y == 'N':
        return 3
    elif est_y == 'E':
        return 4
    elif est_y == 'T':
        return 5
    elif est_y == 'X':
        return 6
    else:
        return None


def addslashes(string, sub=re.compile(r"[\\\"']").sub):
    """ To add slashes. """
    def fixup(m):
        return "\\" + m.group(0)
    return sub(fixup, string)


def get_spectrograms_figure(t, x, y, z,
                            length_inches=18.0, width_inches=5.0,
                            nfft=8, noverlap=4,
                            save_fig=True, file_name='spect.jpg'):
    """ Returns image in base64 (for Raspberry Pi), if and only if save_fig=True, or figure if rpi=False """
    # t is in milliseconds
    fs = (len(t) / t[-1]) * pow(10, 3) # sampling frequency in Hertz

    fig2, (axX2, axY2, axZ2) = plt.subplots(1, 3)  # ------------------------------------------------------- fig2

    # figure('x spect')
    axX2.specgram(x, NFFT=nfft, Fs=fs, noverlap=noverlap)
    axX2.set_ylabel('X Frequency [Hz]')
    axX2.set_xlabel('Time [sec]')

    # figure('y spect')
    axY2.specgram(y, NFFT=nfft, Fs=fs, noverlap=noverlap)
    axY2.set_ylabel('Y Frequency [Hz]')
    axY2.set_xlabel('Time [sec]')

    # figure('z spect')
    axZ2.specgram(z, NFFT=nfft, Fs=fs, noverlap=noverlap)
    axZ2.set_ylabel('Z Frequency [Hz]')
    axZ2.set_xlabel('Time [sec]')

    fig2.set_size_inches(length_inches, width_inches)

    if save_fig:
        savefig(file_name)

    return fig2


def get_histograms_figure(t, x, y, z,
                          length_inches=18.0, width_inches=5.0,
                          save_fig=True, file_name='histograms.jpg'):
    """ Returns image in base64 (for Raspberry Pi), if and only if save_fig=True, or figure if rpi=False """

    fig1, (axX1, axY1, axZ1) = plt.subplots(1, 3)  # ------------------------------------------------------- fig1

    # number of classes for histograms
    class_n_for_hist = int(1 + 3.32 * log(len(t)))

    # these are matplotlib.patch.Patch properties
    props = dict(boxstyle='round', facecolor='wheat', alpha=0.5)

    # x data
    text_x = '\n'.join((
        r'        x-axis',
        r'$\mu=%.2f$' % (mean(x)),
        r'$\mathrm{median}=%.2f$' % (median(x)),
        r'$\sigma=%.2f$' % (std(x)),
        r'$\mathrm{kurtosis}=%.2f$' % (kurtosis(x),),
        r'$\mathrm{skewness}=%.2f$' % (skew(x))
    ))
    axX1.hist(x, alpha=0.5, bins=class_n_for_hist, color='red')
    # place a text box in upper left in axes coords
    axX1.text(0.05, 0.95, text_x, transform=axX1.transAxes, fontsize=14, verticalalignment='top', bbox=props)

    # y data
    text_y = '\n'.join((
        r'        y-axis',
        r'$\mu=%.2f$' % (mean(y)),
        r'$\mathrm{median}=%.2f$' % (median(y)),
        r'$\sigma=%.2f$' % (std(y)),
        r'$\mathrm{kurtosis}=%.2f$' % (kurtosis(y),),
        r'$\mathrm{skewness}=%.2f$' % (skew(y))
    ))
    axY1.hist(y, alpha=0.5, bins=class_n_for_hist, color='green')
    # place a text box in upper left in axes coords
    axY1.text(0.05, 0.95, text_y, transform=axY1.transAxes, fontsize=14, verticalalignment='top', bbox=props)

    # z data
    text_z = '\n'.join((
        r'        z-axis',
        r'$\mu=%.2f$' % (mean(z)),
        r'$\mathrm{median}=%.2f$' % (median(z)),
        r'$\sigma=%.2f$' % (std(z)),
        r'$\mathrm{kurtosis}=%.2f$' % (kurtosis(z),),
        r'$\mathrm{skewness}=%.2f$' % (skew(z))
    ))
    axZ1.hist(z, alpha=0.5, bins=class_n_for_hist, color='blue')
    # place a text box in upper left in axes coords
    axZ1.text(0.05, 0.95, text_z, transform=axZ1.transAxes, fontsize=14, verticalalignment='top', bbox=props)

    fig1.set_size_inches(length_inches, width_inches)

    if save_fig:
        savefig(file_name)

    return fig1


def get_signal_figure(t, x, y, z, newX, newY, newZ,
                            length_inches=18.0, width_inches=5.0,
                            nfft=8, noverlap=4,
                            save_fig=True, file_name='signal.jpg'):
    """ Returns image in base64 (for Raspberry Pi), if and only if save_fig=True, or figure if rpi=False """
    # t is in milliseconds
    fig0, (ax0) = plt.subplots()  # ------------------------------------------------------- fig0

    plot(t, newX, 'r.-')
    plot(t, newY, 'g.-')
    plot(t, newZ, 'b.-')

    plot(t, x, 'm|-')
    plot(t, y, 'y|-')
    plot(t, z, 'c|-')

    # to label the plotted lines
    legend(['x uniform time', 'y uniform time', 'z uniform time', 'smooth x', 'smooth y', 'smooth z'])

    fig0.set_size_inches(length_inches, width_inches)

    if save_fig:
        savefig(file_name)
    return fig0



