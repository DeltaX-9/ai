from elasticsearch import Elasticsearch
import json

es = Elasticsearch("http://localhost:9200")
mapping_data = json.load(open("map1.json", "r"))   
index_name = "scrapped_data"

es.indices.create(index=index_name, body=mapping_data, ignore=400)

sample_data = {
    "title": "Example Title",
    "source_url": "http://example.com",
    "contents": [
        {"content": "First version of content", "timestamp": "2023-01-01T12:00:00"},
        {"content": "Updated content", "timestamp": "2023-02-01T14:30:00"}
    ]
}


def insert_data(data):
    es.index(index=index_name, body=data)

def search_data(query):
    res = es.search(index=index_name, body=query)
    return res

insert_data(sample_data)
res = search_data({
    "query": {
        "match": {
            "source_url": "http://example.com"
        }
    }
})

print(res)

# print(es.info())

