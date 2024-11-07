import os
import pandas as pd
import joblib
import numpy as np

def calculate(row):
     level = str(row['受験番号'])[9]
     level = int(level)
     match level:
        case 1:
            calculate1Q(row)
        case 2:
            calculate2Q(row)
        case 3:
            calculate3Q(row)
        case 4:
            calculate4Q(row)
        case 5:
            calculate5Q(row)

def calculate1Q(row):
    print('')

def calculate2Q(row):
    print('') 

def calculate3Q(row):
    print('') 

def calculate4Q(row):
    section1And2Total = (
        int(row['correct_q1'].split()[0]) / 7 * 5.25 / 80 * 120 +
        int(row['correct_q2'].split()[0]) / 5 * 3.75 / 80 * 120 +
        int(row['correct_q3'].split()[0]) / 8 * 6 / 80 * 120 +
        int(row['correct_q4'].split()[0]) / 4 * 5 / 80 * 120 +
        int(row['correct_q5'].split()[0]) / 4 * 5 / 80 * 120 +
        int(row['correct_q6'].split()[0]) / 13 * 13.5 / 80 * 120 +
        int(row['correct_q7'].split()[0]) / 4 * 5.5 / 80 * 120 +
        int(row['correct_q8'].split()[0]) / 4 * 8 / 80 * 120 +
        int(row['correct_q9'].split()[0]) / 3 * 10.5 / 80 * 120 +
        int(row['correct_q10'].split()[0]) / 3 * 11.5 / 80 * 120 +
        int(row['correct_q11'].split()[0]) / 2 * 6 / 80 * 120
    )
    section3Total = (
        int(row['correct_q12'].split()[0]) / 8 * 10.5 / 35 * 60 +
        int(row['correct_q13'].split()[0]) / 7 * 10.5 / 35 * 60 +
        int(row['correct_q14'].split()[0]) / 5 * 6.5 / 35 * 60 +
        int(row['correct_q15'].split()[0]) / 8 * 7.5 / 35 * 60
    )

    predict4Q(section1And2Total, section3Total)

def calculate5Q(row):
    section1And2Total = (
        row['correct_q1'] / 7 * 5.5 / 60 * 120 +
        row['correct_q2'] / 5 * 4.5 / 60 * 120 +
        row['correct_q3'] / 6 * 5 / 60 * 120 +
        row['correct_q4'] / 3 * 5 / 60 * 120 +
        row['correct_q5'] / 9 * 8 / 60 * 120 +
        row['correct_q6'] / 4 * 5.5 / 60 * 120 +
        row['correct_q7'] / 4 * 7 / 60 * 120 +
        row['correct_q8'] / 2 * 6 / 60 * 120 +
        row['correct_q9'] / 2 * 8 / 60 * 120 +
        row['correct_q10'] / 1 * 5.5 / 60 * 120
    )

    section3Total = (
        row['correct_q11'] / 7 * 9 / 30 * 60 +
        row['correct_q12'] / 6 * 9 / 30 * 60 +
        row['correct_q13'] / 5 * 6 / 30 * 60 +
        row['correct_q14'] / 6 * 6 / 30 * 60
    )

def predict1Q():
    print("")

def predict2Q():
    print("")

def predict3Q():
    print("")

def predict4Q(soten12, soten3):
    # Load the model and the scaler from the file

    model = joblib.load('data/models/4Q_RandomForestCBT.pkl')
    scaler = joblib.load('data/models/4Q_scalerCBT.pkl')
    # Sample new data
    new_data = np.array([[soten12, soten3, soten12+soten3, 60]])

    # Scale the new data using the loaded scaler
    scaled_data = scaler.transform(new_data)

    # Make prediction
    prediction = model.predict(scaled_data)
    print(prediction[0])

def predict5Q(soten12, soten3):
    # Load the model and the scaler from the file

    model = joblib.load('data/models/5Q_RandomForestCBT.pkl')
    scaler = joblib.load('data/models/5Q_scalerCBT.pkl')
    # Sample new data
    new_data = np.array([[soten12, soten3, soten12+soten3, 60]])

    # Scale the new data using the loaded scaler
    scaled_data = scaler.transform(new_data)

    # Make prediction
    prediction = model.predict(scaled_data)
    print(prediction[0])

# Define the folder name to add to the path
folder_name = "data"
# Specify the file name
file_name = 'grade_list.csv'

# Define the path to the file
# Since the script is in the 'app' folder, use '..' to move up one directory
file_path = os.path.join(folder_name, file_name)


if os.path.exists(file_path):
    
    Data = pd.read_csv(file_path, encoding='shift_jis', low_memory=False)
    for index, row in Data.iterrows():
            print(f"{row.iloc[0]}")    

            # Create the PDF
            calculate(row)


else:
    print("file yo'q")    