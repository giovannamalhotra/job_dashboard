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
#ES_TYPE = 'jobposting'
ES_TYPE = 'jobpost'
#ES_RESOURCE = 'dashboard/jobposting'
ES_RESOURCE = 'dashboard/jobpost'
es = Elasticsearch([{'host': ES_NODES}])

#Amazon S3
S3_BUCKET = 'giovanna-insight'

# Shema structure


feedStruct  = [StructField("jobtitle", StringType(), True),
        StructField("company", StringType(), True),
        StructField("url", StringType(), True),
        StructField("location", StringType(), True),
        StructField("snippet", StringType(), True),
        StructField("strday", IntegerType(), True),
        StructField("strmonth", IntegerType(), True),
        StructField("stryear", IntegerType(), True),
        StructField("creationdate", StringType(), True),
        StructField("origin", StringType(), True)]

'''
indeedStruct  = [StructField("city", StringType(), True),
        StructField("company", StringType(), True),
        StructField("country", StringType(), True),
        StructField("date", StringType(), True),
        StructField("expired", BooleanType(), True),
        StructField("formattedLocation", StringType(), True),
        StructField("formattedLocationFull", StringType(), True),
        StructField("formattedRelativeTime", StringType(), True),
        StructField("indeedApply", BooleanType(), True),
        StructField("jobkey", StringType(), True),
        StructField("jobtitle", StringType(), True),
        StructField("onmousedown", StringType(), True),
        StructField("snippet", StringType(), True),
        StructField("source", StringType(), True),
        StructField("sponsored", BooleanType(), True),
        StructField("state", StringType(), True),
        StructField("url", StringType(), True)]


diceStruct  = [StructField("company", StringType(), True),
        StructField("date", StringType(), True),
        StructField("detailUrl", StringType(), True),
        StructField("jobTitle", StringType(), True),
        StructField("location", StringType(), True)]
'''


#result = es.search(index="dashboard", body={'query': {'match': {'jobtitle': 'data_engineering'}}})
#print json.dumps(result, indent=2)


#def notFoundInJobsDB(row):
def notFoundInJobsDB(jobtitle, company, location):

    criteria_list = []
    criteria_list.append({ "match": { "jobtitle": jobtitle }})
    criteria_list.append({ "match": { "company": company }})
    criteria_list.append({ "match": { "location": location }})

    body = {"query": { "bool": {  "must": criteria_list } } }
    res = es.search(index = ES_INDEX, doc_type = ES_TYPE, size = 500, body = body)
    if res.length:
        return false
    else:
        return true    


