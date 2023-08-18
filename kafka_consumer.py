from confluent_kafka import Consumer


def consume_events():
    consumer_config = {
        "bootstrap.servers": "localhost:9092",
        "group.id": "cat_photo_group",
        "auto.offset.reset": "earliest",
    }

    consumer = Consumer(consumer_config)
    topic = "cat_photo_events"
    consumer.subscribe([topic])

    try:
        while True:
            # Poll for new messages with a timeout of 10 second
            message = consumer.poll(10.0)

            if message is None:
                continue
            if message.error():
                print(f"Consumer error: {message.error()}")
                continue

            # Process the received message
            url_img = message.key().decode("utf-8")
            data = message.value().decode("utf-8")
            print(
                f"--- Received message ---\n"
                f"Last URL image: {url_img}\n"
                f"Last Likes/Views: {data}"
            )

    except KeyboardInterrupt:
        pass

    finally:
        consumer.close()


if __name__ == "__main__":
    consume_events()
