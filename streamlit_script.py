from googletrans import Translator
from langdetect import detect
import streamlit as st
from PIL import Image
import io
import easyocr
import fitz  # PyMuPDF
from summary import summarize_and_translate
from stt import record_text

# Initialize the translator
translator = Translator()

import nltk
nltk.download('popular')

# Streamlit user interface setup
st.title('Adaptxt: OCR, Translation, and Summarization')

# Sidebar for file upload and language selection
uploaded_file = st.sidebar.file_uploader("Choose a file (PDF, JPG, JPEG, PNG)", type=['pdf', 'jpg', 'jpeg', 'png'])
lang_options = {'Hindi': 'hi', 'English': 'en', 'French': 'fr', 'Spanish': 'es', 'Chinese': 'zh-CN'}
target_lang = st.sidebar.selectbox("Select target language for translation:", options=list(lang_options.keys()))

# Function to record audio and get text
def get_recorded_text():
    st.write("Listening for audio input...")
    recorded_text = record_text()
    if recorded_text:
        st.write(recorded_text)
        translated_recorded_text = translator.translate(recorded_text, dest=lang_options[target_lang]).text
        st.subheader(f"Translated Audio Text ({target_lang}):")
        st.write(translated_recorded_text)
    else:
        st.write("No audio input detected.")

# Main content
if uploaded_file is not None:
    text = ""

    if uploaded_file.type == "application/pdf":
        # Extract text from PDF using PyMuPDF
        pdf_document = fitz.open(stream=uploaded_file.read(), filetype='pdf')
        for page_num in range(pdf_document.page_count):
            page = pdf_document.load_page(page_num)
            page_text = page.get_text()
            if page_text:
                text += page_text
            else:
                st.warning(f"Unable to extract text from page {page_num + 1}")

    else:
        # Perform OCR on the image using EasyOCR
        image = Image.open(uploaded_file)
        img_byte_array = io.BytesIO()
        image.save(img_byte_array, format='PNG')
        img_byte_array = img_byte_array.getvalue()
        
        reader = easyocr.Reader(['en'], gpu=False)
        result = reader.readtext(img_byte_array)
        text = " ".join([entry[1] for entry in result])

    # Clean the extracted text by replacing '#' with spaces
    cleaned_text = text.replace('#', ' ')

    if cleaned_text:  # Proceed only if there's valid text
        # Detect language and display it
        detected_language = detect(cleaned_text)
        st.subheader("Detected Language:")
        st.write(detected_language)

        # Display the original text
        st.subheader("Original Text:")
        st.write(cleaned_text)

        try:
            # Translate the text and display it
            translated_text = translator.translate(cleaned_text, dest=lang_options[target_lang]).text
            st.subheader(f"Translated Text ({target_lang}):")
            st.write(translated_text)

            if st.button("Summarize"):
                try:
                    translated_summary = summarize_and_translate(cleaned_text, target_language=lang_options[target_lang])
                    if translated_summary[1]:
                        st.subheader(f"Summary ({target_lang}):")
                        st.write(translated_summary[1])
                    else:
                        st.write("Summary translation not available.")
                except Exception as e:
                    st.error(f"Error during translation or summarization: {e}")

        except Exception as e:
            st.error(f"Error during translation or summarization: {e}")
    else:
        st.write("No text could be extracted.")

# Button for speech-to-text functionality in the sidebar
if st.sidebar.button("Speech to Text"):
    get_recorded_text()
