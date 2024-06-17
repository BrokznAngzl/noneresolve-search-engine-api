from database_connector import DatabaseConnector
from tfidf_service import TfidfService

# def loadData():
    # print('loading data...')
    # db = DatabaseConnector()
    # db.connect()
    # sql = "SELECT `doc_id`, tokens ,mylinks.link'web', mylinks.title'title', mylinks.icon'icon', mylinks.body'body' FROM `mytoken`, mylinks WHERE mytoken.doc_id = mylinks.id"
    # data = db.execute_query(sql)
    # db.close_connection()
    # model = Mylinks.objects.all()
    # serializer = MylinksSerializer(model, many=True)
    # data = serializer.data

    # for doc in data:
    #     doc_id, link, title, icon, body = doc[0], doc[2], doc[3], doc[4], doc[5]
    #     text = doc[1].replace('\r', '').replace('\t', '').replace('|', ' ')
    #
    #     TfidfService.DOCS['doc-id'].append(doc_id)
    #     TfidfService.DOCS['doc-token'].append(text)
    #     TfidfService.DOCS['doc-link'].append(link)
    #     TfidfService.DOCS['doc-title'].append(title)
    #     TfidfService.DOCS['doc-icon'].append(icon)
    #     TfidfService.DOCS['doc-body'].append(body)
    #
    # TfidfService.setup_doc(TfidfService.DOCS['doc-token'])
    # print('load data successfully')


# loadData()
