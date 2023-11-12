import csv
import io
import logging
import time
from kafka import KafkaProducer
from kafka.errors import KafkaError

import avro.schema
from avro.io import DatumWriter


def read_csv(file_path):
    with open(file_path, "r") as file:
        reader = csv.DictReader(file)
        for row in reader:
            yield row


def publish(producer, topic, key, message):
    # produce keyed messages to enable hashed partitioning
    future = producer.send(topic, key=key, value=message)

    try:
        record_metadata = future.get(timeout=10)
        # successful result returns assigned partition and offset
        print(
            "topic: ", record_metadata.topic,
            "partition: ", record_metadata.partition,
            "offset: ", record_metadata.offset
        )

    except KafkaError:
        # decide what to do if produce request failed...
        logging.exception("Failed to send the message {}".format((key, message)))
        pass

    producer.flush()
    print("msgs json sent")


if __name__ == "__main__":
    schema_path = "user.avsc"
    schema = avro.schema.parse(open(schema_path).read())

    producer = KafkaProducer(
        bootstrap_servers="broker:29092",
        api_version=(0, 10, 5),
        #value_serializer=lambda x: json.dumps(x).encode("utf-8")
    )

    data = read_csv("wines_SPA.csv")
    for i, item in enumerate(data):
        bytes_writer = io.BytesIO()
        encoder = avro.io.BinaryEncoder(bytes_writer)

        writer = DatumWriter(schema)
        writer.write(
            {
                "winery": "Teso La Monja",
                "wine": "Tinto",
                "year": "2013",
                "rating": 4.9,
                "num_reviews": 58,
                "country": "Espana",
                "region": "Toro",
                "price": 995,
                "type": "Toro Red",
                "body": 5,
                "acidity": 3,
            },
            encoder
        )

        print("item: ", i, item)
        publish(
            producer=producer,
            topic="test-topic",
            key=str(i).encode("utf-8"),
            message=item
        )
        time.sleep(3)

    producer.close()

# consumer output {"event_id": 123, "website": "https://www.rolex.com/", "name": "John Doe", "action": "click"}
# json serialization, no schema enforced

# "winery","wine","year","rating","num_reviews","country","region","price","type","body","acidity"
# "Teso La Monja","Tinto","2013",4.9,58,"Espana","Toro",995,"Toro Red",5,3
