from df_pubmed import df_pubmed

query = input('please enter your PubMed query here: ')

pubmed_raw_data = df_pubmed(query)
pubmed_raw_data = pubmed_raw_data.dropna(subset=['title', 'abstract'])
pubmed_raw_data.to_csv('pubmed_raw_data.csv', sep = ';')
pubmed_raw_data.to_csv('./saved_csv/pubmed_raw_data.csv', sep = ';')