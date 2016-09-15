from kafka import KafkaProducer
import json
import requests
#from urlparse import urlparse

initialURL = 'http://api.indeed.com/ads/apisearch?publisher=9693529091171604&q=data+engineering&l=San+Francisco,+CA&radius=10&limit=10000&format=json&userip=65.87.19.170&useragent=Mozilla&v=2&start=0'
#parsed_uri = urlparse(initialURL)
#domain = '{uri.scheme}://{uri.netloc}/'.format(uri=parsed_uri)

producer = KafkaProducer(bootstrap_servers='localhost:9092')
producer = KafkaProducer(value_serializer=lambda v: json.dumps(v).encode('utf-8'))


def getAndSendJobs(url):
   resp = requests.get(url)

   if resp.status_code != 200:
      # This means something went wrong.
      #raise ApiError('GET /tasks/ {}'.format(resp.status_code))
      print('Error')

   sendMessages(resp.json()['results'])
   return resp


def sendMessages(jobsListJSON):
   #Send to Kafka each job item inside "resultItemList"
   for json_item in jobsListJSON:
       #print('{} {}'.format(json_item['jobTitle'], todo_item['company']))
       producer.send('indeedFeed', json_item)


# Data Engineering jobs in San Francisco
resp = getAndSendJobs(initialURL)
start = 0

while ( start <= 1000 ): #Indeed doesn't return more than 1000 rows at a time
   start += 25
   url = 'http://api.indeed.com/ads/apisearch?publisher=9693529091171604&q=data+engineering&l=San+Francisco,+CA&radius=10&limit=10000&format=json&userip=65.87.19.170&useragent=Mozilla&v=2&start=' + str(start)
   resp = getAndSendJobs(url)


# Block until all pending messages are sent
producer.flush()


