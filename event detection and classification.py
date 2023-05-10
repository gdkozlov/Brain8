import pandas
import statistics
from sklearn.ensemble import RandomForestClassifier
from tsfeatures import tsfeatures
from scipy.io import wavfile
import numpy
import joblib
from tsfresh.feature_extraction import extract_features, MinimalFCParameters

def event_sd (Y, thresholdEvents):
    testStat = statistics.stdev(Y.tolist())
    if testStat > thresholdEvents:
        return 'T'
    else:
        return 'F'

rf = joblib.load('tsfresh_rf.joblib')
def predict (wave):
    # wave_list = wave.tolist()  

    # time_range = range(0, len(wave_list))
    # time = list(time_range)

    # df = pandas.DataFrame({'id': 1, 'ds': time, 'y': wave_list})

    # df['id'] = df['id'].astype('object')
    # df['ds'] = df['ds'].astype('object')
    # df['y'] = df['y'].astype('object')

    # # extract features
    # features = extract_features(df, column_id='id', column_sort='ds', default_fc_parameters=MinimalFCParameters())
    
    dict = {'y__sum_values':sum(wave),
             'y__median':statistics.median(wave),
             'y__mean':statistics.mean(wave),
             'y__standard_deviation':statistics.stdev(wave.tolist()),
             'y__variance':statistics.variance(wave.tolist()),
             'y__root_mean_square':(statistics.mean(wave**2))**(1/2),
             'y__maximum':max(wave),
             'y__absolute_maximum':max(abs(wave)),
             'y__minimum':min(wave)}

    # y__sum_values = sum(wave)
    # y__median = statistics.median(wave)
    # y__mean = statistics.mean(wave)
    # y__standard_deviation = statistics.stdev(wave.tolist())
    # y__variance = statistics.variance(wave.tolist())
    # y__root_mean_square = (statistics.mean(wave**2))**(1/2)
    # y__maximum = max(wave)
    # y__absolute_maximum = max(abs(wave))
    # y__minimum = min(wave)
    
    features = pandas.DataFrame(data = dict, index = ['values'])
    return rf.predict(features)

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
            
if __name__ == '__main__':
    sample_rate, wave_array = wavfile.read('Brain8-main/gleb/BBR.wav')
    predict_sd(wave_array, sample_rate, 500)