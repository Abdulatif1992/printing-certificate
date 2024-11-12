import os
import pandas as pd
import joblib
import numpy as np
import csv

def calculate(row):
    level = str(row['受験番号'])[9]
    model = joblib.load('data/models/'+level+'Q_RandomForestCBT.pkl')
    scaler = joblib.load('data/models/'+level+'Q_scalerCBT.pkl')
    level = int(level)
    result = 2

    row1 = 0
    row2 = 0
    row3 = 0

    match level:
        case 1:
            soten1, soten2,soten3 = calculate1Q(row)
            result = predict(model, scaler, row['anchor'], soten1, soten2, soten3)
            row1, row2, row3 = soten1, soten2, soten3
        case 2:
            soten1, soten2,soten3 = calculate2Q(row)
            result = predict(model, scaler, row['anchor'], soten1, soten2, soten3)
            row1, row2, row3 = soten1, soten2, soten3
        case 3:
            soten1, soten2,soten3 = calculate3Q(row)
            result = predict(model, scaler, row['anchor'], soten1, soten2, soten3)
            row1, row2, row3 = soten1, soten2, soten3
        case 4:
            soten12, soten3 = calculate4Q(row)
            result = predict(model, scaler, row['anchor'], soten12, soten3)
            row1,  row3 = soten12,  soten3
        case 5:
            soten12, soten3 = calculate5Q(row)
            result = predict(model, scaler, row['anchor'], soten12, soten3)
            row1,  row3 = soten12,  soten3
    return result, row1, row2, row3
            

def calculate1Q(row):
    section1Soten = (
        int(row['correct_q1'].split()[0]) *4/40*60/6 +
        int(row['correct_q2'].split()[0]) *5/40*60/7 +
        int(row['correct_q3'].split()[0]) *6/40*60/6 +
        int(row['correct_q4'].split()[0]) *6.5/40*60/6 +
        int(row['correct_q5'].split()[0]) *5.5/40*60/10 +
        int(row['correct_q6'].split()[0]) *6/40*60/5 +
        int(row['correct_q7'].split()[0]) *7/40*60/5
    )
    section2Soten = (
        int(row['correct_q8'].split()[0]) *10/70*60/4 +
        int(row['correct_q9'].split()[0]) *18/70*60/9 +
        int(row['correct_q10'].split()[0]) *12/70*60/4 +
        int(row['correct_q11'].split()[0]) *11/70*60/3 +
        int(row['correct_q12'].split()[0]) *12/70*60/4 +
        int(row['correct_q13'].split()[0]) *7/70*60/2
    )
    section3Soten = (
        int(row['correct_q14'].split()[0]) *11/55*60/5 +
        int(row['correct_q15'].split()[0]) *12/55*60/6 +
        int(row['correct_q16'].split()[0]) *12/55*60/5 +
        int(row['correct_q17'].split()[0]) *8.5/55*60/11 +
        int(row['correct_q18'].split()[0]) *11.5/55*60/4
    )
    return section1Soten, section2Soten, section3Soten

def calculate2Q(row):
    section1Soten = (
        int(row['correct_q1'].split()[0]) *3.5/45*60/5 +
        int(row['correct_q2'].split()[0]) *3.5/45*60/5 +
        int(row['correct_q3'].split()[0]) *4/45*60/5 +
        int(row['correct_q4'].split()[0]) *5/45*60/7 +
        int(row['correct_q5'].split()[0]) *5/45*60/5 +
        int(row['correct_q6'].split()[0]) *6/45*60/5 +
        int(row['correct_q7'].split()[0]) *7/45*60/12 +
        int(row['correct_q8'].split()[0]) *5/45*60/5 +
        int(row['correct_q9'].split()[0]) *6/45*60/5
    )
    section2Soten = (
        int(row['correct_q10'].split()[0]) *13/60*60/5 +
        int(row['correct_q11'].split()[0]) *18/60*60/9 +
        int(row['correct_q12'].split()[0]) *10.5/60*60/2 +
        int(row['correct_q13'].split()[0]) *12/60*60/3 +
        int(row['correct_q14'].split()[0]) *6.5/60*60/2
    )
    section3Soten = (
        int(row['correct_q15'].split()[0]) *10/50*60/5 +
        int(row['correct_q16'].split()[0]) *11.5/50*60/6 +
        int(row['correct_q17'].split()[0]) *10/50*60/5 +
        int(row['correct_q18'].split()[0]) *9.5/50*60/12 +
        int(row['correct_q19'].split()[0]) *9/50*60/4
    )
    return section1Soten, section2Soten, section3Soten

