
import time
import paho.mqtt.client as paho
from paho import mqtt


def on_connect(client, userdata, flags, rc, properties=None):
    print("CONNACK received with code %s." % rc)

# with this callback you can see if your publish was successful
def on_publish(client, userdata, mid, properties=None):
    print("mid: " + str(mid))

# print which topic was subscribed to
def on_subscribe(client, userdata, mid, granted_qos, properties=None):
    print("Subscribed: " + str(mid) + " " + str(granted_qos))

# print message, useful for checking if it was successful
def on_message(client, userdata, msg):
    print(msg.topic + " " + str(msg.qos) + " " + str(msg.payload))


client = paho.Client(client_id="", userdata=None, protocol=paho.MQTTv5)
client.on_connect = on_connect


client.tls_set(tls_version=mqtt.client.ssl.PROTOCOL_TLS)
client.username_pw_set("username", "password")
client.connect("29c3f12466b54850a985489d111baaf9.s1.eu.hivemq.cloud", 8883)


client.on_subscribe = on_subscribe
client.on_message = on_message
client.on_publish = on_publish


client.subscribe("encyclopedia/#", qos=1)

client.publish("encyclopedia/temperature", payload="hot", qos=1)
client.loop_forever()
