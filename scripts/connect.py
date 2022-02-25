import paho.mqtt.client as mqtt
import json
from sqlalchemy import create_engine


#engine = create_engine('mysql+pymysql://blub12:Gsef-&Tbd@85.215.80.236:3306/tutorial')
#engine = create_engine('mysql+pymysql://root:password@localhost/tutorial')
#conn = engine.connect()

# The callback for when the client receives a CONNACK response from the server.
def on_connect(client, userdata, flags, rc):
    print("Connected with result code "+str(rc))
    # Subscribing in on_connect() means that if we lose the connection and
    # reconnect then subscriptions will be renewed.
    client.subscribe("$SYS/#")

# The callback for when a PUBLISH message is received from the server.
def on_message(client, userdata, msg):
    msg.payload = msg.payload.decode("utf-8")
    loadJson(msg.payload, 'print')
    
def loadJson(payload, type='print'):
    try:
        if type == 'print':
            print(payload)
        
        elif type == "status":
            obj = json.loads(payload)
            status = obj["status"]
            print("Change status of " + obj["stationId"] + " to " + status)
            conn.execute("INSERT INTO {} ({}, {}) values ('{}', '{}')".format('test','stationId', 'status', str(obj['stationId']), str(obj['status'])))
            
        elif type == "performance":
            obj = json.loads(payload)
            conn.execute("INSERT INTO {} ({}, {}, {}, {}, {}) values ('{}', '{}', '{}', '{}', '{}')".format('performance','cpu', 'used_ram_percent','total_ram', 'used_ram', 'free_ram',
                                                                                                             str(obj['cpu']), str(obj['used_ram_percent']), str(obj['total_ram']), str(obj['used_ram']), str(obj['free_ram'])))
           
    except Exception as e: print(e)
        

client = mqtt.Client()
client.username_pw_set("default", password="default") 
client.on_connect = on_connect
client.on_message = on_message

#connect to mqtt port
client.connect("localhost", 1883, 60)
client.subscribe("solace/try/this/topic")

# Blocking call that processes network traffic, dispatches callbacks and
# handles reconnecting.
# Other loop*() functions are available that give a threaded interface and a
# manual interface.
client.loop_forever()