def calculate3Q(row):
    section1Total = (
        int(row['correct_q1'].split()[0]) / 8 * 5.5 / 55 * 60 +
        int(row['correct_q2'].split()[0]) / 6 * 4 / 55 * 60 +
        int(row['correct_q3'].split()[0]) / 11 * 7.5 / 55 * 60 +
        int(row['correct_q4'].split()[0]) / 5 * 7.5 / 55 * 60 +
        int(row['correct_q5'].split()[0]) / 5 * 7.5 / 55 * 60 +
        int(row['correct_q6'].split()[0]) / 13 * 8.5 / 55 * 60 +
        int(row['correct_q7'].split()[0]) / 5 * 6 / 55 * 60 +
        int(row['correct_q8'].split()[0]) / 5 * 8.5 / 55 * 60
    )
    section2Total = (
        int(row['correct_q9'].split()[0]) / 4 * 12 / 45 * 60 +
        int(row['correct_q10'].split()[0]) / 6 * 13 / 45 * 60 +
        int(row['correct_q11'].split()[0]) / 4 * 12 / 45 * 60 +
        int(row['correct_q12'].split()[0]) / 2 * 8 /  45 * 60
    )
    
    section3Total = (
        int(row['correct_q13'].split()[0]) / 6 * 11 / 40 * 60 +
        int(row['correct_q14'].split()[0]) / 6 * 11 / 40 * 60 +
        int(row['correct_q15'].split()[0]) / 3 * 6 / 40 * 60 +
        int(row['correct_q16'].split()[0]) / 4 * 5.3 / 40 * 60 +
        int(row['correct_q17'].split()[0]) / 9 * 6.7 / 40 * 60
    )

    return section1Total, section2Total, section3Total

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

    return section1And2Total, section3Total

def calculate5Q(row):
    section1And2Total = (
        int(row['correct_q1'].split()[0]) / 7 * 5.5 / 60 * 120 +
        int(row['correct_q2'].split()[0]) / 5 * 4.5 / 60 * 120 +
        int(row['correct_q3'].split()[0]) / 6 * 5 / 60 * 120 +
        int(row['correct_q4'].split()[0]) / 3 * 5 / 60 * 120 +
        int(row['correct_q5'].split()[0]) / 9 * 8 / 60 * 120 +
        int(row['correct_q6'].split()[0]) / 4 * 5.5 / 60 * 120 +
        int(row['correct_q7'].split()[0]) / 4 * 7 / 60 * 120 +
        int(row['correct_q8'].split()[0]) / 2 * 6 / 60 * 120 +
        int(row['correct_q9'].split()[0]) / 2 * 8 / 60 * 120 +
        int(row['correct_q10'].split()[0]) / 1 * 5.5 / 60 * 120
    )

    section3Total = (
        int(row['correct_q11'].split()[0]) / 7 * 9 / 30 * 60 +
        int(row['correct_q12'].split()[0]) / 6 * 9 / 30 * 60 +
        int(row['correct_q13'].split()[0]) / 5 * 6 / 30 * 60 +
        int(row['correct_q13'].split()[0]) / 6 * 6 / 30 * 60
    )

    return section1And2Total, section3Total

def predict(model, scaler, anchor, soten1, soten2, soten3=999):
    if(soten3 == 999):
        # 4Q or 5Q       
        new_data = pd.DataFrame([[soten1, soten2, soten1+soten2, anchor]], columns=['S12', 'S3', 'Total', 'Anchor'])
    else :
        # 1Q, 2Q or 3Q
        new_data = pd.DataFrame([[soten1, soten2, soten3, soten1+soten2+soten3, anchor]], columns=['S1', 'S2', 'S3', 'Total', 'Anchor']) 
        
    # Scale the new data using the loaded scaler
    scaled_data = scaler.transform(new_data)

    # Make prediction
    prediction = model.predict(scaled_data)
    return prediction[0]

# Define the folder name to add to the path
folder_name = "data"
# Specify the file name
file_name = 'grade_list.csv'

# Since the script is in the 'app' folder, use '..' to move up one directory
file_path = os.path.join(folder_name, file_name)

if os.path.exists(file_path):    
    Data = pd.read_csv(file_path, encoding='shift_jis', low_memory=False)
    
    # Open the CSV file for writing
    with open("outputfile.csv", mode="w", newline="") as fw:
        # Initialize CSV writer
        writer = csv.writer(fw)

        # Write the header row (adjust as needed)
        writer.writerow(["number", "S1", "S2", "S3", "Total", "Anchor", "Pass", "level", "tokuten1", "tokuten2", "tokuten3"])
    
        # Iterate over the rows in your DataFrame

        for index, row in Data.iterrows():
            # print(f"{row.iloc[0]}")    
            result, soten1, soten2, soten3 = calculate(row)
            total = soten1+soten2+soten3
            level = int(str(row.iloc[0])[9])
            tokuten1, tokuten2, tokuten3 = 0,0,0
            
            if(level == 1 or level == 2):
                tokuten1, tokuten2, tokuten3 = soten1, soten2, soten3
            elif(level == 3):
                tokuten1, tokuten2, tokuten3 = soten1*0.896, soten2*0.896, soten3*0.896
            elif(level == 4):
                tokuten1, tokuten3 =  soten1*0.796, soten3*0.796
            elif(level == 5):
                tokuten1, tokuten3 =  soten1*0.7, soten3*0.7   
            
            # Write the row to the CSV file
            writer.writerow([row.iloc[0],  soten1, soten2, soten3, row['anchor'], result, level,  tokuten1, tokuten2, tokuten3])
       
    print("Data saved to outputfile.csv")

else:
    print("file yo'q")    