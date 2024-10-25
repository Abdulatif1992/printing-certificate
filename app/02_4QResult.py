# Import necessary libraries
import pandas as pd
import os

# Define the folder name to add to the path
folder_name = "data"
# Specify the file name
file_name = '3Q_DB_United.csv'

# Define the path to the file
# Since the script is in the 'app' folder, use '..' to move up one directory
file_path = os.path.join(folder_name, file_name)



def tokutenAndPassed(S1, S2, S3, Total, Anchor):
    tokuten12 = 0
    tokuten3 = 0
    tokuten = 0
    passed = 9

    if( (S1+S2) >=113 ):
        tokuten12 = round(tokutenUpper(S1+S2))
    else:
        tokuten12 = round(tokutenLower(S1+S2))
    tokuten3 = round(tokutenLower(S3))

    # mana shu joydan hisoblash boshlandi

    if( tokuten12 < 38 or tokuten3 < 19 ):
        tokuten = tokuten12 + tokuten3
        passed = 0        
    else:
        tokuten = round(Tokuten(Total))

        if( Total >= 113 ):
            passed = 1
            tokuten12 = round( tokuten * (S1+S2) / Total )
            tokuten3 = round( tokuten * S3 / Total )
        elif( Total < 86 ):
            passed = 0
            tokuten12 = round(S1+S2)
            tokuten3 = round(S3)
        else:
            if( Anchor >= 50 ):
                tokuten = 90
                passed = 1
            else:
                tokuten = 89
                passed = 0
            tokuten12 = round( tokuten * (S1+S2) / Total )
            tokuten3 = round( tokuten * S3 / Total )       

    gosa = tokuten - tokuten12 - tokuten3
    if( gosa > 0.9 ):
        if( tokuten12 != 120 ):
            tokuten12 += 1
        else:
            tokuten3 += 1
    elif( gosa < -0.9 ):
        if( tokuten12 != 0 ):
            tokuten12 -= 1
        else:
            tokuten3 -= 1                         
    # tokuten = round(subTokuten(Total))    
    
    return tokuten12, tokuten3, tokuten, passed 

def Tokuten(soten):
    if(soten >= 113):
        return tokutenUpper(soten)
    elif(soten < 113 and soten >= 86):
        return 90
    else:
        return soten

def tokutenLower(soten):
    return soten * 90/113

def tokutenUpper(soten):
    return 180 - (90/67) * (180-soten)

# Check if the file exists
if os.path.exists(file_path):
    # Load your data
    data = pd.read_csv(file_path, encoding='unicode_escape', low_memory=False)

    # Ensure the correct types for columns
    data['S1'] = data['S1'].astype(float)
    data['S2'] = data['S2'].astype(float)
    data['S3'] = data['S3'].astype(float)
    data['Total'] = data['Total'].astype(float)
    data['Anchor'] = data['Anchor'].astype(float)


    # Define features and target variable
    X = data[['number','S1',  'S2',  'S3',  'Total', 'Anchor', 'Pass']]

    
    X[['tokuten12', 'tokuten3', 'tokuten', 'Passed']] = X.apply(lambda row: pd.Series(tokutenAndPassed(row['S1'], row['S2'], row['S3'], row['Total'], row['Anchor'],)), axis=1)
    
    # Export part1 and part2 as new CSV files
    print(X)
    X.to_csv('data/4Q_Result.csv', index=False)

else:
    print('there is no file')