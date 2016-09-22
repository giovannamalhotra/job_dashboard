import json
import pyspark
import os
from pyspark import SparkContext, SparkConf, StorageLevel
from pyspark.sql import SQLContext
from pyspark.sql.types import *
from elasticsearch import Elasticsearch

#----- Define constants --------

#Spark
#SPARK_MASTER = os.environ['SPARK_MASTER']
SPARK_MASTER = 'ec2-52-89-46-245.us-west-2.compute.amazonaws.com'

# Elasticsearch
#ES_NODES = os.environ['ES_NODES']
#ES_NODES = 'ec2-52-26-9-10.us-west-2.compute.amazonaws.com:9200'
ES_NODES = 'ec2-52-26-9-10.us-west-2.compute.amazonaws.com'
ES_INDEX = 'dashboard'
ES_TYPE = 'jobs'

print "ES_NODES:" + ES_NODES
print "SPARK_MASTER:" + SPARK_MASTER

es = Elasticsearch([{'host': ES_NODES}])

#Amazon S3
S3_BUCKET = 'giovanna-insight'


#result = es.search(index="dashboard", body={'query': {'match': {'jobtitle': 'data_engineering'}}})
#print json.dumps(result, indent=2)


def create_es_index():

   es_settings = {'number_of_shards':3, 'number_of_replicas': 2, 'refresh_interval': '1s', 'index.translog.flush_threshold_size': '1gb'}
   es_mapping = {"jobs ": {"properties": {"jobtitle ": { "type ": "string" }, "company ": { "type ": "string" }, "url ": { "type ": "string" }, "location ": { "type ": "string" },"date ": { "type ": "string"},"real ": { "type ": "string" }}}} 
   #return self.es.indices.create(index=ES_INDEX, body={'settings': es_settings, 'mappings': es_mapping}, ignore=400)
   response = es.indices.create(index=ES_INDEX, body={'settings': es_settings, 'mappings': es_mapping})


if __name__ == '__main__':

   print "****************** Result = TEST  **********************"   
   sc = SparkContext('spark://' + SPARK_MASTER + ':7077', 'jobs_batch')
   #sc = SparkContext("local", "Jobs batch App")
   sqlContext = SQLContext(sc)

   if not es.indices.exists(ES_INDEX):
      create_es_index()

   # folder on HDFS and Amazon S3 to pull the data from
   #val diceFile = "hdfs://ec2-52-89-46-245.us-west-2.compute.amazonaws.com:9000/camus/exec/history/2016-09-16*"
   #val diceFileS3 = "s3a://giovanna-insight/raw_logs/secor_backup/diceFeed/"
      

   # construct RDD[Sting]
   indeedStaticFile = '{"snippet": "The <b>data</b> science team is the core of 6sense <b>engineering</b>. Our <b>data</b> scientists are not optimizing software; We’re growing quickly and want to expand our <b>data</b>...", "city": "San Francisco", "state": "CA", "date": "Mon, 18 Jul 2016 05:47:44 GMT", "url": "http://www.indeed.com/viewjob?jk=231996de16f8c0a0&qd=w-2ovI1tcnsfYPwo0sLkH9zbhbnue5uotyVhKGbVyKMWZG2Qcqk4kcnEktztFnFoBz9U92JvRWUwZzl66iD44zxoxgsbBlaVUvGtwJ4oKEZSI4CmH9UzR8aTbSGPezp5qbUCPeLOQ7Dzs0cmDHOdgA&indpubnum=9693529091171604&atk=1astii41qburm805", "country": "US", "formattedLocation": "San Francisco, CA", "jobtitle": "Data Scientist", "company": "6sense", "formattedLocationFull": "San Francisco, CA"}'

   diceStaticFile = '{"date": "2016-09-09", "jobTitle": "Data and Application Engineering Manager", "company": "EPE Innovations", "location": "Dallas, TX", "detailUrl": "http://www.dice.com/job/result/90955654/637266?src=19"}' +   
   '{"date": "2016-09-09", "jobTitle": "Data and Application Engineering Manager", "company": "EPE Innovations", "location": "Dallas, TX", "detailUrl": "http://www.dice.com/job/result/90955654/637266?src=19"}'

   indeedDF = sqlContext.read.json(indeedStaticFile)
   diceDF = sqlContext.read.json(diceStaticFile)
