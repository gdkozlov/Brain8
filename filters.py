from scipy.signal import butter, lfilter
import numpy as np

FS = 10000

# notch filter?

def butter_filter(data):
    
    # Get the filter coefficients 
    # For digital filters, Wn is normalized from 0 to 1, where 1 is the Nyquist frequency, pi radians/sample.
    b, a = butter(1, [1 / (2 * FS), 100 / (2 * FS)], btype='bandpass', analog=False)
    y = lfilter(b, a, data)
    return y

def chebyshev_filter():
    pass

def gaussian_filter():
    pass