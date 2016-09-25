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
  
  res = es.search(index = INDEX_NAME, size = 500, body={"query": {"match_all": {}}})
  json_res =  json.dumps(res, indent=2)
  
  return render_template("index.html", jsonResult = json_res)


@app.route('/search', methods=['POST'])
def search():
    req_json = request.get_json();   
    print req_json

    criteria_list = []
    if req_json["jobtitle"].strip():
       criteria = { "match": { "jobtitle": req_json["jobtitle"].strip() }}
       criteria_list.append(criteria)

    if req_json["company"].strip():
       criteria = { "match": { "company": req_json["company"].strip() }}
       criteria_list.append(criteria)

    if req_json["location"].strip():
       criteria = { "match": { "location": req_json["location"].strip() }}
       criteria_list.append(criteria)


    search_json = {'query': { "bool": {  "should": criteria_list } } }
    print search_json

    res = es.search(index="dashboard", doc_type="jobs", body={'query': { "bool": {  "should": criteria_list } } })
     
    return json.dumps({'status':'OK','req_json':req_json, 'resJSON':res});



