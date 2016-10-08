#!/usr/bin/env bash

# - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - — - - - - - - - - -
# Script to create company type for "dashboard" index in  Elasticsearch 
#
# - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - — - - - - - - - - -

#curl -XPOST 'http://ec2-52-26-9-10.us-west-2.compute.amazonaws.com:9200/dashboard/_mapping/company' -d '{"company ": {"properties": {"company": { "type ": "string" }}}}'

#curl http://ec2-52-26-9-10.us-west-2.compute.amazonaws.com:9200/_stats/indexes\?pretty\=1

curl -XGET 'http://ec2-52-26-9-10.us-west-2.compute.amazonaws.com:9200/dashboard/_mapping/company'


#curl -XPOST "http://ec2-52-26-9-10.us-west-2.compute.amazonaws.com:9200/dashboard/company/c1" -d '{"company" : "LinkedIn"}'
#curl -XPOST "http://ec2-52-26-9-10.us-west-2.compute.amazonaws.com:9200/dashboard/company/c2" -d '{"company" : "Facebook"}'
#curl -XPOST "http://ec2-52-26-9-10.us-west-2.compute.amazonaws.com:9200/dashboard/company/c3" -d '{"company" : "Fitbit"}'
#curl -XPOST "http://ec2-52-26-9-10.us-west-2.compute.amazonaws.com:9200/dashboard/company/c4" -d '{"company" : "Yelp"}'
#curl -XPOST "http://ec2-52-26-9-10.us-west-2.compute.amazonaws.com:9200/dashboard/company/c5" -d '{"company" : "Slack"}'
#curl -XPOST "http://ec2-52-26-9-10.us-west-2.compute.amazonaws.com:9200/dashboard/company/c6" -d '{"company" : "Twitter"}'
#curl -XPOST "http://ec2-52-26-9-10.us-west-2.compute.amazonaws.com:9200/dashboard/company/c7" -d '{"company" : "Opendoor"}'
#curl -XPOST "http://ec2-52-26-9-10.us-west-2.compute.amazonaws.com:9200/dashboard/company/c8" -d '{"company" : "Grand Rounds"}'
#curl -XPOST "http://ec2-52-26-9-10.us-west-2.compute.amazonaws.com:9200/dashboard/company/c9" -d '{"company" : "Tamr"}'
#curl -XPOST "http://ec2-52-26-9-10.us-west-2.compute.amazonaws.com:9200/dashboard/company/c10" -d '{"company" : "Casetext"}'
#curl -XPOST "http://ec2-52-26-9-10.us-west-2.compute.amazonaws.com:9200/dashboard/company/c11" -d '{"company" : "Komodo Heath"}'
#curl -XPOST "http://ec2-52-26-9-10.us-west-2.compute.amazonaws.com:9200/dashboard/company/c12" -d '{"company" : "6sense"}'
#curl -XPOST "http://ec2-52-26-9-10.us-west-2.compute.amazonaws.com:9200/dashboard/company/c13" -d '{"company" : "Spire"}'
#curl -XPOST "http://ec2-52-26-9-10.us-west-2.compute.amazonaws.com:9200/dashboard/company/c14" -d '{"company" : "Zenysis"}'
#curl -XPOST "http://ec2-52-26-9-10.us-west-2.compute.amazonaws.com:9200/dashboard/company/c15" -d '{"company" : "Domino Data Labs"}'
#curl -XPOST "http://ec2-52-26-9-10.us-west-2.compute.amazonaws.com:9200/dashboard/company/c16" -d '{"company" : "The Voleon Group"}'
#curl -XPOST "http://ec2-52-26-9-10.us-west-2.compute.amazonaws.com:9200/dashboard/company/c17" -d '{"company" : "Tophatter"}'
#curl -XPOST "http://ec2-52-26-9-10.us-west-2.compute.amazonaws.com:9200/dashboard/company/c18" -d '{"company" : "Microsoft"}'
#curl -XPOST "http://ec2-52-26-9-10.us-west-2.compute.amazonaws.com:9200/dashboard/company/c19" -d '{"company" : "Oracle"}'
#curl -XPOST "http://ec2-52-26-9-10.us-west-2.compute.amazonaws.com:9200/dashboard/company/c20" -d '{"company" : "Apple"}'
#curl -XPOST "http://ec2-52-26-9-10.us-west-2.compute.amazonaws.com:9200/dashboard/company/c21" -d '{"company" : "Google"}'
#curl -XPOST "http://ec2-52-26-9-10.us-west-2.compute.amazonaws.com:9200/dashboard/company/c22" -d '{"company" : "Accenture"}'
#curl -XPOST "http://ec2-52-26-9-10.us-west-2.compute.amazonaws.com:9200/dashboard/company/c23" -d '{"company" : "Yahoo"}'
#curl -XPOST "http://ec2-52-26-9-10.us-west-2.compute.amazonaws.com:9200/dashboard/company/c24" -d '{"company" : "Cisco"}'
#curl -XPOST "http://ec2-52-26-9-10.us-west-2.compute.amazonaws.com:9200/dashboard/company/c25" -d '{"company" : "Stripe"}'
#curl -XPOST "http://ec2-52-26-9-10.us-west-2.compute.amazonaws.com:9200/dashboard/company/c26" -d '{"company" : "Sojern"}'
#curl -XPOST "http://ec2-52-26-9-10.us-west-2.compute.amazonaws.com:9200/dashboard/company/c27" -d '{"company" : "SambaTV"}'
#curl -XPOST "http://ec2-52-26-9-10.us-west-2.compute.amazonaws.com:9200/dashboard/company/c28" -d '{"company" : "Driver Group"}'
#curl -XPOST "http://ec2-52-26-9-10.us-west-2.compute.amazonaws.com:9200/dashboard/company/c29" -d '{"company" : "Uber"}'

curl -XGET 'http://ec2-52-26-9-10.us-west-2.compute.amazonaws.com:9200/dashboard/company/c25'
