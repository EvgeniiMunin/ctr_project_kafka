from kafka import KafkaConsumer
import logging

#logging.basicConfig(level=logging.DEBUG)


if __name__ == "__main__":
    # Create a Kafka consumer instance
    consumer = KafkaConsumer(
        bootstrap_servers="broker:29092",
        api_version=(0, 10, 5),
        value_deserializer=lambda value: value.decode("utf-8"),
        #auto_offset_reset="earliest",
        consumer_timeout_ms=20000
    )
    print("consumer created")

    consumer.subscribe(["test-topic"])
    print("consumer subscribed to topic")

    # Consume messages from the Kafka topic
    for message in consumer:
        print("msg check: ", message.key, message.value)

    consumer.close()

# consumer output: msg check: b'63' {"winery": "Vega Sicilia", "wine": "Unico Reserva Especial Edicion", "year": "2000", "rating": "4.7", "num_reviews": "935", "country": "Espana", "region": "Ribera del Duero", "price": "877.85", "type": "Ribera Del Duero Red", "body": "5", "acidity": "3"}