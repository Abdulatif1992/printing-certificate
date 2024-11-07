import joblib
import numpy as np
import os

# Define the folder name to add to the path
folder_name = "data/models"

# Construct the new path
new_path = os.path.join(os.getcwd(), folder_name)

# Change the current working directory to the new path
os.chdir(new_path)

# Load the model and the scaler from the file
model = joblib.load('5Q_RandomForestCBT.pkl')
scaler = joblib.load('5Q_scalerCBT.pkl')

# Sample new data
new_data = np.array([[60, 29, 89, 51]])

# Scale the new data using the loaded scaler
scaled_data = scaler.transform(new_data)

# Make prediction
prediction = model.predict(scaled_data)

print(f'Prediction: {prediction[0]}')  # Output will be 0 or 1