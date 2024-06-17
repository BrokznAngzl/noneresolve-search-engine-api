from django.db import connection
from django.utils.deprecation import MiddlewareMixin

from tfidf_service import TfidfService


class InitiateRequestMiddleware(MiddlewareMixin):
    def __init__(self, get_response=None):
        super().__init__(get_response)
        try:
            print('loading data...')
            from rest_api.models import MyLinks, MyToken
            cursor = connection.cursor()
            cursor.execute(
                "SELECT `doc_id`, tokens ,mylinks.link'web', mylinks.title'title', mylinks.icon'icon', mylinks.body'body' FROM `mytoken`, mylinks WHERE mytoken.doc_id = mylinks.id")
            data = cursor.fetchall()
            cursor.close()

            for item in data:
                doc_id, link, title, icon, body = item[0], item[2], item[3], item[4], item[5]
                text = item[1].replace('\r', '').replace('\t', '').replace('|', ' ')

                TfidfService.DOCS['doc-id'].append(doc_id)
                TfidfService.DOCS['doc-token'].append(text)
                TfidfService.DOCS['doc-link'].append(link)
                TfidfService.DOCS['doc-title'].append(title)
                TfidfService.DOCS['doc-icon'].append(icon)
                TfidfService.DOCS['doc-body'].append(body)

            TfidfService.setup_doc(TfidfService.DOCS['doc-token'])
            print('load data successfully')

        except Exception as e:
            print(f'Error importing MyLink: {e}')

        self.get_response = get_response


def process_request(self, request):
    # This code will run when the server is started
    print("Middleware is running before any request or response.")
