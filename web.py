# -*- coding: utf-8 -*-
"""
Created on Tue Nov 16 12:14:00 2021

@author: Sangsam
"""

import streamlit as st 
import os


# NLP Pkgs
from textblob import TextBlob 
import spacy
from spacy.lang.en.stop_words import STOP_WORDS
from string import punctuation
from heapq import nlargest
from spacy.lang.en.stop_words import STOP_WORDS
from string import punctuation
import en_core_web_sm

punctuation = punctuation+'/n' 


# Function for Sumy Summarization
def spacy_summarizer(docx):
    stopwords = list(STOP_WORDS)
    nlp = en_core_web_sm.load()
    doc = nlp(docx)
    mytokens = [token.text for token in doc]
    
    
    word_frequencies = {}
    for word in  doc:
        if word.text.lower() not in stopwords:
            if word.text.lower() not in punctuation:
                if word.text not in word_frequencies.keys():
                    word_frequencies[word.text]=1
                else:
                    word_frequencies[word.text] += 1
                    
    # Maximum Word Frequency
    maximum_frequency = max(word_frequencies.values())
    for word in word_frequencies.keys(): # normalization 
        word_frequencies[word] = (word_frequencies[word]/maximum_frequency)
    
    sentences_token = [ sent for sent in doc.sents]
    sentence_scores = {}  
    for sent in sentences_token:  
        for word in sent:
            if word.text.lower() in word_frequencies.keys():
                if sent not in sentence_scores.keys():
                    sentence_scores[sent] = word_frequencies[word.text.lower()]
                else:
                    sentence_scores[sent] += word_frequencies[word.text.lower()]
                    
    select_lenght = int(len(sentences_token)*0.3)
    summarized_sentences = nlargest(select_lenght,sentence_scores,key = sentence_scores.get)
    final_sentences = [ w.text for w in summarized_sentences ]
    summary = ' '.join(final_sentences)
    
    return summary
                        

# Function to Analyse Tokens and Lemma
@st.cache
def text_analyzer(my_text):
	nlp = en_core_web_sm.load()
	docx = nlp(my_text)
	allData = [('"Token":{},\n"Lemma":{}'.format(token.text,token.lemma_))for token in docx ]
	return allData

# Function For Extracting Entities
@st.cache
def entity_analyzer(my_text):
	nlp = en_core_web_sm.load()
	docx = nlp(my_text)
	tokens = [ token.text for token in docx]
	entities = [(entity.text,entity.label_)for entity in docx.ents]
	allData = ['"Token":{},\n"Entities":{}'.format(tokens,entities)]
	return allData


def main():
	""" NLP Based App with Streamlit """

	# Title
	st.title("Textiffy with Streamlit")
	st.subheader("All in one Natural Language Processing App ..")
	st.markdown("""
    	#### Description
    	+ This is a Natural Language Processing(NLP) Based App useful for basic NLP task like 
    	Tokenization,NER,Sentiment,Summarization
    	""")

	# Tokenization
	if st.checkbox("Show Tokens and Lemma"):
		st.subheader("Tokenize Your Text")

		message = st.text_area("Enter Text","Type Here ..")
		if st.button("Analyze"):
			nlp_result = text_analyzer(message)
			st.json(nlp_result)

	# Entity Extraction
	if st.checkbox("Show Named Entities"):
		st.subheader("Analyze Your Text")

		message = st.text_area("Enter Text","Type Here ..")
		if st.button("Extract"):
			entity_result = entity_analyzer(message)
			st.json(entity_result)

	# Sentiment Analysis
	if st.checkbox("Show Sentiment Analysis"):
		st.subheader("Analyse Your Text")

		message = st.text_area("Enter Text","Type Here ..")
		if st.button("Analyze"):
			blob = TextBlob(message)
			result_sentiment = blob.sentiment.polarity
			st.success(result_sentiment)

	# Summarization
	if st.checkbox("Show Text Summarization"):
		st.subheader("Summarize Your Text")

		message = st.text_area("Enter Text","Type Here ..")
		if st.button("Summarize"):
			summary_result = spacy_summarizer(message)
			st.success(summary_result)

	st.sidebar.subheader("NLP App")
	st.sidebar.info("More Functionality Coming soon")
    


	st.sidebar.subheader("By")
	st.sidebar.text("Sangarsh")





if __name__ == '__main__':
	main()
