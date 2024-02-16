from nltk.corpus import stopwords
from nltk.tokenize import sent_tokenize, word_tokenize
from sklearn.feature_extraction.text import TfidfVectorizer
from googletrans import Translator
from langdetect import detect
from autodetect import ImageOCR  # Ensure this import matches your ImageOCR class
import heapq
import streamlit as st
from PIL import Image
import PyPDF2

# Initialize the translator
translator = Translator()

# Streamlit user interface setup
st.title('OCR, Translation, and Summarization')

# Sidebar for file upload and language selection
uploaded_file = st.sidebar.file_uploader("Choose a file (PDF, JPG, JPEG, PNG)", type=['pdf', 'jpg', 'jpeg', 'png'])
lang_options = {'Hindi': 'hi', 'English': 'en', 'French': 'fr', 'Spanish': 'es', 'Chinese': 'zh-CN'}
target_lang = st.sidebar.selectbox("Select target language for translation:", options=list(lang_options.keys()))


def get_stopwords(language):
    if language == 'hi':
            # Load Hindi stopwords from the custom file
            with open('hindi_words.txt', 'r', encoding='utf-8') as file:
                stopwords_list = [line.strip() for line in file]
            return set(stopwords_list)
    else:
        return set(stopwords.words('english'))


def summarize_text(text, summary_percentage=0.30, language='english'):
    # Tokenize the text into sentences
    sentences = sent_tokenize(text)
    
    # Remove stopwords and tokenize words
    stop_words = get_stopwords(language)
    words = [word.lower() for word in word_tokenize(text) if word.lower() not in stop_words and word.isalnum()]
    
    # Calculate TF-IDF scores for each word
    tfidf_vectorizer = TfidfVectorizer()
    tfidf_matrix = tfidf_vectorizer.fit_transform([' '.join(words)])
    feature_names = tfidf_vectorizer.get_feature_names_out()
    word_tfidf_scores = dict(zip(feature_names, tfidf_matrix.toarray()[0]))
    
    # Score sentences based on TF-IDF scores
    sentence_scores = {}
    for sentence in sentences:
        sentence_words = [word.lower() for word in word_tokenize(sentence) if word.lower() not in stop_words and word.isalnum()]
        sentence_tfidf_score = sum(word_tfidf_scores.get(word, 0) for word in sentence_words)
        sentence_scores[sentence] = sentence_tfidf_score
    
    # Calculate the summary length based on the percentage of total sentences
    summary_length = max(int(len(sentences) * summary_percentage), 1)
    
    # Select the top 'summary_length' sentences with the highest scores
    summary_sentences = heapq.nlargest(summary_length, sentence_scores, key=sentence_scores.get)
    summary = ' '.join(summary_sentences)
    return summary

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
