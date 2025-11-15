# streaming_demo/flink-jobs/kafka_to_postgres.py
from pyflink.datastream import StreamExecutionEnvironment
from pyflink.datastream.connectors.kafka import KafkaSource, KafkaOffsetsInitializer
from pyflink.common.serialization import SimpleStringSchema
from pyflink.common import Types
from pyflink.datastream.functions import MapFunction
import json
import os

class PostgresUpsertFunction(MapFunction):
    """Custom function to upsert events to Postgres"""
    
    def open(self, runtime_context):
        import psycopg2
        # Create Postgres connection
        self.conn = psycopg2.connect(
            host=os.getenv('POSTGRES_HOST'),
            database=os.getenv('POSTGRES_DB'),
            user=os.getenv('POSTGRES_USER'),
            password=os.getenv('POSTGRES_PASSWORD')
        )
        self.cur = self.conn.cursor()
        
        # Create table if not exists
        self.cur.execute("""
            CREATE TABLE IF NOT EXISTS streaming.user_events (
                user_id INT,
                event_type VARCHAR(50),
                event_count INT,
                created_at TIMESTAMP DEFAULT NOW(),
                PRIMARY KEY (user_id, event_type)
            )
        """)
        self.conn.commit()
    
    def map(self, value):
        # Parse JSON event
        event = json.loads(value)
        user_id = event['user_id']
        event_type = event['event_type']
        
        # Upsert into Postgres (exact same logic as Python consumer)
        self.cur.execute("""
            INSERT INTO streaming.user_events (user_id, event_type, event_count)
            VALUES (%s, %s, 1)
            ON CONFLICT (user_id, event_type)
            DO UPDATE SET event_count = streaming.user_events.event_count + 1
        """, (user_id, event_type))
        
        self.conn.commit()
        return f"Processed: user {user_id}, event {event_type}"
    
    def close(self):
        self.cur.close()
        self.conn.close()

def main():
    # Create execution environment
    env = StreamExecutionEnvironment.get_execution_environment()
    env.set_parallelism(1)  # Keep at 1 to avoid concurrency issues with Postgres
    
    # Kafka connection settings
    kafka_servers = os.getenv('KAFKA_BOOTSTRAP_SERVERS', 'kafka-service.streaming-demo:9092')
    kafka_topic = os.getenv('KAFKA_TOPIC', 'user-events')
    kafka_group_id = os.getenv('KAFKA_GROUP_ID', 'flink-consumer')
    
    # Create Kafka source
    kafka_source = KafkaSource.builder() \
        .set_bootstrap_servers(kafka_servers) \
        .set_topics(kafka_topic) \
        .set_group_id(kafka_group_id) \
        .set_starting_offsets(KafkaOffsetsInitializer.earliest()) \
        .set_value_only_deserializer(SimpleStringSchema()) \
        .build()
    
    # Create stream from Kafka
    stream = env.from_source(kafka_source, "Kafka Source")
    
    # Apply Postgres upsert function
    result = stream.map(PostgresUpsertFunction(), output_type=Types.STRING())
    
    # Print results (optional, for debugging)
    result.print()
    
    # Execute
    env.execute("Kafka to Postgres Flink Job")

if __name__ == '__main__':
    main()