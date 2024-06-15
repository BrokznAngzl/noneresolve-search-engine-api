from django.http import JsonResponse
from tfidf_service import TfidfService


def index(request):

    query_result = []
    if request.method == "GET":
        query = request.GET.get('query')

        if query == 'ไอ้แก่':
            query = 'cis'

        print('finding in query in docs...')
        query_result = TfidfService.search(query, 10, TfidfService.DOCS)

    response = {
        'data': query_result
    }

    return JsonResponse(response, status=200)
