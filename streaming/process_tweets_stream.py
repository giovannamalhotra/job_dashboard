#import sys, os

import os
from pyspark.sql import SQLContext
from pyspark import SparkContext, SparkConf
from pyspark.streaming import StreamingContext
from pyspark.streaming.kafka import KafkaUtils
from uuid import uuid1

import json


if __name__ == "__main__":
    sc = SparkContext(appName="streamingFromKafka")
    ssc = StreamingContext(sc, 2)   # every 2 seconds

    # topics = {'chicago': 1, 'nyc': 1}
    topics = {'tweetsFeed': 2}

    #kafka_machines = envir_vars.storage_cluster_ips
    #zkQuorum = ','.join([m + ':2181' for m in kafka_machines])
    zookeeperServ = 'ec2-52-89-43-209.us-west-2.compute.amazonaws.com:2181'

    kafkaStream = KafkaUtils.createStream(ssc, zookeeperServ, "GroupNameDoesntMatter", topics)
    #lines = kafkaStream.map(lambda x: x[1])
    #lines = kafkaStream.map(lambda x: json.loads(x[1]))
    lines = kafkaStream.map(lambda (k, v): json.loads(v))

    for x in kafkaStream.collect():
       print x


    ssc.start()
    ssc.awaitTermination()