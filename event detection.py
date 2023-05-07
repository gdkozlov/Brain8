import pandas
import statistics
from sklearn.ensemble import RandomForestClassifier
from tsfeatures import tsfeatures
from scipy.io import wavfile
import numpy

def event_sd (Y, thresholdEvents):
    testStat = statistics.stdev(Y.tolist())
    if testStat > thresholdEvents:
        return 'T'
    else:
        return 'F'

def predict (wave):
#   features <- tsfeatures(wave,
#                features = ["acf_features","entropy","lumpiness",
#                  "flat_spots","crossing_points"])
#   test = features  
  return 'lol'
  #return str(sklearn.ensemble.RandomForestClassifier(train = X, test = test, cl = y, k = 3))

def predict_sd (wave_array, sample_rate, events):
    window_size = sample_rate
    increment = window_size/10
    Y = wave_array
    predicted_labels = []
    predicted_times = []
    lower_interval = 1
    max_time = len(wave_array)
    last_sd = 0
    in_movement = 'F'
    past_peak = 'F'

    while max_time > (lower_interval + 10000):
        upper_interval = int(lower_interval + 10000)
        interval = Y[lower_interval:upper_interval]
        in_movement = event_sd(interval, events)
        if in_movement == 'T':
            if statistics.stdev(interval.tolist()) < last_sd and past_peak == 'F':
                predicted_sd = predict(interval)
                predicted_labels.append(predicted_sd)
                predicted_times.append(lower_interval/10000)
                print(predicted_sd)
                print(lower_interval/10000)
                past_peak = 'T'
        else:
            past_peak = 'F'
        last_sd = statistics.stdev(interval.tolist())
        lower_interval = int(lower_interval + increment)

    return predicted_labels, predicted_times
            
sample_rate, wave_array = wavfile.read('Brain8-main/gleb/BBB.wav')
predict_sd(wave_array, sample_rate, 500)
