from googletrans import Translator
from langdetect import detect
import streamlit as st
from PIL import Image
import PyPDF2

from ocr import ImageOCR  # calling OCR model
from summary import summarize_and_translate  # calling modified summary model

# Initialize the translator
translator = Translator()

# Streamlit user interface setup
st.title('Adaptxt: Recognition, Translation, and Summarization')

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

    if text is not None:
        # Detect language and display it
        detected_language = detect(text)
        st.subheader("Detected Language:")
        st.write(detected_language)

        # Display the original text
        st.subheader("Original Text:")
        st.write(text)

        try:

            # Translate the text and display it
            translated_text = translator.translate(text, dest=lang_options[target_lang]).text
            st.subheader(f"Translated Text ({target_lang}):")
            st.write(translated_text)

            # Summarize and translate the text only when the button is clicked
            if st.button("Summarize"):
                translated_summary = summarize_and_translate(text, target_language=lang_options[target_lang])

                # Display the translated summary
                st.subheader(f"Summary ({target_lang}):")
                st.write(translated_summary[1])

        except Exception as e:
            st.error(f"Error during translation or summarization:{e}")

    else:
        st.write("No text could be extracted.")
