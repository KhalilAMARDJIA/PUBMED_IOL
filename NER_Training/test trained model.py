import spacy
import pandas as pd

nlp = spacy.load('./NER_Training/models/outcome_model/model-best')

#### PUBMED #################

df = pd.read_csv('pubmed_raw_data.csv', sep=';')
df.abstract = df.abstract.dropna()
df.abstract = df.abstract.drop_duplicates()


abstracts_w_id = []  # create a tuple of (abstract, id) to trace
for abstract,pubmed_id in zip(df.abstract.astype(str),df.pubmed_id.astype(str)): 
    abstracts_w_id.append((abstract,pubmed_id))

docs = nlp.pipe(abstracts_w_id, as_tuples= True)

ner_data = {
    "pubmed_id":[],
    "entity": [],
    "tag": []
}


for doc, pubmed_id in docs:
    for ent in doc.ents:
        ner_data["pubmed_id"].append(pubmed_id)
        ner_data["entity"].append(ent.text)
        ner_data["tag"].append(ent.label_)

dat = pd.DataFrame(ner_data)
dat = dat.pivot_table(index= "pubmed_id", columns= "tag", values="entity", aggfunc=list)

dat.to_csv("./saved_csv/ner_data.csv", sep = ";")
