from kafka import KafkaProducer
import json
import time
import random
from datetime import datetime
import os

KAFKA_BOOTSTRAP_SERVERS = os.getenv('KAFKA_BOOTSTRAP_SERVERS', 'localhost:9092')
KAFKA_TOPIC = os.getenv('KAFKA_TOPIC', 'user-events')

producer = KafkaProducer(
    bootstrap_servers=[KAFKA_BOOTSTRAP_SERVERS],  # Use the env var here!
    value_serializer=lambda v: json.dumps(v).encode('utf-8')
)

def generate_event():
    return {
        'user_id': random.randint(1, 100),
        'event_type': random.choice(['click', 'view', 'purchase']),
        'timestamp': datetime.now().isoformat(),
        'value': random.randint(1, 100)
    }

if __name__ == '__main__':
    print(f"Producing messages to {KAFKA_TOPIC} on {KAFKA_BOOTSTRAP_SERVERS}...")
    
    while True:
        event = generate_event()
        producer.send(KAFKA_TOPIC, event)  # Use env var for topic too
        print(f"Sent: {event}")
        time.sleep(1)