from googletrans import Translator
from langdetect import detect 
import streamlit as st
from PIL import Image
import PyPDF2

from ocr import ImageOCR #calling ocr model
from summary import get_stopwords, summarize_text #calling summary model

# Initialize the translator
translator = Translator()

# Streamlit user interface setup
st.title('OCR, Translation, and Summarization')

# Sidebar for file upload and language selection
uploaded_file = st.sidebar.file_uploader("Choose a file (PDF, JPG, JPEG, PNG)", type=['pdf', 'jpg', 'jpeg', 'png'])
lang_options = {'Hindi': 'hi', 'English': 'en', 'French': 'fr', 'Spanish': 'es', 'Chinese': 'zh-CN'}
target_lang = st.sidebar.selectbox("Select target language for translation:", options=list(lang_options.keys()))


# Main content
if uploaded_file is not None:
    text = ""
    if uploaded_file.type == "application/pdf":
        # Extract text from PDF
        reader = PyPDF2.PdfReader(uploaded_file)
        for page_num in range(len(reader.pages)):
            text += reader.pages[page_num].extract_text()
    else:
        # Perform OCR on the image
        image = Image.open(uploaded_file)
        ocr = ImageOCR(image)
        text = ocr.perform_ocr()

    if text:
        # Detect language and display it
        detected_language = detect(text)
        st.subheader("Detected Language:")
        st.write(detected_language)

        # Display the original text
        st.subheader("Original Text:")
        st.write(text)

        # Translate the text and display it
        translated_text = translator.translate(text, dest=lang_options[target_lang]).text
        st.subheader(f"Translated Text ({target_lang}):")
        st.write(translated_text)

        # Summarize the translated text and display it
        if st.button("Summarize"):
            summarized_text = summarize_text(translated_text, language=target_lang.lower())
            st.subheader("Summarized Text:")
            st.write(summarized_text)
    else:
        st.write("No text could be extracted.")
