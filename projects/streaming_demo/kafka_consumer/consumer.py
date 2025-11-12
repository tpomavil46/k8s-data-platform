from kafka import KafkaConsumer
import json
import psycopg2
import os

# Note: No need for dotenv in containerized environment - K8s injects env vars directly

KAFKA_BOOTSTRAP_SERVERS = os.getenv('KAFKA_BOOTSTRAP_SERVERS', 'localhost:9092')
KAFKA_TOPIC = os.getenv('KAFKA_TOPIC', 'user-events')
KAFKA_GROUP_ID = os.getenv('KAFKA_GROUP_ID', 'python-consumer')

# Postgres connection
conn = psycopg2.connect(
    host=os.getenv('POSTGRES_HOST'),
    database=os.getenv('POSTGRES_DB'),
    user=os.getenv('POSTGRES_USER'),
    password=os.getenv('POSTGRES_PASSWORD')
)
cur_test = conn.cursor()
cur_test.execute("SELECT current_database(), inet_server_addr(), inet_server_port(), version()")
print(f"CONSUMER CONNECTED TO: {cur_test.fetchone()}")
cur_test.close()
cur = conn.cursor()

# Create table if not exists
cur.execute("""
    CREATE TABLE IF NOT EXISTS streaming.user_events (
        user_id INT,
        event_type VARCHAR(50),
        event_count INT,
        created_at TIMESTAMP DEFAULT NOW(),
        PRIMARY KEY (user_id, event_type)
    )
""")
conn.commit()

# Kafka consumer - use env vars here!
consumer = KafkaConsumer(
    KAFKA_TOPIC,  # Use env var
    bootstrap_servers=[KAFKA_BOOTSTRAP_SERVERS],  # Use env var
    value_deserializer=lambda m: json.loads(m.decode('utf-8')),
    group_id=KAFKA_GROUP_ID,  # Use env var
    auto_offset_reset='earliest'
)

print(f"Consuming messages from {KAFKA_TOPIC} on {KAFKA_BOOTSTRAP_SERVERS} and writing to Postgres...")

for message in consumer:
    event = message.value
    user_id = event['user_id']
    event_type = event['event_type']
    
    # Upsert into Postgres
    cur.execute("""
        INSERT INTO streaming.user_events (user_id, event_type, event_count)
        VALUES (%s, %s, 1)
        ON CONFLICT (user_id, event_type)
        DO UPDATE SET event_count = streaming.user_events.event_count + 1
    """, (user_id, event_type))
    
    conn.commit()
    print(f"Processed: user {user_id}, event {event_type}")