from PIL import Image
import pytesseract
import cv2
import numpy as np
import os

import enchant  # For spell-checking
#pip install pyenchant 
from googletrans import Translator
#pip install googletrans==4.0.0-rc1



class ImageOCR:
    def __init__(self, image_path):
        self.image_path = image_path
        #enchant.set_param('enchant.myspell.suggest.threshold', 1)  # Set sensitivity

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
        if angle < -45:
            angle = -(90 + angle)
        else:
            angle = -angle
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

        inverted_image = cv2.bitwise_not(img)
        cv2.imwrite("inverted.jpeg", inverted_image)
        Image.open("inverted.jpeg")

        grey_img = cv2.cvtColor(img, cv2.COLOR_BGR2GRAY)
        cv2.imwrite('greyscale.jpeg', grey_img)
        Image.open("greyscale.jpeg")

        self.remove_table_lines(img) 

        _, im_bw = cv2.threshold(grey_img, 125, 255, cv2.THRESH_BINARY)
        cv2.imwrite('binary.jpeg', im_bw)
        Image.open("binary.jpeg")

        def noise_removal(image):
            kernel = np.ones((1, 1), np.uint8)
            image = cv2.dilate(image, kernel, iterations=1)
            image = cv2.morphologyEx(image, cv2.MORPH_CLOSE, kernel)
            image = cv2.medianBlur(image, 1)
            return image
        
        enhanced_image = cv2.convertScaleAbs(im_bw, alpha=2, beta=0)  # Enhance the image
        cv2.imwrite('enhanced.jpeg', enhanced_image)
        Image.open("enhanced.jpeg")

        no_noise = noise_removal(im_bw)
        cv2.imwrite('noiseless.jpeg', no_noise)
        Image.open("noiseless.jpeg")

        self.image_path = 'noiseless.jpeg'

    def perform_ocr(self):
        text = pytesseract.image_to_string(self.image_path)
        return text
    
    def post_process_text(self, text):
        # Example: Spell-checking using PyEnchant
        d = enchant.Dict("en_US")
        words = text.split()
        corrected_words = []
        for word in words:
            if not d.check(word):
                suggestions = d.suggest(word)
                if suggestions:
                    corrected_word = suggestions[0]
                    corrected_words.append(corrected_word)
                else:
                    corrected_words.append(word)
            else:
                corrected_words.append(word)

        corrected_text = ' '.join(corrected_words)
        return corrected_text
    
    def translate_text(self, text, target_language='en'):
        translator = Translator()
        translated = translator.translate(text, dest=target_language)
        return translated.text 


    def select_target_language(self):
        print("Select a target language for translation:")
        print("1. Hindi")
        print("2. French")
        print("3. Spanish")
        print("4. Mandarin")
        
        choice = input("Enter the number of your choice: ")
        languages = {
            '1': 'hi',  # Hindi
            '2': 'fr',  # French
            '3': 'es',  # Spanish
            '4': 'zh-cn'  # Mandarin
        }
        
        return languages.get(choice, 'en')     
    

# Usage example:
if __name__ == "__main__":
    image_path = "hindi_esay.jpeg"
    ocr_processor = ImageOCR(image_path)
    ocr_processor.convert_to_jpeg()
    ocr_processor.deskew_image(cv2.imread(ocr_processor.image_path))
    ocr_processor.preprocess_image()
    recognized_text = ocr_processor.perform_ocr()
    corrected_text = ocr_processor.post_process_text(recognized_text)
    print("Recognized Text:")
    print(corrected_text)

    target_language = ocr_processor.select_target_language()
    translated_text = ocr_processor.translate_text(corrected_text, target_language)
    print("Translated Text:")
    print(translated_text)
  

