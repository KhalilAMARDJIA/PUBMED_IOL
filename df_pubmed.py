import pandas as pd
from pymed import PubMed

pubmed = PubMed(tool="PubMedSearcher", email="khalil.amardjia@gmail.com")


def df_pubmed(query):

    search_term = query

    results = pubmed.query(search_term, max_results=20000)
    articleList = []
    articleInfo = []

    for article in results:
        articleDict = article.toDict()
        articleList.append(articleDict)
    try:
        for article in articleList:
            pubmedId = article['pubmed_id'].partition('\n')[0]
            articleInfo.append({
                u'pubmed_id': pubmedId,
                u'title': article['title'],
                u'keywords': article['keywords'],
                u'journal': article['journal'],
                u'abstract': article['abstract'],
                u'conclusions': article['conclusions'],
                u'methods': article['methods'],
                u'results': article['results'],
                u'copyrights': article['copyrights'],
                u'doi': article['doi'],
                u'publication_date': article['publication_date'],
                u'authors': article['authors']
            })
    except:
        pass
    articlesPD = pd.DataFrame.from_dict(articleInfo)
    return articlesPD
