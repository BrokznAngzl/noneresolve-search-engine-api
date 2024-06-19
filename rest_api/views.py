from django.http import JsonResponse
from rest_framework.decorators import api_view
# from .models import MyLinks
from tfidf_service import TfidfService


@api_view(['GET'])
def index(request):
    query = request.GET.get('query')
    print('finding in query in docs...')
    query_result = TfidfService.search(query, 10, TfidfService.DOCS)

    response = {
        'data': query_result
    }

    return JsonResponse(response, status=200)
