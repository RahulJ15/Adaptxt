from PIL import Image
import pytesseract
import cv2
import os
from googletrans import Translator
import PyPDF2
import langdetect 
from langdetect import detect
import easyocr

class ImageOCR:
    def __init__(self, image_path):
        self.image_path = image_path

    def convert_to_jpeg(self):
        _, file_extension = os.path.splitext(self.image_path)
        if file_extension.lower() not in ['.jpg', '.jpeg']:
            img = cv2.imread(self.image_path)
            jpeg_image_path = os.path.splitext(self.image_path)[0] + '.jpeg'
            cv2.imwrite(jpeg_image_path, img)
            self.image_path = jpeg_image_path

    def process_pdf_and_summarize(self):
        pdf_text = self.extract_text_from_pdf()
        print("Recognized Text from PDF:")
        print(pdf_text)

        original_language = self.detect_language(pdf_text)
        print("Original Language:", original_language)

        target_language = self.select_target_language()
        translated_text = self.translate_text(pdf_text, target_language)
        print("Translated Text from PDF:")
        print(translated_text)

    def extract_text_from_pdf(self):
        pdf_text = ""
        with open(self.image_path, 'rb') as pdf_file:
            pdf_reader = PyPDF2.PdfReader(pdf_file)
            pdf_text = ''.join(pdf_reader.pages[i].extract_text() for i in range(len(pdf_reader.pages)))
        return pdf_text

    def translate_text(self, text, target_language='en'):
        translator = Translator()
        translated = translator.translate(text, dest=target_language)
        return translated.text

    def select_target_language(self):
        print("Select a target language for translation:")
        print("1. Hindi")
        print("2. French")
        print("3. Spanish")
        print("4. Chinese")
        print("5. English")
        choice = input("Enter the number of your choice: ")
        languages = {'1': 'hi', '2': 'fr', '3': 'es', '4': 'zh-cn', '5': 'en'}
        return languages.get(choice, 'en')

    def detect_language(self, text):
        try:
            detected_lang = detect(text)
        except:
            detected_lang = "unknown"
        return detected_lang

    def perform_easyocr(self):
        reader = easyocr.Reader(['en'], gpu=False)
        result = reader.readtext(self.image_path)
        return result

if __name__ == "__main__":
    image_path = input("Enter the path of the PDF or image: ")
    ocr_processor = ImageOCR(image_path)

    if image_path.lower().endswith((".pdf", ".jpg", ".jpeg", ".png")):
        if image_path.lower().endswith(".pdf"):
            ocr_processor.process_pdf_and_summarize()
        else:
            ocr_processor.convert_to_jpeg()
            easyocr_result = ocr_processor.perform_easyocr()
            print("EasyOCR Result:")
            for item in easyocr_result:
                print(item)
    else:
        print("Invalid file format. Supported formats: PDF, JPG, JPEG, PNG.")
