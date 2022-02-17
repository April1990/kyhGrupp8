import random

import paho.mqtt.client as paho
import time


CLIENT_ID = f'kyh-mqtt-{random.randint(0,1000)}'
USERNAME = 'kyh_1'
PASSWORD = 'kyh1super2'
BROKER = '104.248.47.103'
PORT = 1883


def on_connect(client, userdata, flags, rc):
    if rc == 0:
        print('Connected to MQTT Broker')
    else:
        print(f'Failed to connect to Broker. Error code {rc}')


def connect_mqtt():
    # Create a MQTT client object.
    # Every client has an id
    client = paho.Client(CLIENT_ID)
    # Set username and password to connect to broker
    client.username_pw_set(USERNAME, PASSWORD)

    # When connection response is received from broker
    # call the function on_connect
    client.on_connect = on_connect

    # Connect to broker
    client.connect(BROKER, PORT)

    return client


def main():
    client = connect_mqtt()
    # Start the paho loop that will
    # spawn a new thread and send and receive messages
    client.loop_start()

    sub_topic = 'adam/message/'
    # sub_topic = input('Publish to what sub-topic? ')

    while True:
        # Get current temperature
        temp = random.uniform(15.0, 25.0)
        # Publish to the topic temperature/room1 with temp
        client.publish(f'kyh/{sub_topic}', str(temp))
        # Interval to publish messages
        time.sleep(1)

    client.loop_stop()


if __name__ == '__main__':
    main()

