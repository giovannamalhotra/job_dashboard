#!/usr/bin/env bash

# - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - — - - - - - - - - -
# Script to create company type for "dashboard" index in  Elasticsearch 
#
# - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - — - - - - - - - - -

curl -XPOST 'http://ec2-52-26-9-10.us-west-2.compute.amazonaws.com:9200/dashboard/' -d '{"mapping": {"companytweet": {"properties": {"company": { "type":"string" }, "tweet": { "type":"string"}, "link": { "type":"string" }, "source": { "type":"string" }}}}}'

#curl http://ec2-52-26-9-10.us-west-2.compute.amazonaws.com:9200/_stats/indexes\?pretty\=1

curl -XGET 'http://ec2-52-26-9-10.us-west-2.compute.amazonaws.com:9200/dashboard/_mapping/companytweet'


curl -XPOST "http://ec2-52-26-9-10.us-west-2.compute.amazonaws.com:9200/dashboard/companytweet/t1" -d '{"company" : "LinkedIn", "tweet" : "Learning doesn\'t have to happen in the classroom.", "link": "https://t.co/07jcNIPNX1", "source": "Twitter" }'
#curl -XPOST "http://ec2-52-26-9-10.us-west-2.compute.amazonaws.com:9200/dashboard/companytweet/t2" -d '{"company" : "Facebook"}'
#curl -XPOST "http://ec2-52-26-9-10.us-west-2.compute.amazonaws.com:9200/dashboard/companytweet/t3" -d '{"company" : "Fitbit"}'
#curl -XPOST "http://ec2-52-26-9-10.us-west-2.compute.amazonaws.com:9200/dashboard/companytweet/t4" -d '{"company" : "Yelp"}'
#curl -XPOST "http://ec2-52-26-9-10.us-west-2.compute.amazonaws.com:9200/dashboard/companytweet/t5" -d '{"company" : "Slack"}'
#curl -XPOST "http://ec2-52-26-9-10.us-west-2.compute.amazonaws.com:9200/dashboard/companytweet/t6" -d '{"company" : "Twitter"}'
#curl -XPOST "http://ec2-52-26-9-10.us-west-2.compute.amazonaws.com:9200/dashboard/companytweet/t7" -d '{"company" : "Opendoor"}'
#curl -XPOST "http://ec2-52-26-9-10.us-west-2.compute.amazonaws.com:9200/dashboard/companytweet/t8" -d '{"company" : "Grand Rounds"}'
#curl -XPOST "http://ec2-52-26-9-10.us-west-2.compute.amazonaws.com:9200/dashboard/companytweet/t9" -d '{"company" : "Tamr"}'
#curl -XPOST "http://ec2-52-26-9-10.us-west-2.compute.amazonaws.com:9200/dashboard/companytweet/t10" -d '{"company" : "Casetext"}'
#curl -XPOST "http://ec2-52-26-9-10.us-west-2.compute.amazonaws.com:9200/dashboard/companytweet/t11" -d '{"company" : "Komodo Heath"}'
#curl -XPOST "http://ec2-52-26-9-10.us-west-2.compute.amazonaws.com:9200/dashboard/companytweet/t12" -d '{"company" : "6sense"}'
#curl -XPOST "http://ec2-52-26-9-10.us-west-2.compute.amazonaws.com:9200/dashboard/companytweet/t13" -d '{"company" : "Spire"}'
#curl -XPOST "http://ec2-52-26-9-10.us-west-2.compute.amazonaws.com:9200/dashboard/companytweet/t14" -d '{"company" : "Zenysis"}'
#curl -XPOST "http://ec2-52-26-9-10.us-west-2.compute.amazonaws.com:9200/dashboard/companytweet/t15" -d '{"company" : "Domino Data Labs"}'
#curl -XPOST "http://ec2-52-26-9-10.us-west-2.compute.amazonaws.com:9200/dashboard/companytweet/t16" -d '{"company" : "The Voleon Group"}'
#curl -XPOST "http://ec2-52-26-9-10.us-west-2.compute.amazonaws.com:9200/dashboard/companytweet/t17" -d '{"company" : "Tophatter"}'
#curl -XPOST "http://ec2-52-26-9-10.us-west-2.compute.amazonaws.com:9200/dashboard/companytweet/t18" -d '{"company" : "Microsoft"}'
#curl -XPOST "http://ec2-52-26-9-10.us-west-2.compute.amazonaws.com:9200/dashboard/companytweet/t19" -d '{"company" : "Oracle"}'
#curl -XPOST "http://ec2-52-26-9-10.us-west-2.compute.amazonaws.com:9200/dashboard/companytweet/t20" -d '{"company" : "Apple"}'
#curl -XPOST "http://ec2-52-26-9-10.us-west-2.compute.amazonaws.com:9200/dashboard/companytweet/t21" -d '{"company" : "Google"}'
#curl -XPOST "http://ec2-52-26-9-10.us-west-2.compute.amazonaws.com:9200/dashboard/companytweet/t22" -d '{"company" : "Accenture"}'
#curl -XPOST "http://ec2-52-26-9-10.us-west-2.compute.amazonaws.com:9200/dashboard/companytweet/t23" -d '{"company" : "Yahoo"}'
#curl -XPOST "http://ec2-52-26-9-10.us-west-2.compute.amazonaws.com:9200/dashboard/companytweet/t24" -d '{"company" : "Cisco"}'

curl -XGET 'http://ec2-52-26-9-10.us-west-2.compute.amazonaws.com:9200/dashboard/companytweet/t24'
