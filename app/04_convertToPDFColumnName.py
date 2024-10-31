from reportlab.lib.pagesizes import A4, landscape
from reportlab.pdfgen import canvas
from reportlab.lib.units import cm
from reportlab.lib.utils import ImageReader
from reportlab.pdfbase.ttfonts import TTFont
from reportlab.pdfbase import pdfmetrics
from PIL import Image
import tempfile
import datetime
import pandas as pd
import os
import io

# Define the folder name to add to the path
folder_name = "data"
# Specify the file name
file_name = 'grade_list.csv'

# Define the path to the file
# Since the script is in the 'app' folder, use '..' to move up one directory
file_path = os.path.join(folder_name, file_name)

# Register the Meiryo font
def register_meiryo_font():
    # Replace this with the actual path to your Meiryo font file
    font_path = "C:/Windows/Fonts/Meiryo.ttc"  # Path to Meiryo font on Windows
    pdfmetrics.registerFont(TTFont('Meiryo', font_path))

def text_width(text, c, font='Meiryo', size = 9):
    #matnning kengligini aniqlaymiz
    text = str(text)
    text_width = c.stringWidth(text, font, size)
    return text_width

def getOverallPassMark(number, section):
    level = str(number)[9]
    level = int(level)
    result = '0'

    match level:
        case 1:
            match section:
                case 0:
                    result = '100'
                case 1:
                    result = '19'
                case 2:
                    result = '19'
                case 3:
                    result = '19'    
        case 2:
            match section:
                case 0:
                    result = '90'
                case 1:
                    result = '19'
                case 2:
                    result = '19'
                case 3:
                    result = '19'    
        case 3:
            match section:
                case 0:
                    result = '95'
                case 1:
                    result = '19'
                case 2:
                    result = '19'
                case 3:
                    result = '19'    
        case 4:
            match section:
                case 0:
                    result = '90'
                case 1:
                    result = '38'
                case 2:
                    result = '19'
                case 3:
                    result = ''    
        case 5:
            match section:
                case 0:
                    result = '80'
                case 1:
                    result = '38'
                case 2:
                    result = '19'
                case 3:
                    result = ''    
    return result 

def getLevelAsText(number):
    level = str(number)[9]
    return level+"Q (N"+level+"相当)    "+level+"Q (N"+level+" equivalent)"

def getMonthAndYearAsText(number):
    month = str(number)[2:4]
    monthinteger = int(month)
    monthName = datetime.date(1900, monthinteger, 1).strftime('%B')
    
    year = str(number)[0:2]    
    year = "20"+year

    return year+"年"+str(monthinteger)+"月    " +monthName+" "+year

def getImageName(percent):
    # '%' belgisini olib tashlash
    value = percent.replace('%', '')

    # Butun qismini olish
    integer_part = int(float(value))
    image_path = "data/正答率バー/bar_"+str(integer_part)+".png"

    
    # PNG faylni yuklash va shaffofligini saqlash
    img = Image.open(image_path)

    # Vaqtinchalik fayl yaratish
    temp_file = tempfile.NamedTemporaryFile(delete=False, suffix=".png")
    img.save(temp_file, format='PNG')  # PNG ni vaqtinchalik faylga saqlash
    temp_file.close()
    
    return temp_file.name  # Vaqtinchalik fayl nomini qaytarish

def getIdsFromImage():
    # Rasm joylashgan papka yo'lini ko'rsatish
    folder_path = 'data/userImages'

    # Bo'sh array yaratish
    image_names = []

    # Papka ichidagi fayllarni o'qish
    for file_name in os.listdir(folder_path):
        # Agar faylning kengaytmasi .png bo'lsa
        if file_name.endswith('.png'):
            # Fayl nomini kengaytmasiz olish
            image_name = os.path.splitext(file_name)[0]
            image_names.append(image_name)

    return image_names

def getDateOfIssue():
    # Bugungi sanani olish
    today = datetime.datetime.today()
    # Sanani formatlash
    formatted_date = today.strftime("%B %d, %Y")
    year = today.strftime("%Y")
    month = today.strftime("%m")
    day = today.strftime("%d")
    
    return year +" 年 "+ month +" 月 "+day+" 日   "+formatted_date

