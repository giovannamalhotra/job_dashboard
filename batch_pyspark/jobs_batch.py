import json
import pyspark
import os
from pyspark import SparkContext, SparkConf, StorageLevel
from pyspark.sql import SQLContext
from pyspark.sql.types import *
from elasticsearch import Elasticsearch
from datetime import datetime

#----------------------- Define constants ----------------------------#

#Spark
#SPARK_MASTER = os.environ['SPARK_MASTER']
SPARK_MASTER = 'ec2-52-89-46-245.us-west-2.compute.amazonaws.com'

# Elasticsearch
#ES_NODES = os.environ['ES_NODES']
#ES_NODES = 'ec2-52-26-9-10.us-west-2.compute.amazonaws.com:9200'

ES_NODES = 'ec2-52-26-9-10.us-west-2.compute.amazonaws.com'
#ES_NODES = ['ec2-52-26-9-10.us-west-2.compute.amazonaws.com:9200','ec2-54-68-213-131.us-west-2.compute.amazonaws.com:9200','ec2-52-43-52-129.us-west-2.compute.amazonaws.com:9200'])
#ES_NODES = 'ec2-52-26-9-10.us-west-2.compute.amazonaws.com,ec2-54-68-213-131.us-west-2.compute.amazonaws.com,ec2-52-43-52-129.us-west-2.compute.amazonaws.com'


ES_INDEX = 'dashboard'
ES_TYPE = 'job'
ES_RESOURCE = 'dashboard/job'
es = Elasticsearch([{'host': ES_NODES}])

#Amazon S3
S3_BUCKET = 'giovanna-insight'

# Shema structure
feedStruct  = [StructField("jobtitle", StringType(), True),
        StructField("company", StringType(), True),
        StructField("url", StringType(), True),
        StructField("location", StringType(), True),
        StructField("snippet", StringType(), True),
        StructField("day", LongType(), True),
        StructField("month", LongType(), True),
        StructField("year", LongType(), True),
        StructField("date", StringType(), True),
        #StructField("id", StringType(), True),
        StructField("origin", StringType(), True)]

#result = es.search(index="dashboard", body={'query': {'match': {'jobtitle': 'data_engineering'}}})
#print json.dumps(result, indent=2)

def create_es_index():
   es_settings = {'number_of_shards':3, 'number_of_replicas': 2, 'refresh_interval': '1s', 'index.translog.flush_threshold_size': '1gb'}
   es_mapping = {"job ": {"properties": {"jobtitle": { "type": "string" }, "company": { "type": "string" }, "url ": { "type": "string" }, "location": { "type": "string" }, "snippet": { "type": "string" }, "day ":{"type":"integer"}, "month ":{"type":"integer"}, "year ":{"type":"integer"}, "date": { "type ": "string"}, "origin": { "type ": "string" }}}} 
   #return self.es.indices.create(index=ES_INDEX, body={'settings': es_settings, 'mappings': es_mapping}, ignore=400)
   response = es.indices.create(index=ES_INDEX, body={'settings': es_settings, 'mappings': es_mapping})



