import spacy
import pandas as pd

nlp = spacy.load('./NER_Training/models/outcome_model/model-best')

#### PUBMED #################

df = pd.read_csv('pubmed_raw_data.csv', sep=';')
abstracts = df.abstract.dropna()
abstracts = abstracts.drop_duplicates()


docs = nlp.pipe(abstracts)


for doc in docs:
    for ent in doc.ents:
        print(ent.label_+'\t'+'\t'+ent.text)