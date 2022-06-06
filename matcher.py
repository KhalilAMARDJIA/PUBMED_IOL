import pandas as pd
import spacy
from spacy.matcher import Matcher
import json

df = pd.read_csv("pubmed_raw_data.csv", sep = ';', encoding='UTF-8')
df = df[df['abstract'].notna()]
nlp = spacy.load('en_core_sci_sm')
matcher = Matcher(nlp.vocab)

with open ("databases/patterns.json", encoding='UTF-8') as file:
    patterns = json.load(file)

patient_age = [patterns[0]['age']]
sample_size = [patterns[0]['sample_size']]
outcomes = [patterns[0]['outcomes']]

matcher.add("AGE_PATIENT", patient_age, greedy="LONGEST")
matcher.add("SAMPLE_SIZE", sample_size, greedy="LONGEST")


abstracts_w_id = []  # create a tupple of (abstract, id) to trace

for abstract,pubmed_id in zip(df.abstract,df.pubmed_id): 
    abstracts_w_id.append((abstract,pubmed_id))

df_match = {
    "pubmed_id": [],
    "score": [],
    "tag": [],
    "start": [],
    "end": []}


for doc, abstract_id in list(nlp.pipe(abstracts_w_id, as_tuples=True)):
    matches = matcher(doc)

    for match in matches:
        for pubmed_id, start, end in matches:

            string_id = nlp.vocab.strings[pubmed_id]
            span = doc[start:end]  # The matched span
            df_match["tag"].append(string_id)
            df_match["score"].append(span.text.replace('\n', ''))
            df_match["pubmed_id"].append(abstract_id)
            df_match["start"].append(start)
            df_match["end"].append(end)


df_match = pd.DataFrame(df_match)

df_match = df_match.drop_duplicates()

summary_dat = df_match[["pubmed_id", "score", "tag"]]
summary_dat = summary_dat.pivot_table(index= 'pubmed_id', columns= 'tag', values='score', aggfunc=list)
summary_dat.to_csv('saved_csv/matcher.csv', sep=';', encoding='UTF-8')


