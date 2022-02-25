# python 3.6

import random
import time
from paho.mqtt import client as mqtt_client
import psutil
import json

broker = 'localhost'
port = 1883
topic = "solace/try/this/topic"
# generate client ID with pub prefix randomly
client_id = f'python-mqtt-{random.randint(0, 1000)}'
username = 'default'
password = 'default'

def connect_mqtt():
    def on_connect(client, userdata, flags, rc):
        if rc == 0:
            print("Connected to MQTT Broker!")
        else:
            print("Failed to connect, return code %d\n", rc)

    client = mqtt_client.Client(client_id)
    client.username_pw_set(username, password)
    client.on_connect = on_connect
    client.connect(broker, port)
    return client


def publish(client):
    modus = 'topic'
    while True:
        cpu = psutil.cpu_percent()
        used_ram_percent = psutil.virtual_memory().percent
        total_ram = round(psutil.virtual_memory().total * 1e-9, 2)
        used_ram = round(psutil.virtual_memory().used * 1e-9, 2)
        free_ram = round(psutil.virtual_memory().free * 1e-9, 2)
        time.sleep(5) 
        values = dict({"cpu" : cpu,
                       "used_ram_percent": used_ram_percent,
                       "total_ram" : total_ram,
                       "used_ram" : used_ram,
                       "free_ram" : free_ram})
        jsonStr = json.dumps(values)
        
        result = client.publish(topic, jsonStr)             


def run():
    client = connect_mqtt()
    client.loop_start()
    publish(client)


if __name__ == '__main__':
    run()
