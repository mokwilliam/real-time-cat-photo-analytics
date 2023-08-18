import json
import requests
import random

from confluent_kafka import Producer


def download_cat_image_data() -> None:
    url: str = "https://api.thecatapi.com/v1/images/search"
    response = requests.get(url)
    data = response.json()[0]

    data_to_be_saved: dict = {
        "image_url": data["url"],
        "likes": random.randint(1, 10),
        "views": random.randint(10, 100),
    }

    try:
        with open("./cat_data.json", "r+") as file:
            existing_data = json.load(file)
            existing_data.append(data_to_be_saved)
            file.seek(0)
            json.dump(existing_data, file, indent=2)
            file.truncate()
    except FileNotFoundError:
        with open("./cat_data.json", "w") as file:
            json.dump([data_to_be_saved], file, indent=2)

    # Produce the event
    produce_event(data_to_be_saved)


def delivery_report(err, msg):
    if err is not None:
        print(f"Message delivery failed: {err}")
    else:
        print(
            f"Message delivered to {msg.topic()} \
                [{msg.partition()}] at offset {msg.offset()}"
        )


def produce_event(data_to_be_saved: dict) -> None:
    producer_config = {
        "bootstrap.servers": "localhost:9092",
    }

    producer = Producer(producer_config)
    topic = "cat_photo_events"

    producer.produce(
        topic,
        key=data_to_be_saved["image_url"],
        value=f"{data_to_be_saved['likes']}, {data_to_be_saved['views']}",
        callback=delivery_report,
    )

    # Wait up to 1 second for events. Callbacks will be invoked during
    # This method call if the message is acknowledged.
    producer.poll(1.0)


if __name__ == "__main__":
    test = [
        {
            "image_url": "https://cdn2.thecatapi.com/images/6tq.jpg",
            "likes": 8,
            "views": 52,
        }
    ]
    produce_event(test)
