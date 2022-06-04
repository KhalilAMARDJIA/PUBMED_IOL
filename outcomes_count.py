import json
import pandas as pd
import re
import plotly.express as px


# fetch data from PubMed
pubmed_raw_data = pd.read_csv('pubmed_raw_data.csv', sep=";")

# open scores database
with open('./databases/scores_db.json') as file:
    scores_db = json.load(file)

# check if scores are present in the abstracts

clinical_outcomes = []
scores = []

score_matrix = pd.DataFrame()
for clinical_outcome in scores_db['Clinical outcomes']:
    for score in scores_db['Clinical outcomes'][clinical_outcome]:
        clinical_outcomes.append(clinical_outcome)
        scores.append(score)
        for syn in scores_db['Clinical outcomes'][clinical_outcome][score]:
            search_or_syno = '|'.join(
                 scores_db['Clinical outcomes'][clinical_outcome][score])
            try:
                search_or_syno = search_or_syno.replace("(", "\(")
                search_or_syno = search_or_syno.replace(")", "\)")

                score_matrix[score] = pubmed_raw_data.abstract.str.count(search_or_syno, flags = re.IGNORECASE)
            except:
                pass

for col in score_matrix.columns:
    score_matrix.loc[score_matrix[col] > 0, col] = 1

# before transpose joint final output csv
score_matrix.to_csv("./saved_csv/matrix_score.csv", sep = ';')


# ploting

score_matrix = score_matrix.transpose()

body_map = dict(zip(scores, clinical_outcomes)) # create map from 2 list as dict

score_matrix_plot = score_matrix.sum(axis=1).reset_index()
score_matrix_plot['Clinical outcomes'] = score_matrix_plot['index'].map(body_map)
score_matrix_plot = score_matrix_plot.rename(columns={'index': 'score', 0:'n'})
score_matrix_plot = score_matrix_plot.sort_values(['Clinical outcomes','n'])
score_matrix_plot = score_matrix_plot[score_matrix_plot.n >0]

fig = px.bar(
    template = 'simple_white',
    x = 'n', 
    y = 'score',
    color=  'Clinical outcomes',
    color_discrete_sequence=px.colors.diverging.curl,
    data_frame=score_matrix_plot,
    title=f'PubMed data extracted from {len(pubmed_raw_data)} abstracts'
    )

fig.update_traces(marker_line_color='black',marker_line_width=1)
fig.update_layout(font_family="JetBrainsMono NF")

fig.write_html("./plots/clinical_outcomes.html", auto_open=True)