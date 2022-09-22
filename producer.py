"""
A Kafka Producer that listens to Wikimedia recent changes
"""
import requests
import time
import sseclient
import structlog
from confluent_kafka import Producer

log = structlog.get_logger()

TOPIC = 'wikimedia.recentchange'
WIKIMEDIA_URL = 'https://stream.wikimedia.org/v2/stream/recentchange'


if __name__ == '__main__':
    log.msg("Starting Kafka Wikimedia Producer")

    # Kafka Producer
    properties = {
        'bootstrap.servers': 'kafka:29092',
        'linger.ms': '20',
        'batch.size': 32 * 1024,
        'compression.type': 'snappy',
    }
    producer = Producer(properties)

    # Wikimedia stream
    headers = {'Accept': 'text/event-stream'}
    response = requests.get(WIKIMEDIA_URL, stream=True, headers=headers)
    client = sseclient.SSEClient(response)

    try:
        # Handle events
        for event in client.events():
            if event.event == 'message':
                log.info(event.data)
                producer.produce(TOPIC, event.data)

    except KeyboardInterrupt:
        pass

    finally:
        # flush and close the Producer
        producer.flush()
