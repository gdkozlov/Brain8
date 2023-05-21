from scipy.signal import iirfilter, lfilter
import numpy as np
import statistics 

### CONSTANTS ###

SAMPLING_FREQUENCY = 10000 # Sampling Frequency in Hz
LOWPASS_CUTOFF = 50 # Cutoff Frequencies in Hz
HIGHPASS_CUTOFF = 100
WINDOW_SIZE = 1000

# notch filter?

def running_average(x, N):
    cumsum = np.cumsum(np.insert(x, 0, 0)) 
    return (cumsum[N:] - cumsum[:-N]) / float(N)

def butter_filter_lowpass(data):

    # For digital filters, Wn is normalized from 0 to 1, where 1 is the Nyquist frequency, pi radians/sample.
    b, a = iirfilter(8, Wn=LOWPASS_CUTOFF, fs=SAMPLING_FREQUENCY, btype='lowpass', ftype='butter', analog=False)
    y = lfilter(b, a, data)
    return y

def butter_filter_highpass(data):
    # For digital filters, Wn is normalized from 0 to 1, where 1 is the Nyquist frequency, pi radians/sample.
    b, a = iirfilter(8, Wn=HIGHPASS_CUTOFF, fs=SAMPLING_FREQUENCY, btype='highpass', ftype='butter', analog=False)
    y = lfilter(b, a, data)
    return y

def butter_filter(data):
    data = data - statistics.median(data)
    return butter_filter_lowpass(running_average(data, WINDOW_SIZE))

def chebyshev_filter():
    pass

def gaussian_filter():
    pass