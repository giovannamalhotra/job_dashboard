from app import app
from flask import render_template, request, jsonify
from elasticsearch import Elasticsearch
import json

INDEX_NAME = 'dashboard'
TYPE_NAME = 'jobs'
#es = Elasticsearch(hosts = 'ec2-52-26-9-10.us-west-2.compute.amazonaws.com')
es = Elasticsearch(hosts = ['ec2-52-26-9-10.us-west-2.compute.amazonaws.com:9200','ec2-54-68-213-131.us-west-2.compute.amazonaws.com:9200','ec2-52-43-52-129.us-west-2.compute.amazonaws.com:9200'])

#@app.route('/')
@app.route('/index')
def index():
  #user = { 'nickname': 'Giovanna' } #fake user
  #mylist = [1,2,3,4]
  #return render_template("index.html", title = 'Home', user = user, mylist = mylist)
  
  #res = es.search(index="dashboard", body={'query': {'match': {'description': 'CIA'}}})
  #res = es.search(index = INDEX_NAME, size = 50, body={"query": {"match_all": {}}})
  res = es.search(index = INDEX_NAME, size = 500, body={"query": {"match_all": {}}})
  jsonRes =  json.dumps(res, indent=2)
  
  resultList = []
  for hit in res['hits']['hits']:
    #resultList.append(json.dumps(hit["_source"]))
    jsonStr = {'url': hit["_source"]["url"], 'jobtitle': hit["_source"]["jobtitle"], 'company': hit["_source"]["company"], 'location': hit["_source"]["location"]}
    print "jsonStr:" + str(jsonStr)
    resultList.append(json.dumps(str(jsonStr))) 


  return render_template("index.html", jsonResult = jsonRes, resultList = resultList)
  #return render_template("index.html", jsonResult = jsonify(jsonRes))


@app.route('/search', methods=['POST'])
def search():
    req_json = request.get_json();   
    return json.dumps({'status':'OK','req_json':req_json});
