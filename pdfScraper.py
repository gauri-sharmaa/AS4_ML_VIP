##Prasun's scraping file 

import re
from pdfminer.high_level import extract_pages, extract_text
import pandas as pd

def get_text(pdfname):
    text = extract_text(pdfname)
    return text

def get_sentences(text):
    pattern = r'(?<!\w\.\w.)(?<![A-Z][a-z]\.)(?<=\.|\?|\!)\s'
    sentences = re.split(pattern, text)
    sentences = [s.strip() for s in sentences if s.strip()]
    return sentences

def display_setnences(list):
    for sentence in list:
        print(sentence + "\n")
        print("--------------------------------------")

def dictionary_to_df(sentences):
    return pd.DataFrame(sentences, columns=['Sentence'])

def save_dataframe(df, filename):
    try:
        df.to_csv(filename)
        print("save successful")
    except:
        print("file not saved properly")



text = get_text("BH.pdf")
sentences = get_sentences(text)
df = dictionary_to_df(sentences)
save_dataframe(df, "Berkshire_sentences.csv")
