from scipy.signal import iirfilter, lfilter
import numpy as np
import statistics 

### CONSTANTS ###

SAMPLING_FREQUENCY = 10000 # Sampling Frequency in Hz
CUTOFF = [1, 100] # Cutoff Frequencies in Hz

# notch filter?

def running_average(x, N):
    cumsum = np.cumsum(np.insert(x, 0, 0)) 
    return (cumsum[N:] - cumsum[:-N]) / float(N)

def butter_filter(data):
    # data = data - statistics.median(data)
    N = 100
    data = running_average(data, N)
    # For digital filters, Wn is normalized from 0 to 1, where 1 is the Nyquist frequency, pi radians/sample.
    b, a = iirfilter(8, Wn=50, fs=SAMPLING_FREQUENCY, btype='lowpass', ftype='butter', analog=False)
    y = lfilter(b, a, data)
    return y

def chebyshev_filter():
    pass

def gaussian_filter():
    pass