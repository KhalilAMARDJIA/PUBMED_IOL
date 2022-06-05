import pandas as pd
import spacy
nlp = spacy.load("en_core_sci_sm")

dat = pd.read_csv('pubmed_raw_data.csv', sep=';')
dat = dat['abstract'].dropna()

docs = nlp.pipe(dat)

text = ''

for doc in docs:
    for sent in doc.sents:
        text += sent.text + "\n"


with open('NER_Training/training_text.txt', 'w') as file:
    file.write(text)