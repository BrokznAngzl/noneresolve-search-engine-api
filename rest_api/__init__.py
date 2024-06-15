from database_connector import DatabaseConnector
from tfidf_service import TfidfService


def loadData():
    print('loading data...')
    db = DatabaseConnector()
    db.connect()
    sql = "SELECT `doc_id`, tokens ,mylinks.link'web' FROM `mytoken`, mylinks WHERE mytoken.doc_id = mylinks.id"
    data = db.execute_query(sql)
    db.close_connection()

    # docs = {'doc-token': [], 'web-link': []}
    for doc in data:
        text = doc[1].replace('\r', '').replace('\t', '').replace('|', ' ')
        link = doc[2]
        TfidfService.DOCS['doc-token'].append(text)
        TfidfService.DOCS['web-link'].append(link)

    TfidfService.setup_doc(TfidfService.DOCS['doc-token'])
    print('load data successfully')


loadData()
