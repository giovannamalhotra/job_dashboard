from kafka import KafkaProducer
import json
import requests
#from urlparse import urlparse

initialURL = 'http://api.indeed.com/ads/apisearch?publisher=9693529091171604&radius=10&limit=10000&format=json&userip=65.87.19.170&useragent=Mozilla&v=2'
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
   
   if 'results' in resp.json():
      sendMessages(resp.json()['results'])
      return resp


def sendMessages(jobsListJSON):
   #Send to Kafka each job item
   for json_item in jobsListJSON:
       #print('{} {}'.format(json_item['jobtitle'], todo_item['company']))
       producer.send('indeedFeed', {'jobtitle': json_item['jobtitle'], 'company': json_item['company'], 'city': json_item['city'], 'state': json_item['state'], 'country': json_item['country'], 'formattedLocation': json_item['formattedLocation'], 'date': json_item['date'], 'snippet': json_item['snippet'], 'url': json_item['url'], 'formattedLocationFull': json_item['formattedLocationFull'] })


#Arrays for combinations
locationArray = ['San+Francisco,+CA', 'Palo+Alto,+CA', 'New+York,+NY', 'Austin,+TX', 'Los+Angeles,+CA', 'Miami,+CA', 'Seattle,+WA', 'Oakland,+CA', 'San+Diego,+CA' ]
jobtitleArray = ['data+engineer', 'python', 'java', 'javascript', 'ruby', 'react', 'oracle', 'product manager', 'sql', 'c++', '.net',  'angular', 'cassandra', 'spark', 'sap', 'data scientist' ] 

for location in locationArray:
   for title in jobtitleArray:
      
      additionalParams = '&q=' + title + '&l=' + location 
      resp = getAndSendJobs(initialURL + additionalParams)
      start = 0

      while ( start <= 1000 ): #Indeed doesn't return more than 1000 rows at a time
         start += 25
         url = initialURL + additionalParams + '&start=' + str(start)
         resp = getAndSendJobs(url)


'''
# Data Engineering jobs in San Francisco
resp = getAndSendJobs(initialURL + '&q=data+engineering&l=San+Francisco,+CA')
start = 0

while ( start <= 1000 ): #Indeed doesn't return more than 1000 rows at a time
   start += 25
   url = initialURL + '&start=' + str(start)
   resp = getAndSendJobs(url)
'''


# Block until all pending messages are sent
producer.flush()