if __name__ == '__main__':

   print "****************** Result = TEST  **********************"   
   #sc = SparkContext("local", "Jobs batch App")
   sc = SparkContext('spark://' + SPARK_MASTER + ':7077', 'jobs_batch')
   sqlContext = SQLContext(sc)

   if not es.indices.exists(ES_INDEX):
      create_es_index()

   # folder on HDFS and Amazon S3 to pull the data from
   #val diceFile = "hdfs://ec2-52-89-46-245.us-west-2.compute.amazonaws.com:9000/camus/exec/history/2016-09-16*"
   indeedFileS3 = "s3a://giovanna-insight/raw_logs/secor_backup/indeedFeed/*"
   diceFileS3 = "s3a://giovanna-insight/raw_logs/secor_backup/diceFeed/*"
       
   # construct RDD[Sting]
   #indeedStaticFile = 'json1.json'
   #diceStaticFile = 'json2.json'

   indeedDF = sqlContext.read.json(indeedFileS3)
   diceDF = sqlContext.read.json(diceFileS3)

   indeedDF.printSchema()
   diceDF.printSchema()

   # Transform data to extract only the elements that are needed
   feedSchema = StructType(feedStruct)
   dateFormat = "%a, %d %b %Y %H:%M:%S %Z"
 
   indeedRDD = indeedDF.map(lambda row: pyspark.sql.Row(jobtitle=row.jobtitle, \
                                                          company=row.company, \
                                                          url=row.url, \
                                                          location=row.formattedLocation, \
                                                          snippet=row.snippet, \
                                                          #day=datetime.utcfromtimestamp(float(row.date)).day, \
                                                          #month=datetime.utcfromtimestamp(float(row.date)).month, \
                                                          #year=datetime.utcfromtimestamp(float(row.created_utc)).year, \
                                                          day=datetime.strptime(row.date, dateFormat).day, \
                                                          month=datetime.strptime(row.date, dateFormat).month, \
                                                          year=datetime.strptime(row.date, dateFormat).year, \
                                                          date=str(datetime.strptime(row.date, dateFormat).day).zfill(2) + ' - ' + str(datetime.strptime(row.date, dateFormat).month).zfill(2) + str(datetime.strptime(row.date, dateFormat).year), \
                                                          origin='Indeed'))
   transformedIndeedDF = sqlContext.createDataFrame(indeedRDD, feedSchema).persist(StorageLevel.DISK_ONLY)


   diceRDD = diceDF.map(lambda row: pyspark.sql.Row(jobtitle=row.jobTitle, \
                                                          company=row.company, \
                                                          url=row.detailUrl, \
                                                          location=row.location, \
                                                          snippet='', \
                                                          day=row.date[8:10], \
                                                          month=row.date[5:7], \
                                                          year=row.date[0:4], \
                                                          date=row.date[8:10] + ' - ' + row.date[5:7] + ' - ' + row.date[0:4]
                                                          origin='Dice'))

   transformedDiceDF = sqlContext.createDataFrame(diceRDD, feedSchema).persist(StorageLevel.DISK_ONLY)


   print "--------------------------------filteredIndeedDF schema -------------------------------"
   transformedIndeedDF.printSchema()
   print "--------------------------------filteredDiceDF schema -------------------------------"
   transformedDiceDF.printSchema()
   print "--------------------------------indeed and Dice data -------------------------------"
   transformedIndeedDF.show
   transformedDiceDF.show


   transformedIndeedDF.registerTempTable("newIndeedTBL")
   transformedDiceDF.registerTempTable("newDiceTBL")

   # Join both DF contents
   #combinedDF = sqlContext.sql("SELECT jobtitle, company, url, location, date, snippet FROM newDiceTBL UNION ALL SELECT jobtitle, company, url, location, date, snippet FROM newIndeedTBL")
   #combinedDF = sqlContext.sql("SELECT jobtitle, company, url, location, snippet, day, month, year, real,  FROM newDiceTBL UNION ALL SELECT jobtitle, company, url, location, snippet, day, month, year, real FROM newIndeedTBL")
   combinedDF = sqlContext.sql("SELECT * FROM newDiceTBL UNION ALL SELECT * FROM newIndeedTBL")
   combinedDF.registerTempTable("combinedTBL")

   # Dedup rows
   combinedDedupDF = sqlContext.sql("SELECT jobtitle, company, location, first(url) as url, first(snippet) as snippet, first(day) as day, first(month) as month, first(year) as year, first(date) as date, first(origin) as origin FROM combinedTBL GROUP BY jobtitle, company, location")   

   combinedDedupDF.printSchema() 
   #finalRDD = combinedDedupDF.rdd
   #finalRDD.take(10)

   es_conf = {'es.nodes': ES_NODES, 'es.resource': ES_RESOURCE, 'es.port' : '9200',  'es.batch.write.retry.count': '-1', 'es.batch.size.bytes': '0.05mb'}


   finalRDD = combinedDedupDF.map(lambda row: ('key', row.asDict()))
   finalRDD.saveAsNewAPIHadoopFile(path='-', \
                                            outputFormatClass='org.elasticsearch.hadoop.mr.EsOutputFormat', \
                                            keyClass='org.apache.hadoop.io.NullWritable', \
                                            valueClass='org.elasticsearch.hadoop.mr.LinkedMapWritable', \
                                            conf=es_conf)


   #combinedDedupDF.rdd.saveToEs("dashboard/jobs")
   #finalRDD = combinedDedupDF.rdd
