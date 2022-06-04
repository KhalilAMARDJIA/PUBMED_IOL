import pandas as pd
import codecs

dat = pd.read_csv('saved_csv/pubmed_full.csv', sep=';')

matrix_filter= input('Enter the column to filter:  ', )

articles = dat[dat[matrix_filter] > 0]


titles = articles['title']
doi = articles['doi']
abstracts = articles['abstract']


tup = list(zip(doi, titles, abstracts))

file_name = f'{matrix_filter}.md'
file_path = f'filtred_text\{file_name}'


def md_report(doi, title, abstract):
    text = f"""
**{doi}** \n
{title} \n \n 
{abstract} \n \n 
"""
    return text
def report_filter ():
    with codecs.open(file_path, 'a', encoding='utf-8') as txt_file:
        for doi, title, abstract in tup:
            text = md_report(doi, title, abstract)
            txt_file .write(text)

if __name__ == "__main__":
    report_filter()