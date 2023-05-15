import librosa
import numpy as np
import pandas as pd
from sklearn.ensemble import RandomForestClassifier
from sklearn.model_selection import StratifiedKFold

def extract_features(audio_data, sample_rate):
    # Extract features from the audio data
    features = []

    # Compute autocorrelation of the audio data
    autocorr = np.correlate(audio_data, audio_data, mode='full')

    # Calculate features based on autocorrelation
    features.append(autocorr[0])  # x_acf1
    features.append(autocorr[10])  # x_acf10

    # Calculate first-order differences of the autocorrelation
    diff1_autocorr = np.diff(autocorr)
    features.append(diff1_autocorr[0])  # diff1_acf1
    features.append(diff1_autocorr[10])  # diff1_acf10

    # Calculate second-order differences of the autocorrelation
    diff2_autocorr = np.diff(diff1_autocorr)
    features.append(diff2_autocorr[0])  # diff2_acf1
    features.append(diff2_autocorr[10])  # diff2_acf10

    # Calculate entropy of the audio data using spectral entropy
    fft = np.fft.fft(audio_data)
    power_spectrum = np.abs(fft) ** 2
    normalized_power_spectrum = power_spectrum / np.sum(power_spectrum)
    spectral_entropy = -np.sum(normalized_power_spectrum * np.log2(normalized_power_spectrum))
    features.append(spectral_entropy)  # entropy

    # Calculate lumpiness of the audio data
    lumpiness = np.sum(np.abs(np.diff(audio_data)))
    features.append(lumpiness)  # lumpiness

    # Calculate the number of flat spots in the audio data
    flat_spots = np.sum(np.diff(np.sign(np.diff(audio_data))) == 0)
    features.append(flat_spots)  # flat_spots

    # Calculate the number of zero crossings in the audio data
    zero_crossings = np.sum(np.diff(np.sign(audio_data)) != 0)
    features.append(zero_crossings)  # crossing_points

    # Add more feature calculations here based on the provided columns
    features.append(np.max(autocorr))  # max_kl_shift
    features.append(np.argmax(autocorr) / sample_rate)  # time_kl_shift
    features.append(np.mean(audio_data))  # mean
    features.append(np.var(audio_data))  # var
    features.append(np.max(np.abs(np.diff(audio_data))))  # max_level_shift
    features.append(np.argmax(np.abs(np.diff(audio_data))) / sample_rate)  # time_level_shift
    features.append(np.max(np.abs(np.diff(audio_data))) / np.var(audio_data))  # max_var_shift
    features.append(np.argmax(np.abs(np.diff(audio_data))) / sample_rate)  # time_var_shift

    return features


# Set the random seed
np.random.seed(3888)
# Load the data from CSV files
X = pd.read_csv("features.csv").values
y = pd.read_csv("labels.csv").values.flatten()

cvK = 8  # number of CV folds
cv_50acc5_rf = []
cv_acc5 = []

for i in range(50):
    skf = StratifiedKFold(n_splits=cvK, shuffle=True)
    cv_acc = np.zeros(cvK)
    
    for j, (train_index, test_index) in enumerate(skf.split(X, y)):
        X_train, X_test = X[train_index], X[test_index]
        y_train, y_test = y[train_index], y[test_index]
        
        # Fit random forest classifier and predict on test data
        rf_fit = RandomForestClassifier(n_estimators=500, max_depth=10)
        rf_fit.fit(X_train, y_train)
        rf_pred = rf_fit.predict(X_test)
        
        # Calculate accuracy
        cv_acc[j] = np.mean(rf_pred == y_test)
    
    cv_50acc5_rf.append(np.mean(cv_acc))

# Print the mean accuracy
print(np.mean(cv_50acc5_rf))


# Create a function to process a sliding window of data
def process_sliding_window(window_data):
    # Perform any necessary data processing on the window_data
    
    # Pass the processed data to extract_features
    features = extract_features(window_data, 100)
    
    # Make predictions using the extracted features
    predictions = rf_fit.predict(np.reshape(features, (1, -1)))
    
    return predictions