from kafka import KafkaProducer
import json
import requests
from urlparse import urlparse

initialURL = 'http://service.dice.com/api/rest/jobsearch/v1/simple.json?areacode=&country=US&state=&skill=&city=&text=data+engineering&ip=&diceid=&page=1'
parsed_uri = urlparse(initialURL)
domain = '{uri.scheme}://{uri.netloc}/'.format(uri=parsed_uri)

producer = KafkaProducer(bootstrap_servers='localhost:9092')
producer = KafkaProducer(value_serializer=lambda v: json.dumps(v).encode('utf-8'))


def getAndSendJobs(url):
   resp = requests.get(url)

   if resp.status_code != 200:
      # This means something went wrong.
      #raise ApiError('GET /tasks/ {}'.format(resp.status_code))
      print('Error')

   sendMessages(resp.json()['resultItemList'])
   return resp


def sendMessages(jobsListJSON):
   #Send to Kafka each job item inside "resultItemList"
   for json_item in jobsListJSON:
       #print('{} {}'.format(json_item['jobTitle'], todo_item['company']))
       producer.send('diceFeed', {'jobTitle': json_item['jobTitle'], 'company': json_item['company'] })

'''
for i in range(3):
   #   producer.send('foobar', b'some_message_bytes')
   producer.send('diceFeed', {'jobTitle': 'Data Engineering'})
'''

# Data Engineering jobs
# url = 'http://service.dice.com/api/rest/jobsearch/v1/simple.json?areacode=&country=US&state=&skill=&city=&text=data+engineering&ip=&diceid=&page=1'
resp = getAndSendJobs(initialURL)

while ( int(resp.json()['lastDocument']) <= int(resp.json()['count']) ):
   url = domain + resp.json()['nextUrl']
   resp = getAndSendJobs(url)


# Block until all pending messages are sent
producer.flush()

