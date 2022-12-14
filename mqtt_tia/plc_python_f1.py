
import time
import paho.mqtt.client as paho
from paho import mqtt
import threading


def plc_data():
    plc_values = {}
    with open("file_plc.txt","r") as file:
        for line in file.readlines():
            a,b = line.split(":")
            plc_values[a.strip()] = b.strip() 
    return plc_values


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
    if msg.topic == "Start":
        write_


client = paho.Client(client_id="", userdata=None, protocol=paho.MQTTv5)
client.on_connect = on_connect


client.tls_set(tls_version=mqtt.client.ssl.PROTOCOL_TLS)
client.username_pw_set("mainamathengej@gmail.com", "wakaHATOLI001")
client.connect("29c3f12466b54850a985489d111baaf9.s1.eu.hivemq.cloud", 8883)


client.on_subscribe = on_subscribe
client.on_message = on_message
client.on_publish = on_publish


# RECEIVE DATA FROM MQTT
def app_to_plc_data():
    client.subscribe([("Start", 0), ("Stop", 2),("ConnectToMachine", 2)], qos=1)

    client.loop_forever()


# PUSH DATA TO MQTT
def plc_to_app_data():
    old_setpoint = ''
    while True:
        new_setpoint= str(plc_data()["setpoint"])
        if old_setpoint != new_setpoint:
            client.publish("SetPoint", payload=new_setpoint, qos=1)
            
            old_setpoint = new_setpoint
            time.sleep(0.1)


if __name__ == '__main__':
    thread1 = threading.Thread(target=plc_to_app_data)
    thread2 = threading.Thread(target=app_to_plc_data)

    thread1.start()
    thread2.start()

