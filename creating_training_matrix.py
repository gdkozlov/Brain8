import pandas as pd
import os
import numpy as np
from tsfresh.feature_extraction import extract_features, EfficientFCParameters
from tsfresh.utilities.dataframe_functions import impute
from tsfresh import select_features
import math
import statistics as st

# HI GLEB
#you basically just need to change glebdata to whatever directory you're using... as long as that directory contains multiple folders taht each contain multiple eye movements

if __name__ == '__main__':
    def flatten(l):
        flat_list = []
        for i in l:
            for j in i:
                flat_list.append(j)
        return flat_list


    waves = []
    def add_to_waves_list(folder, file):
        with open(f"glebdata/{folder}/{file}") as f:
            datas = f.readlines()
        for i in range(0, len(datas)):
            datas[i] = float(datas[i])
        waves.append(datas)
    # for folder in range(0, len(os.listdir("TerryData"))):
    #     for file in range(0, 3):
    #         if file == 1:
    #             lefts.append()

    for folder in os.listdir('glebdata'):
        for file in os.listdir(f'glebdata/{folder}'):
            add_to_waves_list(folder, file)
    flat_waves = flatten(waves)

    time = []
    for i in waves:
        time.append(list(range(0, len(i))))
    flat_time = flatten(time)

    id_col = []
    for i in range(0, len(waves)):
        id_col.append([str(i)]*len(waves[i]))
    flat_id = flatten(id_col)

    #minimal features
    sum_values = []
    median_values = []
    mean_values = []
    sd_values = []
    var_values = []
    rms_values = []
    max_values = []
    abs_max_values = []
    min_values = []
    for i in waves:
        sum_values.append(sum(i))
        median_values.append(st.median(i))
        mean_values.append(st.mean(i))
        sd_values.append(st.stdev(i))
        var_values.append(st.variance(i))
        squared_list = [j**2 for j in i]
        rms_values.append((st.mean(squared_list))**(1/2))
        max_values.append(max(i))
        absolute_list = [abs(j) for j in i]
        abs_max_values.append(max(absolute_list))
        min_values.append(min(i))

    feature_dict = {'y__sum_values':sum_values,
         'y__median':median_values,
         'y__mean':mean_values,
         'y__standard_deviation':sd_values,
         'y__variance':var_values,
         'y__root_mean_square':rms_values,
         'y__maximum':max_values,
         'y__absolute_maximum':abs_max_values,
         'y__minimum':min_values}
    
    index_values = list(range(0, 50))

    features = pd.DataFrame(data=feature_dict, index=index_values)
    #rename the csv to whatever you want
    features.to_csv('new3.csv', index=False, header=False)





    # df = pd.DataFrame({'id': flat_id, 'ds': flat_time, 'y': flat_waves})
    # labels = ['B']*17 + ['L']*17 + ['R']*16
    # labels = pd.Series(labels)

    # df['id'] = df['id'].astype('object')
    # df['ds'] = df['ds'].astype('object')
    # df['y'] = df['y'].astype('object')

    # feat_dict = EfficientFCParameters()
    # del feat_dict['binned_entropy'], feat_dict['change_quantiles'], feat_dict['friedrich_coefficients'], feat_dict['max_langevin_fixed_point'], feat_dict['linear_trend'], feat_dict['fourier_entropy']
    # features = extract_features(df, column_id='id', column_sort='ds', default_fc_parameters = feat_dict)

    # # save the feature values
    # features = features.drop(features.columns[699], axis = 1)
    # impute(features)
    # features_filtered = select_features(features, labels)

    # features.to_csv('new4.csv', index = False, header = False)