def create_pdf_with_background(row):
    # Define the A4 page size
    width, height = landscape(A4)
    margin = 0.5 * cm
    
    # Create the PDF canvas
    c = canvas.Canvas('pdf files/'+str(row['受験番号'])+'.pdf', pagesize=landscape(A4))

    # Add the background image
    background_image_path = "data/2023年09月_日本語NAT-TEST成績表背景.png"
    background = ImageReader(background_image_path)
    c.drawImage(background, margin, margin, width=width-margin*2, height=height-margin*2)

    # Set font and font size for text
    c.setFont("Meiryo", 9)

    # Set each text line individually
    # Date of Issue
    c.drawString(21.2 * cm, height - 1.75*cm, getDateOfIssue())  # date

    # Position the first group of text (examineeInformation)
    distance = 0.85 * cm
    text_x = 7 * cm
    text_y = height - 2.6 * cm   # Start near the top of the page

    c.drawString(text_x, text_y - distance * 0, getMonthAndYearAsText(row['受験番号']))  # date
    c.drawString(text_x, text_y - distance * 1, getLevelAsText(row['受験番号']))         # level
    c.drawString(text_x, text_y - distance * 2, str(row['受験番号']))                    # examinee's number
    c.drawString(text_x, text_y - distance * 3, str(row['name']).upper())                   # name

    # Position the second group of texts (result)
    distance = 0.45 * cm
    resultText_x = 4.1 * cm
    scoreText_x = 12.9 * cm    
    resultText_y = height - 8.1 * cm   # Start near the top of the page

    c.drawString(resultText_x, resultText_y - distance * 0, str(row['分野名1']))        # section name1
    c.drawString(resultText_x, resultText_y - distance * 1, str(row['分野名2']))        # section name2
    if not pd.isna(row['分野名3']):  # Agar qiymat NaN bo'lmasa
        c.drawString(resultText_x, resultText_y - distance * 2, str(row['分野名3']))    # section name3
    
    # Score section (Max score)
    c.setFont("Meiryo", 12)
    c.drawString(scoreText_x - text_width(int(row['配点総合']), c, 'Meiryo', 12), resultText_y + 0.6 * cm, str(int(row['配点総合'])))
    c.setFont("Meiryo", 9)
    c.drawString(scoreText_x - text_width(int(row['配点1']), c), resultText_y - distance * 0, str(int(row['配点1'])))                # section score1
    c.drawString(scoreText_x - text_width(int(row['配点2']), c), resultText_y - distance * 1, str(int(row['配点2'])))                # section score2
    if not pd.isna(row['配点3']):  # Agar qiymat NaN bo'lmasa 
        c.drawString(scoreText_x - text_width(int(row['配点3']), c), resultText_y - distance * 2, str(int(row['配点3'])))            # section score3


    # Score section
    overalText_x = 11.3 * cm 
    c.setFont("Meiryo", 12) 
    c.drawString(overalText_x - text_width(int(row['得点総合']), c, 'Meiryo', 12), resultText_y + 0.6 * cm, str(int(row['得点総合'])))   # score overall    
    c.setFont("Meiryo", 9)
    c.drawString(overalText_x - text_width(int(row['得点1']), c), resultText_y - distance * 0, str(int(row['得点1'])))      # score1  
    c.drawString(overalText_x - text_width(int(row['得点2']), c), resultText_y - distance * 1, str(int(row['得点2'])))      # score2  
    if not pd.isna(row['得点3']):  # Agar qiymat NaN bo'lmasa 
        c.drawString(overalText_x - text_width(int(row['得点3']), c), resultText_y - distance * 2, str(int(row['得点3'])))  # score3 

    # # just a line    
    overalText_x = 11.7 * cm 
    c.drawString(overalText_x, resultText_y + 0.6 * cm, "/")  
    c.drawString(overalText_x, resultText_y - distance * 0, "/")       
    c.drawString(overalText_x, resultText_y - distance * 1, "/")       
    if not pd.isna(row['得点3']):  # Agar qiymat NaN bo'lmasa 
        c.drawString(overalText_x, resultText_y - distance * 2, "/") 

    # Overall Pass Marks section  
    maxText_x = 15 * cm
    c.drawString(maxText_x - text_width(getOverallPassMark(row['受験番号'], 0), c), resultText_y + 0.6 * cm, getOverallPassMark(row['受験番号'], 0))       # score overall  
    c.drawString(maxText_x - text_width(getOverallPassMark(row['受験番号'], 1), c), resultText_y - distance * 0, getOverallPassMark(row['受験番号'], 1))   # score1  
    c.drawString(maxText_x - text_width(getOverallPassMark(row['受験番号'], 2), c), resultText_y - distance * 1, getOverallPassMark(row['受験番号'], 2))   # score2  
    c.drawString(maxText_x - text_width(getOverallPassMark(row['受験番号'], 3), c), resultText_y - distance * 2, getOverallPassMark(row['受験番号'], 3))   # score3  
    

    # main section
    distance = 0.45 * cm
    sectionText_x = 1.75 * cm
    sectionText_y = height - 11.31 * cm   # Start near the top of the page
    c.drawString(sectionText_x, sectionText_y - distance * 0, row['section_q1']) # sectionName1
    c.drawString(sectionText_x, sectionText_y - distance * 1, row['section_q2']) # sectionName2
    c.drawString(sectionText_x, sectionText_y - distance * 2, row['section_q3']) # sectionName3
    c.drawString(sectionText_x, sectionText_y - distance * 3, row['section_q4']) # sectionName4
    c.drawString(sectionText_x, sectionText_y - distance * 4, row['section_q5']) # sectionName5
    c.drawString(sectionText_x, sectionText_y - distance * 5, row['section_q6']) # sectionName6
    c.drawString(sectionText_x, sectionText_y - distance * 6, row['section_q7']) # sectionName7
    c.drawString(sectionText_x, sectionText_y - distance * 7, row['section_q8']) # sectionName8
    c.drawString(sectionText_x, sectionText_y - distance * 8, row['section_q9']) # sectionName9
    c.drawString(sectionText_x, sectionText_y - distance * 9, row['section_q10']) # sectionName10
    c.drawString(sectionText_x, sectionText_y - distance * 10, row['section_q11']) # sectionName11
    c.drawString(sectionText_x, sectionText_y - distance * 11, row['section_q12']) # sectionName12
    c.drawString(sectionText_x, sectionText_y - distance * 12, row['section_q13']) # sectionName13
    c.drawString(sectionText_x, sectionText_y - distance * 13, row['section_q14']) # sectionName14
    if not pd.isna(row['section_q15']):  # Agar qiymat NaN bo'lmasa
        c.drawString(sectionText_x, sectionText_y - distance * 14, str(row['section_q15'])) # sectionName15
    if not pd.isna(row['section_q16']):  # Agar qiymat NaN bo'lmasa
        c.drawString(sectionText_x, sectionText_y - distance * 15, str(row['section_q16'])) # sectionName16
    if not pd.isna(row['section_q17']):  # Agar qiymat NaN bo'lmasa
        c.drawString(sectionText_x, sectionText_y - distance * 16, str(row['section_q17'])) # sectionName17
    if not pd.isna(row['section_q18']):  # Agar qiymat NaN bo'lmasa
        c.drawString(sectionText_x, sectionText_y - distance * 17, str(row['section_q18'])) # sectionName18
    if not pd.isna(row['section_q19']):  # Agar qiymat NaN bo'lmasa
        c.drawString(sectionText_x, sectionText_y - distance * 18, str(row['section_q19'])) # sectionName19

    # Question section  
    questionText_x = 7.75 * cm  
    c.drawString(questionText_x, sectionText_y - distance * 0, row['問題1']) # questionNumber1
    c.drawString(questionText_x, sectionText_y - distance * 1, row['問題2']) # questionNumber2
    c.drawString(questionText_x, sectionText_y - distance * 2, row['問題3']) # questionNumber3
    c.drawString(questionText_x, sectionText_y - distance * 3, row['問題4']) # questionNumber4
    c.drawString(questionText_x, sectionText_y - distance * 4, row['問題5']) # questionNumber5
    c.drawString(questionText_x, sectionText_y - distance * 5, row['問題6']) # questionNumber6
    c.drawString(questionText_x, sectionText_y - distance * 6, row['問題7']) # questionNumber7
    c.drawString(questionText_x, sectionText_y - distance * 7, row['問題8']) # questionNumber8
    c.drawString(questionText_x, sectionText_y - distance * 8, row['問題9']) # questionNumber9
    c.drawString(questionText_x, sectionText_y - distance * 9, row['問題10']) # questionNumber10
    c.drawString(questionText_x, sectionText_y - distance * 10, row['問題11']) # questionNumber11
    c.drawString(questionText_x, sectionText_y - distance * 11, row['問題12']) # questionNumber12
    c.drawString(questionText_x, sectionText_y - distance * 12, row['問題13']) # questionNumber13
    c.drawString(questionText_x, sectionText_y - distance * 13, row['問題14']) # questionNumber14
    if not pd.isna(row['問題15']):  # Agar qiymat NaN bo'lmasa
        c.drawString(questionText_x, sectionText_y - distance * 14, str(row['問題15'])) # questionNumber15
    if not pd.isna(row['問題16']):  # Agar qiymat NaN bo'lmasa
        c.drawString(questionText_x, sectionText_y - distance * 15, str(row['問題16'])) # questionNumber16
    if not pd.isna(row['問題17']):  # Agar qiymat NaN bo'lmasa
        c.drawString(questionText_x, sectionText_y - distance * 16, str(row['問題17'])) # questionNumber17
    if not pd.isna(row['問題18']):  # Agar qiymat NaN bo'lmasa
        c.drawString(questionText_x, sectionText_y - distance * 17, str(row['問題18'])) # questionNumber18
    if not pd.isna(row['問題19']):  # Agar qiymat NaN bo'lmasa
        c.drawString(questionText_x, sectionText_y - distance * 18, str(row['問題19'])) # questionNumber19

    # Question section  
    questionText_x = 9.85 * cm  
    c.drawString(questionText_x, sectionText_y - distance * 0, row['question_name_q1']) # questionName1
    c.drawString(questionText_x, sectionText_y - distance * 1, row['question_name_q2']) # questionName2
    c.drawString(questionText_x, sectionText_y - distance * 2, row['question_name_q3']) # questionName3
    c.drawString(questionText_x, sectionText_y - distance * 3, row['question_name_q4']) # questionName4
    c.drawString(questionText_x, sectionText_y - distance * 4, row['question_name_q5']) # questionName5
    c.drawString(questionText_x, sectionText_y - distance * 5, row['question_name_q6']) # questionName6
    c.drawString(questionText_x, sectionText_y - distance * 6, row['question_name_q7']) # questionName7
    c.drawString(questionText_x, sectionText_y - distance * 7, row['question_name_q8']) # questionName8
    c.drawString(questionText_x, sectionText_y - distance * 8, row['question_name_q9']) # questionName9
    c.drawString(questionText_x, sectionText_y - distance * 9, row['question_name_q10']) # questionName10
    c.drawString(questionText_x, sectionText_y - distance * 10, row['question_name_q11']) # questionName11
    c.drawString(questionText_x, sectionText_y - distance * 11, row['question_name_q12']) # questionName12
    c.drawString(questionText_x, sectionText_y - distance * 12, row['question_name_q13']) # questionName13
    c.drawString(questionText_x, sectionText_y - distance * 13, row['question_name_q14']) # questionName14
    if not pd.isna(row['question_name_q15']):  # Agar qiymat NaN bo'lmasa
        c.drawString(questionText_x, sectionText_y - distance * 14, str(row['question_name_q15'])) # questionName15
    if not pd.isna(row['question_name_q16']):  # Agar qiymat NaN bo'lmasa
        c.drawString(questionText_x, sectionText_y - distance * 15, str(row['question_name_q16'])) # questionName16
    if not pd.isna(row['question_name_q17']):  # Agar qiymat NaN bo'lmasa
        c.drawString(questionText_x, sectionText_y - distance * 16, str(row['question_name_q17'])) # questionName17
    if not pd.isna(row['question_name_q18']):  # Agar qiymat NaN bo'lmasa
        c.drawString(questionText_x, sectionText_y - distance * 17, str(row['question_name_q18'])) # questionName18
    if not pd.isna(row['question_name_q19']):  # Agar qiymat NaN bo'lmasa
        c.drawString(questionText_x, sectionText_y - distance * 18, str(row['question_name_q19'])) # questionName19
    
    
    # total  section
    totalText_x = 16.2 * cm  
    c.drawString(totalText_x - text_width(int(row['total_q1']), c), sectionText_y - distance * 0, str(int(row['total_q1']))) # total1
    c.drawString(totalText_x - text_width(int(row['total_q2']), c), sectionText_y - distance * 1, str(int(row['total_q2']))) # total2
    c.drawString(totalText_x - text_width(int(row['total_q3']), c), sectionText_y - distance * 2, str(int(row['total_q3']))) # total3
    c.drawString(totalText_x - text_width(int(row['total_q4']), c), sectionText_y - distance * 3, str(int(row['total_q4']))) # total4
    c.drawString(totalText_x - text_width(int(row['total_q5']), c), sectionText_y - distance * 4, str(int(row['total_q5']))) # total5
    c.drawString(totalText_x - text_width(int(row['total_q6']), c), sectionText_y - distance * 5, str(int(row['total_q6']))) # total6
    c.drawString(totalText_x - text_width(int(row['total_q7']), c), sectionText_y - distance * 6, str(int(row['total_q7']))) # total7
    c.drawString(totalText_x - text_width(int(row['total_q8']), c), sectionText_y - distance * 7, str(int(row['total_q8']))) # total8
    c.drawString(totalText_x - text_width(int(row['total_q9']), c), sectionText_y - distance * 8, str(int(row['total_q9']))) # total9
    c.drawString(totalText_x - text_width(int(row['total_q10']), c), sectionText_y - distance * 9, str(int(row['total_q10']))) # total10
    c.drawString(totalText_x - text_width(int(row['total_q11']), c), sectionText_y - distance * 10, str(int(row['total_q11']))) # total11
    c.drawString(totalText_x - text_width(int(row['total_q12']), c), sectionText_y - distance * 11, str(int(row['total_q12']))) # total12
    c.drawString(totalText_x - text_width(int(row['total_q13']), c), sectionText_y - distance * 12, str(int(row['total_q13']))) # total13
    c.drawString(totalText_x - text_width(int(row['total_q14']), c), sectionText_y - distance * 13, str(int(row['total_q14']))) # total14
    if not pd.isna(row['total_q15']):  # Agar qiymat NaN bo'lmasa
        c.drawString(totalText_x - text_width(int(row['total_q15']), c), sectionText_y - distance * 14, str(int(row['total_q15']))) # total15
    if not pd.isna(row['total_q16']):  # Agar qiymat NaN bo'lmasa
        c.drawString(totalText_x - text_width(int(row['total_q16']), c), sectionText_y - distance * 15, str(int(row['total_q16']))) # total16
    if not pd.isna(row['total_q17']):  # Agar qiymat NaN bo'lmasa
        c.drawString(totalText_x - text_width(int(row['total_q17']), c), sectionText_y - distance * 16, str(int(row['total_q17']))) # total17
    if not pd.isna(row['total_q18']):  # Agar qiymat NaN bo'lmasa
        c.drawString(totalText_x - text_width(int(row['total_q18']), c), sectionText_y - distance * 17, str(int(row['total_q18']))) # total18
    if not pd.isna(row['total_q19']):  # Agar qiymat NaN bo'lmasa
        c.drawString(totalText_x - text_width(int(row['total_q19']), c), sectionText_y - distance * 18, str(int(row['total_q19']))) # total19  
    
    # correct answers section  
    totalText_x = 15.7 * cm  
    c.drawString(totalText_x - text_width(row['correct_q1'], c), sectionText_y - distance * 0, str(row['correct_q1'])) # correct1
    c.drawString(totalText_x - text_width(row['correct_q2'], c), sectionText_y - distance * 1, str(row['correct_q2'])) # correct2
    c.drawString(totalText_x - text_width(row['correct_q3'], c), sectionText_y - distance * 2, str(row['correct_q3'])) # correct3
    c.drawString(totalText_x - text_width(row['correct_q4'], c), sectionText_y - distance * 3, str(row['correct_q4'])) # correct4
    c.drawString(totalText_x - text_width(row['correct_q5'], c), sectionText_y - distance * 4, str(row['correct_q5'])) # correct5
    c.drawString(totalText_x - text_width(row['correct_q6'], c), sectionText_y - distance * 5, str(row['correct_q6'])) # correct6
    c.drawString(totalText_x - text_width(row['correct_q7'], c), sectionText_y - distance * 6, str(row['correct_q7'])) # correct7
    c.drawString(totalText_x - text_width(row['correct_q8'], c), sectionText_y - distance * 7, str(row['correct_q8'])) # correct8
    c.drawString(totalText_x - text_width(row['correct_q9'], c), sectionText_y - distance * 8, str(row['correct_q9'])) # correct9
    c.drawString(totalText_x - text_width(row['correct_q10'], c), sectionText_y - distance * 9, str(row['correct_q10'])) # correct10
    c.drawString(totalText_x - text_width(row['correct_q11'], c), sectionText_y - distance * 10, str(row['correct_q11'])) # correct11
    c.drawString(totalText_x - text_width(row['correct_q12'], c), sectionText_y - distance * 11, str(row['correct_q12'])) # correct12
    c.drawString(totalText_x - text_width(row['correct_q13'], c), sectionText_y - distance * 12, str(row['correct_q13'])) # correct13
    c.drawString(totalText_x - text_width(row['correct_q14'], c), sectionText_y - distance * 13, str(row['correct_q14'])) # correct14
    if not pd.isna(row['correct_q15']):  # Agar qiymat NaN bo'lmasa
        c.drawString(totalText_x - text_width(row['correct_q15'], c), sectionText_y - distance * 14, str(row['correct_q15'])) # correct15
    if not pd.isna(row['correct_q16']):  # Agar qiymat NaN bo'lmasa
        c.drawString(totalText_x - text_width(row['correct_q16'], c), sectionText_y - distance * 15, str(row['correct_q16'])) # correct16
    if not pd.isna(row['correct_q17']):  # Agar qiymat NaN bo'lmasa
        c.drawString(totalText_x - text_width(row['correct_q17'], c), sectionText_y - distance * 16, str(row['correct_q17'])) # correct17
    if not pd.isna(row['correct_q18']):  # Agar qiymat NaN bo'lmasa
        c.drawString(totalText_x - text_width(row['correct_q18'], c), sectionText_y - distance * 17, str(row['correct_q18'])) # correct18
    if not pd.isna(row['correct_q19']):  # Agar qiymat NaN bo'lmasa
        c.drawString(totalText_x - text_width(row['correct_q19'], c), sectionText_y - distance * 18, str(row['correct_q19'])) # correct19
    
    
    # percentage section  
    totalText_x = 18.3 * cm  
    c.drawString(totalText_x - text_width(row['percent_q1'], c), sectionText_y - distance * 0, str(row['percent_q1'])) # percent1
    c.drawString(totalText_x - text_width(row['percent_q2'], c), sectionText_y - distance * 1, str(row['percent_q2'])) # percent2
    c.drawString(totalText_x - text_width(row['percent_q3'], c), sectionText_y - distance * 2, str(row['percent_q3'])) # percent3
    c.drawString(totalText_x - text_width(row['percent_q4'], c), sectionText_y - distance * 3, str(row['percent_q4'])) # percent4
    c.drawString(totalText_x - text_width(row['percent_q5'], c), sectionText_y - distance * 4, str(row['percent_q5'])) # percent5
    c.drawString(totalText_x - text_width(row['percent_q6'], c), sectionText_y - distance * 5, str(row['percent_q6'])) # percent6
    c.drawString(totalText_x - text_width(row['percent_q7'], c), sectionText_y - distance * 6, str(row['percent_q7'])) # percent7
    c.drawString(totalText_x - text_width(row['percent_q8'], c), sectionText_y - distance * 7, str(row['percent_q8'])) # percent8
    c.drawString(totalText_x - text_width(row['percent_q9'], c), sectionText_y - distance * 8, str(row['percent_q9'])) # percent9
    c.drawString(totalText_x - text_width(row['percent_q10'], c), sectionText_y - distance * 9, str(row['percent_q10'])) # percent10
    c.drawString(totalText_x - text_width(row['percent_q11'], c), sectionText_y - distance * 10, str(row['percent_q11'])) # percent11
    c.drawString(totalText_x - text_width(row['percent_q12'], c), sectionText_y - distance * 11, str(row['percent_q12'])) # percent12
    c.drawString(totalText_x - text_width(row['percent_q13'], c), sectionText_y - distance * 12, str(row['percent_q13'])) # percent13
    c.drawString(totalText_x - text_width(row['percent_q14'], c), sectionText_y - distance * 13, str(row['percent_q14'])) # percent14
    if not pd.isna(row['percent_q15']):  # Agar qiymat NaN bo'lmasa
        c.drawString(totalText_x - text_width(row['percent_q15'], c), sectionText_y - distance * 14, str(row['percent_q15'])) # percent15
    if not pd.isna(row['percent_q16']):  # Agar qiymat NaN bo'lmasa
        c.drawString(totalText_x - text_width(row['percent_q16'], c), sectionText_y - distance * 15, str(row['percent_q16'])) # percent16
    if not pd.isna(row['percent_q17']):  # Agar qiymat NaN bo'lmasa
        c.drawString(totalText_x - text_width(row['percent_q17'], c), sectionText_y - distance * 16, str(row['percent_q17'])) # percent17
    if not pd.isna(row['percent_q18']):  # Agar qiymat NaN bo'lmasa
        c.drawString(totalText_x - text_width(row['percent_q18'], c), sectionText_y - distance * 17, str(row['percent_q18'])) # percent18
    if not pd.isna(row['percent_q19']):  # Agar qiymat NaN bo'lmasa
        c.drawString(totalText_x - text_width(row['percent_q19'], c), sectionText_y - distance * 18, str(row['percent_q19'])) # percent19  
    
    
    # percentage Image section  
    PercentImage_x = 18.4 * cm    
    distanceImage = 0.45 * cm
    c.drawImage(getImageName(row['percent_q1']), PercentImage_x, sectionText_y - distanceImage * 0, width=9.6 * cm, height=0.3 * cm, mask='auto')        
    c.drawImage(getImageName(row['percent_q2']), PercentImage_x, sectionText_y - distanceImage * 1, width=9.6 * cm, height=0.3 * cm, mask='auto')        
    c.drawImage(getImageName(row['percent_q3']), PercentImage_x, sectionText_y - distanceImage * 2, width=9.6 * cm, height=0.3 * cm, mask='auto')        
    c.drawImage(getImageName(row['percent_q4']), PercentImage_x, sectionText_y - distanceImage * 3, width=9.6 * cm, height=0.3 * cm, mask='auto')        
    c.drawImage(getImageName(row['percent_q5']), PercentImage_x, sectionText_y - distanceImage * 4, width=9.6 * cm, height=0.3 * cm, mask='auto')        
    c.drawImage(getImageName(row['percent_q6']), PercentImage_x, sectionText_y - distanceImage * 5, width=9.6 * cm, height=0.3 * cm, mask='auto')        
    c.drawImage(getImageName(row['percent_q7']), PercentImage_x, sectionText_y - distanceImage * 6, width=9.6 * cm, height=0.3 * cm, mask='auto')        
    c.drawImage(getImageName(row['percent_q8']), PercentImage_x, sectionText_y - distanceImage * 7, width=9.6 * cm, height=0.3 * cm, mask='auto')        
    c.drawImage(getImageName(row['percent_q9']), PercentImage_x, sectionText_y - distanceImage * 8, width=9.6 * cm, height=0.3 * cm, mask='auto')        
    c.drawImage(getImageName(row['percent_q10']), PercentImage_x, sectionText_y - distanceImage * 9, width=9.6 * cm, height=0.3 * cm, mask='auto')        
    c.drawImage(getImageName(row['percent_q11']), PercentImage_x, sectionText_y - distanceImage * 10, width=9.6 * cm, height=0.3 * cm, mask='auto')        
    c.drawImage(getImageName(row['percent_q12']), PercentImage_x, sectionText_y - distanceImage * 11, width=9.6 * cm, height=0.3 * cm, mask='auto')        
    c.drawImage(getImageName(row['percent_q13']), PercentImage_x, sectionText_y - distanceImage * 12, width=9.6 * cm, height=0.3 * cm, mask='auto')        
    c.drawImage(getImageName(row['percent_q14']), PercentImage_x, sectionText_y - distanceImage * 13, width=9.6 * cm, height=0.3 * cm, mask='auto')           
    if not pd.isna(row['percent_q15']):  # Agar qiymat NaN bo'lmasa
        c.drawImage(getImageName(row['percent_q15']), PercentImage_x, sectionText_y - distanceImage * 14, width=9.6 * cm, height=0.3 * cm, mask='auto')        
    if not pd.isna(row['percent_q16']):  # Agar qiymat NaN bo'lmasa    
        c.drawImage(getImageName(row['percent_q16']), PercentImage_x, sectionText_y - distanceImage * 15, width=9.6 * cm, height=0.3 * cm, mask='auto')        
    if not pd.isna(row['percent_q17']):  # Agar qiymat NaN bo'lmasa    
        c.drawImage(getImageName(row['percent_q17']), PercentImage_x, sectionText_y - distanceImage * 16, width=9.6 * cm, height=0.3 * cm, mask='auto')        
    if not pd.isna(row['percent_q18']):  # Agar qiymat NaN bo'lmasa    
        c.drawImage(getImageName(row['percent_q18']), PercentImage_x, sectionText_y - distanceImage * 17, width=9.6 * cm, height=0.3 * cm, mask='auto')        
    if not pd.isna(row['percent_q19']):  # Agar qiymat NaN bo'lmasa    
        c.drawImage(getImageName(row['percent_q19']), PercentImage_x, sectionText_y - distanceImage * 18, width=9.6 * cm, height=0.3 * cm, mask='auto')        

    # Pass image
    if row['合否判定']=="***合格***": # agar  nomzod o'tdi bo'lsa
        pass_image_path = "data/合格判定/goukaku.png"
        # Adjust x, y position for the image
        image_x = 16.5 * cm  # Change this value to set horizontal position
        image_y = 12.1 * cm  # Change this value to set vertical position    
        c.drawImage(pass_image_path, image_x, image_y, width=1.8 * cm, height=1.8 * cm)

    # Change the position of the additional image
    user_image = "data/userImages/"+str(row['受験番号'])+".png"   
    # Adjust x, y position for the image
    image_x = 1.5 * cm  # Change this value to set horizontal position
    image_y = 15.6 * cm  # Change this value to set vertical position    
    # Add the image with the new location
    c.drawImage(user_image, image_x, image_y, width=2.3 * cm, height=3.07 * cm)    
    
    # Save the PDF
    c.save()



