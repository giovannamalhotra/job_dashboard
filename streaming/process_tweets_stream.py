#import sys, os

import os
from pyspark.sql import SQLContext
from pyspark import SparkContext, SparkConf
from pyspark.streaming import StreamingContext
from pyspark.streaming.kafka import KafkaUtils
from uuid import uuid1
from elasticsearch import Elasticsearch

import json

companyList = []

# -------------------------------------------------------------
# --- Get company list from Database
# -------------------------------------------------------------
def getCompanies():
   # Get companies list and load it to memory
   INDEX_NAME = 'dashboard'
   TYPE_NAME = 'company'
   es = Elasticsearch(hosts = ['ec2-52-26-9-10.us-west-2.compute.amazonaws.com:9200','ec2-54-68-213-131.us-west-2.compute.amazonaws.com:9200','ec2-52-43-52-129.us-west-2.compute.amazonaws.com:9200'])

   res = es.search(index = INDEX_NAME, doc_type=TYPE_NAME, body={"query": {"match_all": {}}})
   jsonRes =  json.dumps(res, indent=2)
   print jsonRes

   for hit in res['hits']['hits']:
      companyList.append(hit["_source"]["company"])

   print companyList


# -------------------------------------------------------------
# --- Process RDD in each stream micro batch
# -------------------------------------------------------------
def processStreamRDD(rdd):
   # process each RDD from each micro batch      
   print 'Inside processStreamRDD method is empty for now...'



# -------------------------------------------------------------
# ----------------   MAIN  ------------------------------------
# -------------------------------------------------------------
if __name__ == "__main__":

    getCompanies()

    sc = SparkContext(appName="streamingFromKafka")
    ssc = StreamingContext(sc, 2)   # every 2 seconds

    # topics = {'chicago': 1, 'nyc': 1}
    #topics = {'tweetsFeed': 2}

    #kafka_machines = envir_vars.storage_cluster_ips
    #zkQuorum = ','.join([m + ':2181' for m in kafka_machines])
    #zookeeperServ = 'ec2-52-89-43-209.us-west-2.compute.amazonaws.com:2181'

    #kafkastream = KafkaUtils.createStream(ssc, zookeeperServ, "GroupNameDoesntMatter", topics)
    #lines = kafkaStream.map(lambda x: x[1])
    #lines = kafkaStream.map(lambda x: json.loads(x[1]))
    #lines = kafkaStream.map(lambda (k, v): json.loads(v))

    brokers = "ec2-50-112-19-115.us-west-2.compute.amazonaws.com:9092,ec2-52-33-162-7.us-west-2.compute.amazonaws.com:9092,ec2-52-89-43-209.us-west-2.compute.amazonaws.com:9092" 
    #kafkabrokers = {'metadata.broker.list' : 'ec2-50-112-19-115.us-west-2.compute.amazonaws.com:9092,ec2-52-33-162-7.us-west-2.compute.amazonaws.com:9092,ec2-52-89-43-209.us-west-2.compute.amazonaws.com:9092'}
    #hashablebrokers = frozenset(kafkabrokers.items())
    #kafkastream = KafkaUtils.createDirectStream(ssc, [topics], hashablebrokers)


    '''
    kafkastream = KafkaUtils.createDirectStream(ssc, ['tweetsFeed'], {"metadata.broker.list": brokers})

    lines = kafkastream.map(lambda x: x[1])
    linesRDDCollection = lines.flatMap(lambda line: line.split(" "))
    linesRDDCollection.foreachRDD(lambda rdd: processStreamRDD(rdd))
    '''
    
    


    ssc.start()
    ssc.awaitTermination()
