from app import app
from flask import render_template
from elasticsearch import Elasticsearch
import json

INDEX_NAME = 'dashboard'
TYPE_NAME = 'jobs'
es = Elasticsearch(hosts = 'ec2-52-26-9-10.us-west-2.compute.amazonaws.com')


#@app.route('/')
@app.route('/index')
#@app.route('/email')

def index():
  #return "Hello, World!"
  user = { 'nickname': 'Giovanna' } #fake user
  mylist = [1,2,3,4]
  #return render_template("index.html", title = 'Home', user = user, mylist = mylist)
  
  #res = es.search(index="dashboard", body={'query': {'match': {'description': 'CIA'}}})
  res = es.search(index = INDEX_NAME, size = 50, body={"query": {"match_all": {}}})
  jsonRes =  json.dumps(res, indent=2)

  return render_template("index.html", jsonResult = jsonRes)

def email():
  return render_template("base.html") 
