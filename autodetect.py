from PIL import Image
import pytesseract
import cv2
import numpy as np
import os
from googletrans import Translator
import PyPDF2
import heapq


import langdetect #pip install langdetect
from langdetect import detect
from nltk.corpus import stopwords
from nltk.tokenize import word_tokenize, sent_tokenize
from nltk.tag import pos_tag
from nltk import ne_chunk
import nltk

nltk.download('punkt')
nltk.download('stopwords')
nltk.download('maxent_ne_chunker')
nltk.download('words')
nltk.download('averaged_perceptron_tagger')


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
        print("Select a target language for translation:")
        print("1. Hindi")
        print("2. French")
        print("3. Spanish")
        print("4. Mandarin")
        print("5. English")
        choice = input("Enter the number of your choice: ")
        languages = {'1': 'hi', '2': 'fr', '3': 'es', '4': 'zh-cn', '5': 'en'}
        return languages.get(choice, 'en')

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

    def summarize_text(self, text):
        stopwords_list = set(stopwords.words('english'))
        sentence_list = sent_tokenize(text)
        frequency_map = {}
        word_list = word_tokenize(text)

        def extract_named_entities(text):
            entities = []
            words = word_tokenize(text)
            pos_tags = pos_tag(words)
            named_entities = ne_chunk(pos_tags)
            for entity in named_entities:
                if isinstance(entity, tuple):
                    entities.append(entity[0])
                else:
                    entities.extend([word[0] for word in entity.leaves()])
            return entities

        for word in word_list:
            if word.lower() not in stopwords_list:
                frequency_map[word] = frequency_map.get(word, 0) + 1

        named_entities = extract_named_entities(text)
        for entity in named_entities:
            if entity.lower() not in stopwords_list:
                frequency_map[entity] = frequency_map.get(entity, 0) + 1

        max_frequency = max(frequency_map.values(), default=1)

        for word in frequency_map:
            frequency_map[word] = frequency_map[word] / max_frequency

        sent_scores = {}

        for sent in sentence_list:
            for word in word_tokenize(sent):
                if word in frequency_map and len(sent.split(' ')) < 35:
                    sent_scores[sent] = sent_scores.get(sent, 0) + frequency_map[word]

        summary = heapq.nlargest(3, sent_scores, key=sent_scores.get)
        return ' '.join(summary)

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

        summarized_text = self.summarize_text(translated_text)



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

            summarized_text = ocr_processor.summarize_text(translated_text)
            print("\nSummarized Text:")
            print(summarized_text)
    else:
        print("Invalid file format. Supported formats: PDF, JPG, JPEG, PNG.")
