import requests
import time, os, sys
from typing import Optional, Union, Any, Dict


def fetch_distance_data_from_api() -> Dict:

    url:str  = "http://iotapi.dev.tiacloud.io/api/get"

    response = requests.get(url)

    if response.status_code == 200:
        data = response.json()
        try:
            for index in range(len(data)):
                # Get RabbitMQ server cred and send data to queue
                send_data_to_rabbitmq(data[index])

                # print(f"{data[index]}")
                # simulate realtime data streaming with time.sleep()
                time.sleep(1)

        except IndexError as e:
            print("Error => Index out of range")


    else:
        print("Error: Failed to retrieve data from the API")

def send_data_to_rabbitmq(data: Dict):
    '''
    make connection to rabbitMQ server
    push data to server
    :return:
    '''

    print(f"Streaming data from API....{data}")
    # RabbitMQ credentials
    # RABBITMQ_HOST = os.environ.get("RABBITMQ_HOST")
    # RABBITMQ_PORT = os.environ.get("RABBITMQ_PORT")
    # RABBITMQ_EXCHANGE = os.environ.get("RABBITMQ_EXCHANGE")
    # RABBITMQ_ROUTING_KEY = os.environ.get("RABBITMQ_ROUTING_KEY")
    # RABBITMQ_QUEUE = os.environ.get("RABBITMQ_QUEUE")
    # RABBITMQ_USERNAME = os.environ.get("RABBITMQ_USERNAME")
    # RABBITMQ_PASSWORD = os.environ.get("RABBITMQ_PASSWORD")

    RABBITMQ_HOST = os.environ.get("RABBITMQ_HOST", "localhost")
    RABBITMQ_PORT = os.environ.get("RABBITMQ_PORT", "5672")
    RABBITMQ_EXCHANGE = os.environ.get("RABBITMQ_EXCHANGE", "")
    RABBITMQ_ROUTING_KEY = os.environ.get("RABBITMQ_ROUTING_KEY", "")
    RABBITMQ_QUEUE = os.environ.get("RABBITMQ_QUEUE", "api_data")
    RABBITMQ_USERNAME = os.environ.get("RABBITMQ_USERNAME", "test")
    RABBITMQ_PASSWORD = os.environ.get("RABBITMQ_PASSWORD", "test")

    try:
        # Credentials
        credentials = pika.PlainCredentials(RABBITMQ_USERNAME, RABBITMQ_PASSWORD)

        # Connect to RabbitMQ
        connection = pika.BlockingConnection(pika.ConnectionParameters(host=RABBITMQ_HOST, port=RABBITMQ_PORT, credentials=credentials))

        # Create a channel
        channel = connection.channel()

        # Declare the exchange
        channel.exchange_declare(exchange=RABBITMQ_EXCHANGE, exchange_type='direct')

        # Declare the queue
        channel.queue_declare(queue=RABBITMQ_QUEUE, durable=True)

        # Bind the queue to the exchange with the routing key
        channel.queue_bind(queue=RABBITMQ_QUEUE, exchange=RABBITMQ_EXCHANGE, routing_key=RABBITMQ_ROUTING_KEY)

        # Publish the message to the exchange with the routing key
        channel.basic_publish(
            exchange=RABBITMQ_EXCHANGE,
            routing_key=RABBITMQ_ROUTING_KEY,
            body=data,
            properties=pika.BasicProperties(
                delivery_mode=2
            )
        )

        # Close the connection
        connection.close()
        return True

    except Exception as e:
        print("Error: %s" % str(e))
        return False



def send_data_from_rabbitmq_to_mongodb_collection()-> None:
    '''
    - collects buffered data from rabbit queue and sends them  MongoDB collection
    - sends raw buffered data to one collection and filtered data to another collection
    - will send email when data point (distance) is higher than 12
    :return:
    '''
    pass

if __name__ == "__main__":
    fetch_distance_data_from_api()
