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

def getLevelNameJapanese(level):
    return level+"Q(N"+level+"相当)"

def getLevelNameEnglish(level):
    return level+"Q(N"+level+"equivalent)"

def getJapaneseDate():
    # Bugungi sanani olish
    today = datetime.datetime.today()

    year = today.strftime("%Y")
    month = today.strftime("%m")
    day = today.strftime("%d")
    
    return year +"年"+ month +"月"+day+"日"

def getEnglishDate():
    # Bugungi sanani olish
    today = datetime.datetime.today()
    # Sanani formatlash
    formatted_date = today.strftime("%B %d, %Y")
    return formatted_date

def getTestDateEnglish(number):
    month = str(number)[2:4]
    monthinteger = int(month)
    monthName = datetime.date(1900, monthinteger, 1).strftime('%B')
    
    year = str(number)[0:2]    
    year = "20"+year

    return monthName+" "+year

def getTestDateJapanese(number):
    month = str(number)[2:4]
    monthinteger = int(month)
    monthName = datetime.date(1900, monthinteger, 1).strftime('%B')
    
    year = str(number)[0:2]    
    year = "20"+year

    return year+"年"+month+"月"

def getTestSiteEnglish(testSite):
    match int(testSite):
        case 890:
            return "TOKYO / JAPAN"
        case 550:
            return "KATHMANDU / NEPAL"
        
def getTestSiteJapanese(testSite):
    match int(testSite):
        case 890:
            return "東京 / 日本"
        case 550:
            return "カトマンズ / ネパール"

def getTextWidth(text, c, font_name, font_size):
    #matnning kengligini aniqlaymiz
    text = str(text)
    text_width = c.stringWidth(text, font_name, font_size)
    return text_width

def split_text_to_fit(text, c, page_width, font_name, font_size):

    words = text.split(' ')
    lines = []
    current_line = ''

    for word in words:
        # Har bir so'z uchun vaqtincha qator yaratish
        temp_line = current_line + (word if current_line == '' else ' ' + word)
        
        # Agar qator sahifa kengligidan oshmasa, uni qator sifatida saqlaymiz
        if c.stringWidth(temp_line, font_name, font_size) <= page_width:
            current_line = temp_line
        else:
            # Qator kengligidan oshsa, uni saqlaymiz va yangi qatorni boshlaymiz
            lines.append(current_line)
            current_line = word

    # Oxirgi qatorni ham qo'shamiz
    if current_line:
        lines.append(current_line)
    
    return lines

def create_pdf_with_background(row):
    # Define the A4 page size
    width, height = landscape(A4)
    
    # Create the PDF canvas
    c = canvas.Canvas('pdf files/'+str(row['受験番号'])+'.pdf', pagesize=landscape(A4))

    # # Add the background image
    # background_image_path = "data/sample.png"
    # background = ImageReader(background_image_path)
    # c.drawImage(background, 0, 0, width=width, height=height)

    # Set font and font size for text
    c.setFont("Meiryo", 9)

    # Change the position of the additional image
    user_image = "data/userImages/"+str(row['受験番号'])+".png"   
    # Adjust x, y position for the image
    image_x = 5.5 * cm  # Change this value to set horizontal position
    image_y = 3.3 * cm  # Change this value to set vertical position    
    # Add the image with the new location
    c.drawImage(user_image, image_x, image_y, width = 2.8 * cm, height=3.7 * cm)    

    # First row
    c.setFont("Meiryo", 15)
    text_x = 8.75 * cm
    text_y = 6.5 * cm 
    c.drawString(text_x, text_y, "級")                                                          # Kyuu
    c.drawString(text_x + 2.7 * cm, text_y, getLevelNameJapanese(str(row['受験番号'])[9]))      # Level
    c.drawString(text_x + 8.45 * cm, text_y, getJapaneseDate())                                 # Date
    
    # First column
    #japanese
    c.setFont("Meiryo", 9)
    c.drawString(text_x, text_y - 0.95 * cm, "受験番号")                                 
    c.drawString(text_x, text_y - 1.85 * cm, "試験年月")                                  
    c.drawString(text_x, text_y - 2.8 * cm, "試験会場")    
    # English   
    c.setFont("Meiryo", 6)
    c.drawString(text_x, text_y - 0.33 * cm, "Level")                          
    c.drawString(text_x, text_y - 1.25 * cm, "Examinee's Number")
    c.drawString(text_x, text_y - 2.15 * cm, "Test Month & Year")
    c.drawString(text_x, text_y - 3.1 * cm, "Test Site")    

    # Second   column      
    c.drawString(text_x + 2.7 * cm, text_y - 0.33 * cm, getLevelNameEnglish(str(row['受験番号'])[9]))   # Level
    c.drawString(text_x + 2.7 * cm, text_y - 2.15 * cm, getTestDateEnglish(str(row['受験番号'])))       # Test date English
    c.drawString(text_x + 2.7 * cm, text_y - 3.1 * cm, getTestSiteEnglish(str(row['受験番号'])[6:9]))   # Test site English

    c.setFont("Meiryo", 9)
    c.drawString(text_x + 2.7 * cm, text_y - 0.95 * cm, str(row['受験番号']))                           # Examinee's number
    c.drawString(text_x + 2.7 * cm, text_y - 1.85 * cm, getTestDateJapanese(str(row['受験番号'])))      # Test date Japanese
    c.drawString(text_x + 2.7 * cm, text_y - 2.8 * cm, getTestSiteJapanese(str(row['受験番号'])[6:9]))  # Test site Japanese

    # Third column
    c.setFont("Meiryo", 11)
    c.drawString(text_x + 8.45 * cm, text_y - 0.75 * cm, getEnglishDate())      # Date

    # Name   
    c.setFont("Times-BoldItalic", 36) 
    name = row['name']
    name = name.upper()
    text_width = getTextWidth(name, c, "Times-BoldItalic", 36)
    border = 3 * cm
    width_without_border = width - border * 2
    if(width_without_border >= text_width):
        text_x = (width-text_width)/2        
        c.drawString(text_x, text_y + 4.3 * cm, str(name))           # Name
    else:
        lines = split_text_to_fit(name, c, width_without_border, "Times-BoldItalic", 36)
        text_width = getTextWidth(lines[0], c, "Times-BoldItalic", 36)
        text_x = (width-text_width)/2
        c.drawString(text_x, text_y + 5 * cm, str(lines[0]))                # Name line1

        text_width = getTextWidth(lines[1], c, "Times-BoldItalic", 36)
        text_x = (width-text_width)/2
        c.drawString(text_x, text_y + 3.8 * cm, str(lines[1]))              # Name line2

    # Save the PDF
    c.save()


if os.path.exists(file_path):
    
    # Register Meiryo font before using it
    register_meiryo_font()

    # Load your data
    Data = pd.read_csv(file_path, encoding='shift_jis', low_memory=False)
    Data = Data[Data['合否判定'] == "***合格***"]
    
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
