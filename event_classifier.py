import statistics
import numpy as np
import pandas as pd
from sklearn.ensemble import RandomForestClassifier
import joblib
from scipy.io import wavfile

RANDOM_FOREST = joblib.load('new_rf.joblib')

def is_event_change(interval_arr, event_threshold):
    """Check if 

    Args:
        interval_arr (_type_): _description_
        event_threshold (_type_): _description_

    Returns:
        _type_: _description_
    """
    return statistics.stdev(interval_arr.tolist()) > event_threshold

def predict_movement(event_arr):
    
    features_dict = {
        'y__sum_values':sum(event_arr),
        'y__median':statistics.median(event_arr),
        'y__mean':statistics.mean(event_arr),
        'y__standard_deviation':statistics.stdev(event_arr.tolist()),
        'y__variance':statistics.variance(event_arr.tolist()),
        'y__root_mean_square':(statistics.mean(event_arr**2))**(1/2),
        'y__maximum':max(event_arr),
        'y__absolute_maximum':max(abs(event_arr)),
        'y__minimum':min(event_arr)
    }
    
    features = pd.DataFrame(data=features_dict, index=['values'])
    return RANDOM_FOREST.predict(features)

def predict_events(data, prev_sd, is_peak_found, window_size=10000, event_threshold=500):
    """ window_size = SAMPLING_FREQUENCY
    """
    increment = window_size/10
    predicted_labels = []
    predicted_times = []
    lower_interval = 1
    max_time = len(data)

    while (lower_interval + 4000) < max_time:
        upper_interval = int(lower_interval + 10000)
        interval = data[lower_interval:upper_interval]
        print(lower_interval)
        if not is_event_change(interval, event_threshold):
            is_peak_found = False

        elif not is_peak_found and statistics.stdev(interval.tolist()) < prev_sd:
            predicted_sd = predict_movement(interval)
            predicted_labels.append(predicted_sd)
            predicted_times.append(lower_interval/10000)
            print(predicted_sd)
            print(lower_interval/10000)
            is_peak_found = True

        prev_sd = statistics.stdev(interval.tolist())
        lower_interval = int(lower_interval + increment)

    return predicted_labels, prev_sd, is_peak_found # predicted_times

sample_rate, wave_array = wavfile.read('BBB.wav')
# predict_events(wave_array, 0, False)
section = wave_array[47001:57001]
import sys
np.set_printoptions(threshold=sys.maxsize)
print((statistics.mean(section**2))**(1/2))
print(section**2)
for i in range(1, len(section)):
    print(type(section[i]))