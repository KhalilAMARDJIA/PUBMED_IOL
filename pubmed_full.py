import re
import os
import pandas as pd
from os.path import exists

files = [f for f in os.listdir('./saved_csv') if re.match(r'matrix_', f)]

matrixes = []

for matrix in files:
    df_matrix = pd.read_csv(
        f'./saved_csv/{matrix}', sep=';', index_col=0).transpose()
    matrixes.append(df_matrix)

matrix_all = pd.concat(matrixes)

pubmed_raw_data = pd.read_csv('./saved_csv/pubmed_raw_data.csv', sep=';')

pubmed_full = pd.concat(
    [pubmed_raw_data, matrix_all.transpose()], axis=1, join="inner")

pubmed_full = pubmed_full[pubmed_full.columns.drop(list(pubmed_full.filter(regex='Unnamed')))]



matcher_data = pd.read_csv('./saved_csv/matcher.csv', sep=';')
pubmed_full = pd.merge(pubmed_full, matcher_data, on= "pubmed_id")

ner_path = "./saved_csv/ner_data.csv"
file_exists = exists(ner_path)
if file_exists:
    ner_data = pd.read_csv(ner_path, sep = ";")
    pubmed_full = pd.merge(pubmed_full, ner_data, on= "pubmed_id")
else:
    pass


pubmed_full.to_csv('./saved_csv/pubmed_full.csv', sep=';')
