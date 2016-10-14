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
- Flask, Javascript and Bootstrap

<br/>
<br/>
Demo:
=========

The project is currently hosted at [Demo](http://ec2-50-112-150-148.us-west-2.compute.amazonaws.com/index). Below are screenshots of the Dashboard landing page created for this project.
<br/>
<br/>
![ ](https://github.com/giovannamalhotra/job_dashboard/blob/master/images/landing_page.png)
![ ](https://github.com/giovannamalhotra/job_dashboard/blob/master/images/search_results.png)

<br/>
<br/>
Pipeline:
=========

Below is the pipeline implemented for this project. 
<br/>

![ ](https://github.com/giovannamalhotra/job_dashboard/blob/master/images/pipeline.png)

<br/>
<br/>
Input Data:
==========================
The Input Data for this project consists of data from Indeed, Dice, and Tweets from Twitter.
Data from Indeed and Dice are collected in batch by calling their respective APIs. A Kafka producer was created to call Indeed and Dice APIs multiple times with different criteria, and ingest the data into Kafka.
Tweets from Twitter are collected in real time. A kafka producer calls Twitter API and ingests tweets into Kafka.


<br/>
Batch Layer:
==========================
Raw data from Indeed and Dice that was ingested into Kafka is then stored to Amazon S3 (using Secor) and processed by a batch program using Spark.
This batch program merges and deduplicates data before storing it in Elasticsearch. Job postings being processed in the batch program are compared to existing postings stored in the database to identify the ones that haven't being processed before. Once we have a final unique set of new job postings, that final is saved to Elasticsearch.


<br/>
Streaming Layer:
==========================
Tweets collected from Twitter might contain information about companies or might be about any other topic. The streaming program implemented using Spark filters the tweets that contain at least one of the companies we have jobs for.
The streaming program uses a master list of companies built by the batch job. When job postings are processed in the batch job, the batch job identifies what companies we have jobs for and save those companies into the database.
Then the streaming program compares each tweet content with the master listy of companies. If at least one company is found in the content, then the tweet is retained to be saved into the database.


<br/>
Web UI:
==========================
The web UI for the dashboard has been built using Flask. Javascript and Bootstrap was used for the front end, and python  
for the backend.
Users can search for jobs by job title, company and/or location.
When users click on search, the front end makes an ajax call to retrieve job postings and Tweets from Elasticsearch that match the criteria entered by the user. 
The front end displays information about the job posting, tweets for the specific company and also a link for the user to apply to the job.

<br/>
<br/>





