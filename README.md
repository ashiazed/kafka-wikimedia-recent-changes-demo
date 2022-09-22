# Kafka producer/consumer demo

An example of a Kafka producer that sends Wikimedia recent chnages to a topic,
and a consumer that indexes the data into Elasticsearch

Bring up the containers

```
docker-compose up
```

## Working with the Python app

Enter app container:
```
docker-compose exec backend bash
```

## Basic demos

Run a producer:
```
python producer.py
```

Run a consumer:
```
python consumer.py
```
