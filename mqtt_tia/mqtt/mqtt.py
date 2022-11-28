import paho.mqtt.client as paho
from paho import mqtt


# TODO MQTT UI SAMPLE CODE
# setting callbacks for different events to see if it works, print the message etc.
def on_connect(client_conn, userdata, flags, rc, properties=None):
    print("CONNACK<Response> received with code %s." % rc)


# with this callback you can see if your publish was successful
def on_publish(client_pub, userdata, mid, properties=None):
    print("mid: " + str(mid))


# print which topic was subscribed to
def on_subscribe(client_sub, userdata, mid, granted_qos, properties=None):
    print("Subscribed: " + str(mid) + " " + str(granted_qos))


# print message, useful for checking if it was successful
def on_message(client_msg, userdata, msg):
    print(str(msg.topic))
    print(str(msg.payload))
    # print(msg.topic + " " + str(msg.qos) + " " + str(msg.payload))


# using MQTT version 5 here, for 3.1.1: MQTTv311, 3.1: MQTTv31
# userdata is user defined data of any type, updated by user_data_set()
# client_id is the given name of the client
client = paho.Client(client_id="New User", userdata=None, protocol=paho.MQTTv5)
client.on_connect = on_connect

# enable TLS for secure connection
client.tls_set(tls_version=mqtt.client.ssl.PROTOCOL_TLS)
# set username and password
client.username_pw_set("Vincent Mworia", "mwendamworia")
# connect to HiveMQ Cloud on port 8883 (default for MQTT)
client.connect("8a32997794c84b92a769a6a46bb1582f.s1.eu.hivemq.cloud", 8883)

# setting callbacks, use separate functions like above for better visibility
client.on_subscribe = on_subscribe
client.on_message = on_message
client.on_publish = on_publish

# subscribe to all topics of encyclopedia by using the wildcard "#"
# client.subscribe("CITIES", qos=1)
client.subscribe([("CITIES", 0), ("STATES", 2)])


# a single publish, this can also be done in loops, etc.
# client.publish("Stations/Distribution/Monitor", payload="WEWERR!!", qos=1)
client.publish("CITIES", payload="MOMBASA", qos=1)
client.publish("STATES", payload="MERU", qos=1)
print('done')

# loop_forever for simplicity, here you need to stop the loop manually
# you can also use loop_start and loop_stop
client.loop_forever()
