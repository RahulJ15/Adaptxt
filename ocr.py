#This is our base OCR model that reads text from images and files and performs pre processing for a more accurate result
from PIL import Image
import pytesseract
import cv2
import numpy as np
import os
from googletrans import Translator
import PyPDF2
import heapq
import langdetect 
from langdetect import detect
import tkinter as tk

class LanguageSelectorGUI:
    def __init__(self):
        self.root = tk.Tk()
        self.root.title("Language Selector")

        self.label = tk.Label(self.root, text="Select a target language for translation:")
        self.label.pack()

        self.languages = {'1': 'Hindi', '2': 'French', '3': 'Spanish', '4': 'Chinese', '5': 'English'}

        for key, value in self.languages.items():
            button = tk.Button(self.root, text=f"{key}. {value}", command=lambda k=key: self.select_language(k))
            button.pack()

    def select_language(self, choice):
        selected_language = self.languages.get(choice, 'English')
        print(f"Selected language: {selected_language}")
        # You can add further processing here, such as returning the selected language or calling other functions.

    def run(self):
        self.root.mainloop()




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

    def deskew_image(self, image):
        gray = cv2.cvtColor(image, cv2.COLOR_BGR2GRAY)
        gray = cv2.bitwise_not(gray)
        coords = np.column_stack(np.where(gray > 0))
        angle = cv2.minAreaRect(coords)[-1]
        angle = -(90 + angle) if angle < -45 else -angle
        h, w = image.shape[:2]
        center = (w // 2, h // 2)
        M = cv2.getRotationMatrix2D(center, angle, 1.0)
        deskewed = cv2.warpAffine(image, M, (w, h), flags=cv2.INTER_CUBIC, borderMode=cv2.BORDER_REPLICATE)
        return deskewed

    def remove_table_lines(self, image):
        gray = cv2.cvtColor(image, cv2.COLOR_BGR2GRAY)
        edges = cv2.Canny(gray, 50, 150, apertureSize=3)
        lines = cv2.HoughLinesP(edges, 1, np.pi / 180, 100, minLineLength=100, maxLineGap=10)

        for line in lines:
            x1, y1, x2, y2 = line[0]
            cv2.line(image, (x1, y1), (x2, y2), (255, 255, 255), 2)

    def preprocess_image(self):
        img = cv2.imread(self.image_path)

        cv2.cvtColor(img, cv2.COLOR_BGR2GRAY)
        cv2.imwrite('greyscale.jpeg', img)
        Image.open("greyscale.jpeg").save("greyscale.jpeg")

        self.remove_table_lines(img)

        _, im_bw = cv2.threshold(img, 125, 255, cv2.THRESH_BINARY)
        cv2.imwrite('binary.jpeg', im_bw)
        Image.open("binary.jpeg").save("binary.jpeg")

        def noise_removal(image):
            kernel = np.ones((1, 1), np.uint8)
            image = cv2.dilate(image, kernel, iterations=1)
            image = cv2.morphologyEx(image, cv2.MORPH_CLOSE, kernel)
            image = cv2.medianBlur(image, 1)
            return image

        no_noise = noise_removal(im_bw)
        cv2.imwrite('noiseless.jpeg', no_noise)
        Image.open("noiseless.jpeg").save("noiseless.jpeg")

        self.image_path = 'noiseless.jpeg'

    def perform_ocr(self):
        text = pytesseract.image_to_string(self.image_path)
        return text

    def translate_text(self, text, target_language='en'):
        translator = Translator()
        translated = translator.translate(text, dest=target_language)
        return translated.text

    def select_target_language(self):
        # Create an instance of the LanguageSelectorGUI class and run the GUI.
        language_selector = LanguageSelectorGUI()
        language_selector.run()

    def extract_text_from_pdf(self):
        pdf_text = ""
        with open(self.image_path, 'rb') as pdf_file:
            pdf_reader = PyPDF2.PdfReader(pdf_file)
            pdf_text = ''.join(pdf_reader.pages[i].extract_text() for i in range(len(pdf_reader.pages)))
        return pdf_text

    def detect_language(self, text):
        try:
            detected_lang = detect(text)
        except:
            detected_lang = "unknown"
        return detected_lang


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


if __name__ == "__main__":
    image_path = input("Enter the path of the PDF or image: ")
    ocr_processor = ImageOCR(image_path)

    if image_path.lower().endswith((".pdf", ".jpg", ".jpeg", ".png")):
        if image_path.lower().endswith(".pdf"):
            ocr_processor.process_pdf_and_summarize()
        else:
            ocr_processor.convert_to_jpeg()
            ocr_processor.deskew_image(cv2.imread(ocr_processor.image_path))
            ocr_processor.preprocess_image()
            recognized_text = ocr_processor.perform_ocr()
            print("Recognized Text:")
            print(recognized_text)

            original_language = ocr_processor.detect_language(recognized_text)
            print("Original Language:", original_language)

            target_language = ocr_processor.select_target_language()
            translated_text = ocr_processor.translate_text(recognized_text, target_language)
            print("Translated Text:")
            print(translated_text)


    else:
        print("Invalid file format. Supported formats: PDF, JPG, JPEG, PNG.")
