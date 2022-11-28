import time
import threading
import paho.mqtt.client as paho
from paho import mqtt


def on_connect(client_conn, userdata, flags, rc, properties=None):
    print("CONNACK<Response> received with code %s." % rc)


def on_publish(client_pub, userdata, mid, properties=None):
    print("mid: " + str(mid))


def on_subscribe(client_sub, userdata, mid, granted_qos, properties=None):
    print("Subscribed: " + str(mid) + " " + str(granted_qos))


def on_message(client_msg, userdata, msg):
    # todo, if received message, push to plc the variables
    print('to plc:')
    print(str(msg.payload))
    # print(msg.topic + " " + str(msg.qos) + " " + str(msg.payload))


client = paho.Client(client_id="VINCENT", userdata=None, protocol=paho.MQTTv5)
client.on_connect = on_connect

client.tls_set(tls_version=mqtt.client.ssl.PROTOCOL_TLS)
client.username_pw_set("Vincent Mworia", "mwendamworia")
client.connect("8a32997794c84b92a769a6a46bb1582f.s1.eu.hivemq.cloud", 8883)

client.on_subscribe = on_subscribe
client.on_message = on_message
client.on_publish = on_publish

client.subscribe("topic", qos=1)
client.loop_forever()


def app_to_plc_data():


def plc_to_app_data():
    while True:
        time.sleep(5)
        print('here')
        client.publish("topic", payload="MWORIA", qos=1)
        client.loop_forever()


if __name__ == '__main__':
    thread1 = threading.Thread(target=plc_to_app_data)
    thread2 = threading.Thread(target=app_to_plc_data)

    thread1.start()
    thread2.start()