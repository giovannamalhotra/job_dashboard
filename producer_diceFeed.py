from kafka import KafkaProducer
import json

producer = KafkaProducer(bootstrap_servers='localhost:9092')
producer = KafkaProducer(value_serializer=lambda v: json.dumps(v).encode('utf-8'))

for i in range(10):
    #   producer.send('foobar', b'some_message_bytes')

    # Serialize json messages
    producer.send('diceFeed', {'jobTittle': 'Data Engineering'})
 

# Block until all pending messages are sent
producer.flush()
