import streamlit as st
from PIL import Image
import pytesseract
import cv2
import numpy as np
import PyPDF2
from googletrans import Translator

# Import the ImageOCR class from your uploaded file
from handwriting.model import ImageOCR

# Initialize the translator
translator = Translator()

# Streamlit user interface
st.set_page_config(page_title='OCR and Translation', layout='wide')
st.title('OCR and Translation')

# Sidebar for inputs
with st.sidebar:
    st.header("Upload and Settings")
    # File upload
    uploaded_file = st.file_uploader("Choose a file (PDF, JPG, JPEG, PNG)", type=['pdf', 'jpg', 'jpeg', 'png'])
    # Language selection
    lang_options = {'Hindi': 'hi', 'French': 'fr', 'Spanish': 'es', 'Mandarin': 'zh-CN'}
    target_lang = st.selectbox("Select target language for translation:", options=list(lang_options.keys()))

# Main content
if uploaded_file is not None:
    # Process the uploaded file
    if uploaded_file.type == "application/pdf":
        # Extract text from PDF
        reader = PyPDF2.PdfReader(uploaded_file)
        text = ""
        for page_num in range(len(reader.pages)):
            text += reader.pages[page_num].extract_text()
    else:
        # Perform OCR on the image
        image = Image.open(uploaded_file)
        ocr = ImageOCR(image)
        text = ocr.perform_ocr()

    # Display the original English text
    st.subheader("Original English Text:")
    st.write(text)

    # Translate the text
    translated_text = translator.translate(text, dest=lang_options[target_lang]).text

    # Display the results
    st.subheader(f"Translation to {target_lang}:")
    st.write(translated_text)

# Footer
st.markdown("---")
st.markdown("OCR and Translation | Developed by Rahul Jiandani & Vanshika Nijhawan")