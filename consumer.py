"""
A Kafka Elasticsearch Consumer
"""
import json
import structlog
from confluent_kafka import Consumer
from elasticsearch import Elasticsearch

log = structlog.get_logger()

TOPIC = 'wikimedia.recentchange'
INDEX = 'wikimedia'


def kafka_consumer():
    properties = {
        'bootstrap.servers': 'kafka:29092',
        'group.id': 'consumer-elasticsearch-demo',
        'auto.offset.reset': 'latest',
        'enable.auto.commit': 'false',
    }

    return Consumer(properties)


if __name__ == '__main__':
    log.msg("Starting Elasticsearch Consumer")

    # Elasticsearch Client
    es = Elasticsearch("http://elasticsearch:9200")

    # Kafka Client
    consumer = kafka_consumer()

    try:
        # Subscribe to Wikimedia changes
        consumer.subscribe([TOPIC])

        while True:
            msg = consumer.poll(timeout=1.0)

            if msg is None:
                continue

            if msg.error():
                log.error(msg.error())
            else:
                log.info(
                    f'''
                    Key: {msg.key()}
                    Value: {msg.value()}
                    Partition: {msg.partition()}
                    Offset: {msg.offset()}'''
                )

                # Index data to Elasticsearch using ID from data
                data = json.loads(msg.value())
                try:
                    resp = es.index(index=INDEX, id=data["id"], document=data)
                except KeyError:
                    log.warning("Unable to parse ID from message: {data}")

    except KeyboardInterrupt:
        pass

    finally:
        # Close down consumer to commit final offsets.
        consumer.close()
