from django.views.decorators.csrf import csrf_exempt
from django.http import JsonResponse
from elasticsearch import Elasticsearch
import json


es = Elasticsearch([{'host': 'localhost', 'port': 9200}])
# es = Elasticsearch(host='es')


@csrf_exempt
def query_object(request):
    data = {}

    if request.method == "POST":
        body = json.loads(request.body)

        if 'class' in body:
            response = es.search(index="obj", body={"query": {"bool": {"must": [{"match": {"classes.cat": body['class']}}]}}})

        elif 'face' in body:
            response = es.search(index="facial-recognition", body={"query": {"match_all": {}}})

        else:
            data["error"] = "An error occurred"
            return JsonResponse(data)

        data.update(response)

    return JsonResponse(data)


def filter_data(t1, t2):

    return None



