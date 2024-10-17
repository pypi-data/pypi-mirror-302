# -*- coding: utf-8 -*-
import string
import re
import spacy
from spacy.lang.pt.stop_words import STOP_WORDS 

stop_words = STOP_WORDS
pontuacoes = string.punctuation

def auto_detect_model():
    try:
        return spacy.load("pt_core_news_lg")
    except OSError:
      pass
    try:
        return spacy.load("pt_core_news_md")
    except OSError:
      pass
    
    try:
        return spacy.load("pt_core_news_sm")
    except OSError:
      pass
    
    return None

def remove_emojis(texto):
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
    
    return emoji_pattern.sub(r'', texto)

def P_pt_br(texto):
    pln = auto_detect_model()
    if pln is None:
        print("Nenhum modelo disponível no sistema, consulte o arquivo README do pacote para escolher um dos modelos do spaCy.")
        return None
    texto = texto.lower()
    texto = re.sub(r'http\S+|www\S+|https\S+', '', texto, flags=re.MULTILINE) 
    texto = re.sub(r'@\w+|#\w+', '', texto)  
    texto = remove_emojis(texto)  
    texto = re.sub(r'[^a-zA-Z0-9\s]', '', texto)
    doc = pln(texto)    
    lista = [token.lemma_ for token in doc if token.text not in stop_words and token.text not in pontuacoes]

    lista = ' '.join([str(token) for token in lista if not token.isdigit() and len(token) > 1])
    
    return lista

