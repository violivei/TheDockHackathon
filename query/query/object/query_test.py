from elasticsearch import Elasticsearch
import json
import time
import openface

# Load face recognition models
align = openface.AlignDlib("{base_path}/models/shape_predictor_68_face_landmarks.dat".format(base_path=os.path.abspath(os.path.dirname(__file__))))
net = openface.TorchNeuralNet("{base_path}/models/nn4.small2.v1.t7".format(base_path=os.path.abspath(os.path.dirname(__file__))), 96, False)

# Elasticsearch host
es = Elasticsearch([{'host': 'localhost', 'port': 9200}])
# es = Elasticsearch(host='es')


body = {"from": "1", "to": "2", "face" : "ABC"}
# body = {"class": "motorbike", "from": "1", "to": "2"}

# t1 = 1486031766.241785
t1 = 1486031761.738631
t2 = time.time()




def filter_data(elastic_response, timefrom, timeto):
    filtered_response = []

    for image in elastic_response['hits']['hits']:
        if timefrom <= image['_source']['timestamp'] <= timeto:
            filtered_response.append(image)
    return filtered_response


def get_elastic_rep(res):
    rep = []
    align_face = []
    timestamp = []
    location = []
    for hit in res['hits']['hits']:
        if hit['_source']['timestamp'] - time.time() >= 0:
            continue
        rep.append(hit['_source']['face_rep'])
        align_face.append(hit['_source']['aligned_face'])
        timestamp.append(hit['_source']['timestamp'])
        location.append(hit['_source']['location'])
    return rep, align_face, timestamp, location





if __name__ == '__main__':
    if 'class' in body:
        response = es.search(index="obj", body={"query": {"bool": {"must": [{"match": {"classes.cat": body['class']}}]}}})
        response = filter_data(response, t1, t2)
        # print response

    elif 'face' in body:
        response = es.search(index="facial-recognition", body={"query": {"match_all": {}}})
        response = filter_data(response, t1, t2)
        # print get_elastic_rep(response)
        # print response

    else:
        print "An error occurred"





