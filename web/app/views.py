from app import app
from flask import render_template
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

  return render_template("index.html", jsonResult = jsonRes)


@app.route('/search', methods=['POST'])
def search():
    #user =  request.form['username'];
    #password = request.form['password'];

    req_json =  request.get_json();   
    return json.dumps({'status':'OK','req_json':req_json});