if os.path.exists(file_path):
    
    # Register Meiryo font before using it
    register_meiryo_font()

    # Load your data
    Data = pd.read_csv(file_path, encoding='shift_jis', low_memory=False)

    # barcha rasm bor ekanligini tekshiruvchi funsiya
    idNumbers = Data['受験番号']
    idFromImages = getIdsFromImage()
    
    # Rasmdan olingan id'larni to'plam shaklida olamiz va int() formatiga o'tkazamiz
    image_ids_set = set(int(id) for id in idFromImages)

    # CSV fayldan olingan id'larni to'plam shaklida olamiz
    csv_ids_set = set(idNumbers)

    # CSV'da mavjud lekin rasmlarda yo'q bo'lgan id'larni topamiz
    missing_ids = csv_ids_set - image_ids_set

    # Agar missing_ids bo'sh bo'lmasa, xabar chiqaramiz
    if missing_ids:        
        print("Rasmlarda mavjud bo'lmagan ID'lar:", missing_ids)
    else:
        # Agar missing_ids bo'sh bo'lsa, keyingi kodlar ishlaydi
        # DataFrame bo'yicha loop
        for index, row in Data.iterrows():
            print(f"{row.iloc[0]}")        
        
            text_name = "XASFS ODZN IJI"

            # Create the PDF
            create_pdf_with_background(row)
        
else:
    print('there is no file')
