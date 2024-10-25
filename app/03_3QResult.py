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
    tokuten1 = 0
    tokuten2 = 0
    tokuten3 = 0
    tokuten = 0
    passed = 9

    
    tokuten1 = round(tokutenLower(S1))
    tokuten2 = round(tokutenLower(S2))
    tokuten3 = round(tokutenLower(S3))

    # mana shu joydan hisoblash boshlandi

    if( tokuten1 < 19 or tokuten2 < 19 or tokuten3 < 19 ):
        tokuten = tokuten1 + tokuten2 + tokuten3
        passed = 0        
    else:
        tokuten = round(Tokuten(Total))

        if( Total >= 106 ):
            passed = 1
            tokuten1 = round( tokuten * S1 / Total )
            tokuten2 = round( tokuten * S2 / Total )
            tokuten3 = round( tokuten * S3 / Total )
        elif( Total < 85 ):
            passed = 0
            tokuten1 = round(S1)
            tokuten2 = round(S2)
            tokuten3 = round(S3)
        else:
            if( Anchor >= 50 ):
                tokuten = 95
                passed = 1
            else:
                tokuten = 94
                passed = 0
            tokuten1 = round( tokuten * S1 / Total )
            tokuten2 = round( tokuten * S2 / Total )
            tokuten3 = round( tokuten * S3 / Total )       

    gosa = tokuten - tokuten1 - tokuten2 - tokuten3
    if( gosa > 0.9 ):
        if( tokuten1 != 60 ):
            tokuten1 += 1
        elif( tokuten2 != 60 ):
            tokuten2 += 1
        else:
            tokuten3 += 1
    elif( gosa < -0.9 ):
        if( tokuten1 != 0 ):
            tokuten1 -= 1
        elif( tokuten2 != 0 ):
            tokuten2 -= 1    
        else:
            tokuten3 -= 1                         
    # tokuten = round(subTokuten(Total))    
    
    return tokuten1, tokuten2, tokuten3, tokuten, passed 

def Tokuten(soten):
    if(soten >= 106):
        return tokutenUpper(soten)
    elif(soten < 106 and soten >= 85):
        return 95
    else:
        return soten

def tokutenLower(soten):
    return soten * 95/106

def tokutenUpper(soten):
    return 180 - (85/74) * (180-soten)

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

    
    X[['tokuten1', 'tokuten2', 'tokuten3', 'tokuten', 'Passed']] = X.apply(lambda row: pd.Series(tokutenAndPassed(row['S1'], row['S2'], row['S3'], row['Total'], row['Anchor'],)), axis=1)
    
    # Export part1 and part2 as new CSV files
    print(X)
    X.to_csv('data/3Q_Result.csv', index=False)

else:
    print('there is no file')