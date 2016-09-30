#import sys, os

import os
import pyspark
from pyspark.sql import SQLContext
from pyspark import SparkContext, SparkConf
from pyspark.streaming import StreamingContext
from pyspark.streaming.kafka import KafkaUtils
from uuid import uuid1
from elasticsearch import Elasticsearch, helpers
import pprint
import json

companyList = []

# Set Elasticsearch configuration to save tweets
ES_WRITE_NODES = 'ec2-52-26-9-10.us-west-2.compute.amazonaws.com'
ES_WRITE_INDEX = 'dashboard'
ES_WRITE_TYPE = 'tweets'
ES_WRITE_RESOURCE = 'dashboard/jobs'
es_tweets = Elasticsearch([{'host': ES_WRITE_NODES}])

# Set Elasticsearch configuration to get list of companies
ES_COMPANY_INDEX = 'dashboard'
ES_COMPANY_TYPE = 'company'
es_company = Elasticsearch(hosts = ['ec2-52-26-9-10.us-west-2.compute.amazonaws.com:9200','ec2-54-68-213-131.us-west-2.compute.amazonaws.com:9200','ec2-52-43-52-129.us-west-2.compute.amazonaws.com:9200'])



# -------------------------------------------------------------
# --- Get company list from Database
# -------------------------------------------------------------
def getCompanies():

   # Get companies list and load it to memory
   #res = es_company.search(index = ES_COMPANY_INDEX, doc_type=ES_COMPANY_TYPE, body={"query": {"match_all": {}}})
   #
   #companyList1 = []
   #for hit in res['hits']['hits']:
   #  companyList1.append(hit["_source"]["company"])
   #print companyList1


   page = es_company.search(
     index = ES_COMPANY_INDEX,
     doc_type = ES_COMPANY_TYPE,
     scroll = '2m',
     search_type = 'scan',
     #size = 1000,
     body = {
          # Query's body
          "query": {"match_all": {}} 
     })
   sid = page['_scroll_id']
   scroll_size = page['hits']['total']
  
   # Start scrolling
   while (scroll_size > 0):
     print "Scrolling..."
     page = es_company.scroll(scroll_id = sid, scroll = '2m')
     # Update the scroll ID
     sid = page['_scroll_id']
     # Get the number of results that we returned in the last scroll
     scroll_size = len(page['hits']['hits'])
     #print "scroll size: " + str(scroll_size)
     
     for hit in page['hits']['hits']:
       companyList.append(hit["_source"]["company"])

   print companyList


# -------------------------------------------------------------
# --- Process RDD in each stream micro batch
# -------------------------------------------------------------
def processStreamRDD(rdd):
   # process each RDD from each micro batch      
   print 'Inside processStreamRDD method is empty for now...'
   #print rdd.take(5)
  
   # !!!!!!! Read tweets from each RDD and extract only "text". Create a new RDD with only tweet text
   #tweetsRDD = rdd.map(lambda row: pyspark.sql.Row(tweet=row.text))
   tweetsList = rdd.collect()                                                
   
   print '-------------------------- tweetsList ---------------------------------'
   #tweetsList.pprint() 
   print tweetsList

   es_conf = {'es.nodes': ES_WRITE_NODES, 'es.resource': ES_WRITE_RESOURCE, 'es.port' : '9200',  'es.batch.write.retry.count': '-1', 'es.batch.size.bytes': '0.05mb'}

   #finalRDD.saveAsNewAPIHadoopFile(path='-', \
   #                                         outputFormatClass='org.elasticsearch.hadoop.mr.EsOutputFormat', \
   #                                         keyClass='org.apache.hadoop.io.NullWritable', \
   #                                         valueClass='org.elasticsearch.hadoop.mr.LinkedMapWritable', \
   #                                         conf=es_conf)


# -------------------------------------------------------------
# ----------------   MAIN  ------------------------------------
# -------------------------------------------------------------
if __name__ == "__main__":

    # Load companies
    getCompanies()

    # Set Spark Streaming 
    sc = SparkContext(appName="streamingFromKafka")
    ssc = StreamingContext(sc, 10)   # every 2 seconds

    #kafka_machines = envir_vars.storage_cluster_ips
    #zkQuorum = ','.join([m + ':2181' for m in kafka_machines])
    #zookeeperServ = 'ec2-52-89-43-209.us-west-2.compute.amazonaws.com:2181'

    #kafkastream = KafkaUtils.createStream(ssc, zookeeperServ, "GroupNameDoesntMatter", topics)
    #lines = kafkaStream.map(lambda x: x[1])
    #lines = kafkaStream.map(lambda x: json.loads(x[1]))
    #lines = kafkaStream.map(lambda (k, v): json.loads(v))

    brokers = "ec2-50-112-19-115.us-west-2.compute.amazonaws.com:9092,ec2-52-33-162-7.us-west-2.compute.amazonaws.com:9092,ec2-52-89-43-209.us-west-2.compute.amazonaws.com:9092" 
     

    kafka_stream = KafkaUtils.createDirectStream(ssc, ['tweetsFeed'], {"metadata.broker.list": brokers})
    print '--------------------- Printing kafkastream content --------------------------------'
    kafka_stream.pprint()
    print '--------------------- End of kafkastream content -----------------------------------'

    #lines = kafka_stream.map(lambda x: x[1])  #Twitter message is in second object of the kafka stream response 
    #streamRDDCollection = lines.flatMap(lambda line: line.split(" ")) 

    tweets_stream  = kafka_stream.map(lambda x: json.loads(x[1])) #Twitter message are in second object of the kafka stream response
    #tweets_stream  = tweets_stream.filter(lambda x: 'text' in x)
    #tweets_stream  = tweets_stream.map(lambda x: x['text'])
    tweets_stream  = tweets_stream.map(lambda x: x['text'].encode("utf-8","replace"))
    #streamRDDCollection = tweets_stream.flatMap(lambda x: x.split(" "))
    streamRDDCollection = tweets_stream

    print '--------------------- Printing streamRDDCollection ------------------------------- '
    streamRDDCollection.pprint()
    print '--------------------- End of  streamRDDCollection -------------------------------- '

    streamRDDCollection.foreachRDD(lambda rdd: processStreamRDD(rdd))

    ssc.start()
    ssc.awaitTermination()
