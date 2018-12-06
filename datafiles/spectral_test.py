import matplotlib.pyplot as plt
from pylab import savefig
import numpy as np
from numpy import abs, linspace, argmax, argsort
import process_data_AAIB2018 as my_pd
import novainstrumentation as ni

t, x, y, z = my_pd.get_values_from_csv('pn1.csv', path='..\database_final\\')
t, x, y, z = my_pd.remove_duplicates(t, x, y, z)
t, x, y, z = my_pd.uniform_time(t, x, y, z)
x, y, z = my_pd.smooth_signal(x, y, z)

# t is in milliseconds
n = len(t)  # length of the signal
Fs = (n / t[-1]) * pow(10, 3)
Ts = 1.0/Fs  # sampling interval

print("Fs = " + str(Fs))
print("Ts = " + str(Ts))

print("x fundamental freq: ")
fs = abs(np.fft.fft(x))
f = linspace(0, Fs/2, len(x)/2)
fig, ax = plt.subplots(1, 1)
max_f = f[argmax(fs)]
print(max_f)
if max_f == 0:
    order_coef = argsort(fs)
    max_f = f[order_coef[1]]
    print(max_f)


print("y fundamental freq: ")
fs = abs(np.fft.fft(y))
f = linspace(0, Fs/2, len(x)/2)
fig, ax = plt.subplots(1, 1)
max_f = f[argmax(fs)]
print(max_f)
if max_f == 0:
    order_coef = argsort(fs)
    max_f = f[order_coef[1]]
    print(max_f)

print("z fundamental freq: ")
fs = abs(np.fft.fft(z))
f = linspace(0, Fs/2, len(x)/2)
fig, ax = plt.subplots(1, 1)
max_f = f[argmax(fs)]
print(max_f)
if max_f == 0:
    order_coef = argsort(fs)
    max_f = f[order_coef[1]]
    print(max_f)


'''
k = np.arange(n)
T = n/Fs
frq = k/T  # two sides frequency range
frq = frq[range(int(n/2))]  # one side frequency range

X = np.fft.fft(x)/n # fft computing and normalization
X = X[range(int(n/2))]

fig, ax = plt.subplots(2, 1)
ax[0].plot(t, x)
ax[0].set_xlabel('Time')
ax[0].set_ylabel('Amplitude')
ax[1].plot(frq, abs(X), 'r')  # plotting the spectrum
ax[1].set_xlabel('Freq (Hz)')
ax[1].set_ylabel('|X(freq)|')

savefig('FFTs_x.jpg')

Y = np.fft.fft(y)/n # fft computing and normalization
Y = Y[range(int(n/2))]

fig, ax = plt.subplots(2, 1)
ax[0].plot(t, y)
ax[0].set_xlabel('Time')
ax[0].set_ylabel('Amplitude')
ax[1].plot(frq, abs(Y), 'r')  # plotting the spectrum
ax[1].set_xlabel('Freq (Hz)')
ax[1].set_ylabel('|Y(freq)|')

savefig('FFTs_y.jpg')

Z = np.fft.fft(z)/n # fft computing and normalization
Z = Z[range(int(n/2))]

fig, ax = plt.subplots(2, 1)
ax[0].plot(t, z)
ax[0].set_xlabel('Time')
ax[0].set_ylabel('Amplitude')
ax[1].plot(frq, abs(Z), 'r')  # plotting the spectrum
ax[1].set_xlabel('Freq (Hz)')
ax[1].set_ylabel('|Z(freq)|')

savefig('FFTs_z.jpg')


# spectral domain auxiliary functions to get spectral features from X data
x_fft = np.fft.fft(x)
x_freqs = np.fft.fftfreq(len(x_fft))
x_peak_freq_index = np.argmax(np.abs(x_fft))
# spectral domain auxiliary functions to get spectral features from Y data
y_fft = np.fft.fft(y)
y_freqs = np.fft.fftfreq(len(y_fft))
y_peak_freq_index = np.argmax(np.abs(y_fft))
# spectral domain auxiliary functions to get spectral features from Z data
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
y_peak_freq = y_freqs[y_peak_freq_index]  # not in Hertz
# spectral features from Z data
z_min_freq = z_freqs.min()
z_max_freq = z_freqs.max()
z_peak_freq = z_freqs[z_peak_freq_index]  # not in Hertz
'''
