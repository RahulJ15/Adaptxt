#Summary using Natural Language ToolKit
#This model is a basic extractive type  of summarization,meaning it does not form new sentences rather uses sentences and words in the para to make a summary 
#Summary model v2 with Named Entity Relation using trees

import nltk
import heapq
from nltk.corpus import stopwords
from nltk.tokenize import word_tokenize, sent_tokenize
from nltk.tag import pos_tag
from nltk import ne_chunk

nltk.download('punkt') #used for tokenization (breaking down text into individiual words)
nltk.download('stopwords') ##downloads list of stop words such as - and,but,so,the,that
nltk.download('maxent_ne_chunker') #helps identify names of people,places,organisations etc
nltk.download('words') ##contains various words for NER
nltk.download('averaged_perceptron_tagger') #used for understanding of noun,verb,adverb,adjectives (Parts Of Speech)


text = input("Enter the text you want to summarize:\n")
stopwords_list = set(stopwords.words('english'))

sentence_list = sent_tokenize(text)
frequency_map = {}

word_list = word_tokenize(text)

# Perform Named Entity Recognition
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

# Count frequencies, considering named entities
for word in word_list:
    if word.lower() not in stopwords_list:
        if word not in frequency_map:
            frequency_map[word] = 1
        else:
            frequency_map[word] += 1

# Add named entities to the frequency map
named_entities = extract_named_entities(text)
for entity in named_entities:
    if entity.lower() not in stopwords_list:
        if entity not in frequency_map:
            frequency_map[entity] = 1
        else:
            frequency_map[entity] += 1

max_frequency = max(frequency_map.values())

# Normalize frequencies
for word in frequency_map:
    frequency_map[word] = frequency_map[word] / max_frequency ## counts frequency and importance of words,if frequency of word above a certain threshold it will considered important

sent_scores = {}

# Calculate scores, considering named entities
for sent in sentence_list:
    for word in word_tokenize(sent):
        if word in frequency_map and len(sent.split(' ')) < 35:
            if sent not in sent_scores:
                sent_scores[sent] = frequency_map[word]
            else:
                sent_scores[sent] += frequency_map[word]

# Finding top 10 sentences based on score:
summary = heapq.nlargest(10, sent_scores, key=sent_scores.get)

# Count the number of words in the original text
num_words_original = len(word_list)

# Count the number of words in the summarized text
num_words_summarized = sum(len(word_tokenize(sent)) for sent in summary)

# Print the number of words in the original and summarized text
print(f"\nNumber of words in the original text: {num_words_original}")
print(f"Number of words in the summarized text: {num_words_summarized}")

for a in summary:
    print(a)
