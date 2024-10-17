# -*- coding: utf-8 -*-
import string
import re
import spacy
from spacy.lang.en.stop_words import STOP_WORDS 

stop_words = STOP_WORDS
pontuacoes = string.punctuation

def auto_detect_model():
    try:
        return spacy.load("en_core_web_lg")
    except OSError:
        pass
    try:
        return spacy.load("en_core_web_md")
    except OSError:
        pass
    try:
        return spacy.load("en_core_web_sm")
    except OSError:
        pass
    return None

def remove_emojis(text):
    emoji_pattern = re.compile(
        "["
        u"\U0001F600-\U0001F64F"  
        u"\U0001F300-\U0001F5FF"  
        u"\U0001F680-\U0001F6FF"  
        u"\U0001F1E0-\U0001F1FF"  
        u"\U00002500-\U00002BEF"  
        u"\U00002702-\U000027B0"  
        u"\U000024C2-\U0001F251" 
        "]+", flags=re.UNICODE)
    
    return emoji_pattern.sub(r'', text)

def P_eng(text):
    pln = auto_detect_model()
    if pln is None:
        print("No model available on the system, see the package README file to choose one of the spaCy models.")
        return None
    text = text.lower()
    text = re.sub(r'http\S+|www\S+|https\S+', '', text, flags=re.MULTILINE) 
    text = re.sub(r'@\w+|#\w+', '', text)
    text = remove_emojis(text)
    text = re.sub(r'[^a-zA-Z0-9\s]', '', text)
    doc = pln(text)    
    lista = [token.lemma_ for token in doc if token.text not in stop_words and token.text not in pontuacoes]

    lista = ' '.join([str(token) for token in lista if not token.isdigit() and len(token) > 1])
    
    return lista