def create_es_index():
   es_settings = {'number_of_shards':3, 'number_of_replicas': 2, 'refresh_interval': '1s', 'index.translog.flush_threshold_size': '1gb'}
   es_mapping = {"jobposting": {"properties": {"jobtitle": { "type": "string" }, "company": { "type": "string" }, "url": { "type": "string" }, "location": { "type": "string" }, "snippet": { "type": "string" }, "strday": {"type":"string"}, "strmonth": {"type":"string"}, "stryear": {"type":"string"}, "creationdate": { "type ": "string"}, "origin": { "type": "string" }}}} 
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
   indeedDF = sqlContext.read.json(indeedFileS3)
   diceDF = sqlContext.read.json(diceFileS3)

   indeedDF.printSchema()
   diceDF.printSchema()
   print indeedDF.rdd.take(1)
   print diceDF.rdd.take(1)


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
                                                          strday=str(datetime.strptime(row.date, dateFormat).day), \
                                                          strmonth=str(datetime.strptime(row.date, dateFormat).month), \
                                                          stryear=str(datetime.strptime(row.date, dateFormat).year), \
                                                          creationdate=str(datetime.strptime(row.date, dateFormat).day).zfill(2) + '-' + str(datetime.strptime(row.date, dateFormat).month).zfill(2) + '-' +  str(datetime.strptime(row.date, dateFormat).year), \
                                                          origin='Indeed'))

   print indeedRDD.take(1)
   #transformedIndeedDF = sqlContext.createDataFrame(indeedRDD, feedSchema).persist(StorageLevel.DISK_ONLY)
   transformedIndeedDF = sqlContext.createDataFrame(indeedRDD)

   diceRDD = diceDF.map(lambda row: pyspark.sql.Row(jobtitle=row.jobTitle, \
                                                          company=row.company, \
                                                          url=row.detailUrl, \
                                                          location=row.location, \
                                                          snippet='', \
                                                          strday=row.date[8:10], \
                                                          strmonth=row.date[5:7], \
                                                          stryear=row.date[0:4], \
                                                          creationdate=row.date[8:10] + '-' + row.date[5:7] + '-' + row.date[0:4], \
                                                          origin='Dice'))

   print diceRDD.take(1)

   #transformedDiceDF = sqlContext.createDataFrame(diceRDD, feedSchema).persist(StorageLevel.DISK_ONLY)
   transformedDiceDF = sqlContext.createDataFrame(diceRDD)

   print "--------------------------------transformedIndeedDF schema -------------------------------"
   transformedIndeedDF.printSchema()
   print "--------------------------------transformedDiceDF schema -------------------------------"
   transformedDiceDF.printSchema()
   print "--------------------------------indeed and Dice data -------------------------------"
   print transformedIndeedDF.rdd.take(1)
   print transformedDiceDF.rdd.take(1)

   

   transformedIndeedDF.registerTempTable("newIndeedTBL")
   transformedDiceDF.registerTempTable("newDiceTBL")

   # Join both DF contents
   combinedDF = sqlContext.sql("SELECT jobtitle, company, url, location, snippet, strday, strmonth, stryear, creationdate, origin FROM newDiceTBL UNION ALL SELECT jobtitle, company, url, location, snippet, strday, strmonth, stryear, creationdate, origin FROM newIndeedTBL")
   combinedDF.registerTempTable("combinedTBL")


   # Dedupe rows
   combinedDedupeDF = sqlContext.sql("SELECT jobtitle, company, location, first(url) as url, first(snippet) as snippet, first(strday) as strday, first(strmonth) as strmonth, first(stryear) as stryear, first(creationdate) as creationdate, first(origin) as origin FROM combinedTBL GROUP BY jobtitle, company, location")   

   combinedDedupeDF.printSchema() 
   print combinedDedupeDF.rdd.take(10)


   es_conf = {'es.nodes': ES_NODES, 'es.resource': ES_RESOURCE, 'es.port' : '9200',  'es.batch.write.retry.count': '-1', 'es.batch.size.bytes': '0.05mb'}


   finalRDD = combinedDedupeDF.rdd.map(lambda row: ('key', row.asDict()))
   #combinedDedupeRDD = combinedDedupeDF.filter(notFoundInJobsDB(combinedDedupeDF.jobtitle, combinedDedupeDF.company, combinedDedupeDF.location))
   #combinedDedupeDF = combinedDedupeDF.filter(notFoundInJobsDB(combinedDedupeDF.jobtitle, combinedDedupeDF.company, combinedDedupeDF.location))
   #finalRDD = combinedDedupeDF.rdd.map(lambda row: ('key', row.asDict()))

   print finalRDD.take(10)


   #finalRDD.saveAsNewAPIHadoopFile(path='-', \
   #                                         outputFormatClass='org.elasticsearch.hadoop.mr.EsOutputFormat', \
   #                                         keyClass='org.apache.hadoop.io.NullWritable', \
   #                                         valueClass='org.elasticsearch.hadoop.mr.LinkedMapWritable', \
   #                                         conf=es_conf)
 

   # Store distinct companies
   combinedDedupeDF.registerTempTable("dedupedTBL")
   companiesDF = sqlContext.sql("SELECT distinct company FROM dedupedTBL")   
   companiesRDD = companiesDF.rdd
   #filteredCompaniesRDD = companiesRDD.filter(lambda x: notFoundInDB(x))
   #filteredCompaniesRDD = filteredCompaniesRDD.rdd.map(lambda row: ('key', row.asDict()))

   #es_company_conf = {'es.nodes': ES_NODES, 'es.resource': 'dashboard/company', 'es.port' : '9200',  'es.batch.write.retry.count': '-1', 'es.batch.size.bytes': '0.05mb'}

   #filteredCompaniesRDD.saveAsNewAPIHadoopFile(path='-', \
   #                                         outputFormatClass='org.elasticsearch.hadoop.mr.EsOutputFormat', \
   #                                         keyClass='org.apache.hadoop.io.NullWritable', \
   #                                         valueClass='org.elasticsearch.hadoop.mr.LinkedMapWritable', \
   #                                         conf=es_company_conf)


