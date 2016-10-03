from app import app
from flask import render_template, request, jsonify
from elasticsearch import Elasticsearch
import json

INDEX_NAME = 'dashboard'
TYPE_NAME = 'jobposting'
#es = Elasticsearch(hosts = 'ec2-52-26-9-10.us-west-2.compute.amazonaws.com')
es = Elasticsearch(hosts = ['ec2-52-26-9-10.us-west-2.compute.amazonaws.com:9200','ec2-54-68-213-131.us-west-2.compute.amazonaws.com:9200','ec2-52-43-52-129.us-west-2.compute.amazonaws.com:9200'])

#@app.route('/')
@app.route('/index')
def index():
  
  res = es.search(index = INDEX_NAME, doc_type = TYPE_NAME, size = 500, body={"query": {"match_all": {}}})
  json_res =  json.dumps(res, indent=2)

  res_tweets = es.search(index = INDEX_NAME, doc_type = "companytweet", size = 500, body={"query": {"match_all": {}}})
  json_tweets = json.dumps(res_tweets, indent=2)  

  return render_template("index.html", res_jobs_json = json_res, res_tweets_json = json_tweets)


@app.route('/search', methods=['POST'])
def search():
    req_json = request.get_json();   
    print req_json

    if not req_json["jobtitle"].strip() and not req_json["company"].strip() and not req_json["location"].strip():
       #res = es.search(index = INDEX_NAME, doc_type = TYPE_NAME,  size = 500, body={"query": {"match_all": {}}})
       body = '{"query": {"match_all": {}}}'

    else: 

        criteria_list = []

        #if req_json["jobtitle"].strip():
        #    criteria = { "match": { "jobtitle": req_json["jobtitle"].strip() }}
        #    criteria_list.append(criteria)

        #if req_json["company"].strip():
        #    criteria = { "match": { "company": req_json["company"].strip() }}
        #    criteria_list.append(criteria)

        #if req_json["location"].strip():
        #    criteria = { "match": { "location": req_json["location"].strip() }}
        #    criteria_list.append(criteria)


        # Trim input field content
        jobtitle_input = req_json["jobtitle"].strip()
        company_input = req_json["company"].strip()
        location_input = req_json["location"].strip()

        if jobtitle_input:
            jobtitle_words = jobtitle_input.split(' ')
            for word in jobtitle_words:
              criteria = { "match": { "jobtitle": word }}
              criteria_list.append(criteria)

        if company_input:
            company_words = company_input.split(' ')
            for word in company_words:
              criteria = { "match": { "company": word }}
              criteria_list.append(criteria)

        if location_input:
            location_words = location_input.split(' ')
            for word in location_words:
              criteria = { "match": { "location": word }}
              criteria_list.append(criteria)


        #res = es.search(index = INDEX_NAME, doc_type = TYPE_NAME, body={"query": { "bool": {  "should": criteria_list } } })
        #body = {"query": { "bool": {  "should": criteria_list } } }
        body = {"query": { "bool": {  "must": criteria_list } } }
        print body

    res = es.search(index = INDEX_NAME, doc_type = TYPE_NAME, size = 500, body = body)

    tweets_query = '{"query": {"match_all": {}}}'
    res_tweets = es.search(index = INDEX_NAME, doc_type = "companytweet", size = 500, body = tweets_query)

 
    #return json.dumps({'status':'OK','req_json':req_json, 'resJSON':res});
    return json.dumps({'status':'OK','req_json':req_json, 'res_jobs_json':res['hits']['hits'], 'res_tweets_json': res_tweets['hits']['hits'] });





