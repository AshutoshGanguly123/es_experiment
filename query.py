import os
from datetime import datetime
from elasticsearch import Elasticsearch
from uuid import uuid4

#elastic search
es = Elasticsearch(
    ['https://localhost:9200'],
    http_auth=('elastic', 'CDYAZQqL5f=jN_u-Re+1'),
    verify_certs=False
)

#normal search
search_text = "Hey I am ashutosh, recently lost my job due to crisis of banks in US, I will pay in 5 months"
res = es.search(index="chat-index", body={"query": {"match": {"user_text": search_text}}})


# #similarity search
# similarity_search_text = "Hi, I am Michael. I was affected by the banking crisis too. I lost my job last month and have debts to pay. Can I defer my payments by nine months?"
# res = es.search(index="chat-index", body={
#     "query": {
#         "more_like_this" : {
#             "fields" : ["user_text"],
#             "like" : similarity_search_text,
#         }
#     }
# })

for hit in res['hits']['hits']:
    print(hit["_source"])
