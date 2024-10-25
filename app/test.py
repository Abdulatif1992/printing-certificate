from PIL import Image

def convert_png_to_pdf(png_path, pdf_path):
    image = Image.open(png_path)
    image.convert('RGB').save(pdf_path)

# Rasmni PNG dan PDF ga aylantirish
convert_png_to_pdf('data/正答率バー/bar_25.png', 'output_image.pdf')