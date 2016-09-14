from kafka import KafkaProducer
import json
import requests

producer = KafkaProducer(bootstrap_servers='localhost:9092')
producer = KafkaProducer(value_serializer=lambda v: json.dumps(v).encode('utf-8'))

for i in range(3):
   #   producer.send('foobar', b'some_message_bytes')

   # Serialize json messages
   producer.send('diceFeed', {'jobTitle': 'Data Engineering'})


resp = requests.get('http://service.dice.com/api/rest/jobsearch/v1/simple.json?areacode=&country=US&state=&skill=&city=&text=data+engineering&ip=&diceid=&page=1')
if resp.status_code != 200:
   # This means something went wrong.
   #raise ApiError('GET /tasks/ {}'.format(resp.status_code))
   print('Error') 

for json_item in resp.json()['resultItemList']:
   #print('{} {}'.format(json_item['jobTitle'], todo_item['company']))
   producer.send('diceFeed', {'jobTitle': json_item['jobTitle'], 'company': json_item['company'] })
 

# Block until all pending messages are sent
producer.flush()


