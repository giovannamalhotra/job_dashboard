Overview:
=========

Job Search Datashboard is a data platform implemented for the Insight Data Engineering Fellowship program (Fall 2016). 
It uses the following technologies:

- Kafka
- Secor
- Amazon S3
- Spark batch
- Spark Streaming
- ElasticSearch
- Flask, javascript and bootstrap


Website:
=========

The project is currently hosted at [Demo](http://ec2-50-112-150-148.us-west-2.compute.amazonaws.com/index)
<br/>
<br/>
![ ](https://github.com/giovannamalhotra/job_dashboard/blob/master/images/landing_page.png)
![ ](https://github.com/giovannamalhotra/job_dashboard/blob/master/images/search_results.png)
<br/>
<br/>

Pipeline:
=========

Below is the pipeline implemented for this project. 

![ ](https://github.com/giovannamalhotra/job_dashboard/blob/master/images/pipeline.png)

<br/>
<br/>

1. Batch data is pulled from Dice and Indeed by calling their public APis and ingested to Kafka to different topics: "diceFeed" and "indeedFeed".
2. Tweets are pulled from Twitter in real time and ingested to Kafka to "tweetsFeed" topic.
3. Raw data from Dice and Indeed are saved from Kafka to Amazon S3 by using Secor.
4. Spark batch Program processes, merges and deduplicates data from Indeed and Dice and saves only new job postings to Elasticsearch.
5. Spark Streaming reads and filters tweets from kafka. Only tweets about any of the companies identified from the job postings are saved to Elasticsearch.
6. The Web UI built in Flask pulls job postings and tweets from Elasticsearch and displays them on the dashboard. 

<br/>
<br/>





