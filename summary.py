from googletrans import Translator
from langdetect import detect
from nltk.corpus import stopwords
from nltk.tokenize import sent_tokenize, word_tokenize
from sklearn.feature_extraction.text import TfidfVectorizer
import heapq

import nltk
nltk.download('punkt')


def get_stopwords(language):
    if language == 'hi':
        # Load Hindi stopwords from the custom file
        with open('hindi_words.txt', 'r', encoding='utf-8') as file:
            stopwords_list = [line.strip() for line in file]
        return set(stopwords_list)
    else:
        return set(stopwords.words('english'))

def summarize_and_translate(text, summary_percentage=0.45, target_language='english'):
    # Step 1: Summarize the text in English
    english_summary = summarize_text(text, summary_percentage)
    
    # Step 2: Translate the original text to the target language
    translator = Translator()
    translated_text = translator.translate(text, dest=target_language).text
    
    # Step 3: Translate the English summary to the target language
    translated_summary = translator.translate(english_summary, dest=target_language)
    if translated_summary:
        translated_summary = translated_summary.text
    else:
        translated_summary = "Summary translation not available"

    
    return translated_text, translated_summary

def summarize_text(text, summary_percentage=0.45, language='english'):
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
