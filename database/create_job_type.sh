#!/usr/bin/env bash

# - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - — - - - - - - - - -
# Script to create job type for "dashboard" index in  Elasticsearch 
#
# - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - — - - - - - - - - -

curl -XPUT 'http://ec2-52-26-9-10.us-west-2.compute.amazonaws.com:9200/dashboard/_mapping/jobpost' -d '{ "jobpost": { "properties": {"jobtitle": { "type": "string" }, "company": { "type": "string" }, "url": { "type": "string" }, "location": { "type": "string" }, "snippet": { "type": "string" }, "strday": { "type": "string" }, "strmonth": { "type": "string"}, "stryear": { "type": "string"},  "creationdate": { "type": "String" }, "origin": { "type": "string" }}}}'

#curl http://ec2-52-26-9-10.us-west-2.compute.amazonaws.com:9200/_stats/indexes\?pretty\=1

curl -XGET 'http://ec2-52-26-9-10.us-west-2.compute.amazonaws.com:9200/dashboard/_mapping/jobpost'

