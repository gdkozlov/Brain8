import joblib
from sklearn.ensemble import RandomForestClassifier
from sklearn.model_selection import train_test_split
import pandas as pd
import numpy as np

data = pd.read_csv('new3.csv', header = None)
train_labels = ['B']*17 + ['L']*17 + ['R']*16
# split the data into training and testing sets

train_data, test_data, train_labels, test_labels = train_test_split(data, train_labels, test_size=0.2)

rf = RandomForestClassifier(n_estimators=100, max_depth=5, random_state=42)
rf.fit(train_data, train_labels)

# predict on the test data

predictions = rf.predict(test_data)

# evaluate the model performance
accuracy = rf.score(test_data, test_labels)
print(f"Accuracy: {accuracy}")

print(test_data)
print(test_labels)
print(predictions)