
import time
import paho.mqtt.client as paho
from paho import mqtt
import threading
from dataclasses import dataclass
from tracemalloc import stop
from matplotlib.pyplot import connect
from opcua import Client, ua
import requests
import json
import math

# opcua funtions.
def read_input_value(node_id, client):  # get node
    client_node = Client.get_node(client, node_id)  # get node
    client_node_value = client_node.get_value()  # read node value
   # print("READ Value of : " + str(client_node) + " : " + str(client_node_value))
    return client_node_value


def write_value_bool(node_id, value, client):
    client_node = client.get_node(node_id)  # get node
    client_node_value = value
    client_node_dv = ua.DataValue(ua.Variant(client_node_value, ua.VariantType.Boolean))
    client_node.set_value(client_node_dv)
    print("WRITTEN Value of : " + str(client_node) + " : " + str(client_node_value))


def write_value_int(node_id, value, client):
    client_node = Client.get_node(client, node_id)  # get node
    client_node_value = value
    client_node_dv = ua.DataValue(ua.Variant(client_node_value, ua.VariantType.Int16))
    client_node.set_value(client_node_dv)
    print("WRITTEN Value of : " + str(client_node) + " : " + str(client_node_value))

# connecting to opcua.



# mqtt data funtions


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

    if msg.topic == 'StartMachine':
        print('Start ')
        write_value_bool('ns=4;i=4',True,client1)
        time.sleep(0.1)
        print('revert')
        write_value_bool('ns=4;i=4',False,client1)

    if msg.topic == 'StopMachine':
        print('Stop ')
        write_value_bool('ns=4;i=5',True,client1)
        time.sleep(0.1)
        print('revert')
        write_value_bool('ns=4;i=5',False,client1)
    
    if msg.topic == 'ConnectToMachine':
        print('Connect to Machine')
        write_value_bool('ns=4;i=3',True,client1)
        time.sleep(0.1)
        print('revert')
        #write_value_bool('ns=4;i=3',False,client1)
    if msg.topic == 'DisconnectMachine':
        print('Disconnect to Machine')
        write_value_bool('ns=4;i=7',True,client1)
        time.sleep(0.1)
        print('revert')
        write_value_bool('ns=4;i=3',False,client1)

    # if msg.topic == 'SetPoint':
    #     print('Disconnect to Machine')
    #     write_value_bool('ns=4;i=7',True,client1)
    #     time.sleep(0.1)
    #     print('revert')
    #     write_value_bool('ns=4;i=3',False,client1)

    if msg.topic == 'SetPoint':
        str_payload = msg.payload
        num = []
        for m in str_payload.split():
            if m.isdigit():
                num.append(int(m))
                print(num)
                if num[0] == 1:
                        print ("Setpoint == 1")
                        write_value_int('ns=4;i=6', 1, client1)
                if num[0] == 2:
                        print ("Setpoint == 2")
                        write_value_int('ns=4;i=6', 2, client1)
                if num[0] == 3:
                        print ("Setpoint == 3")
                        write_value_int('ns=4;i=6', 3, client1)
                if num[0] == 4:
                        print ("Setpoint == 4")
                        write_value_int('ns=4;i=6', 4, client1)
                if num[0] == 5:
                        print ("Setpoint == 5")
                        write_value_int('ns=4;i=6', 5, client1)
                if num[0] == 6:
                        print ("Setpoint == 6")
                        write_value_int('ns=4;i=6', 6, client1)
                if num[0] == 7:
                        print ("Setpoint == 7")
                        write_value_int('ns=4;i=6', 7, client1)
                if num[0] == 8:

                        print ("Setpoint == 8")
                        write_value_int('ns=4;i=6', 8, client1)
                if num[0] == 9:
                        print ("Setpoint == 9")
                        write_value_int('ns=4;i=6', 9, client1)
                if num[0] == 10:
                        print ("Setpoint == 10")
                        write_value_int('ns=4;i=6', 10, client1)


# RECEIVE DATA FROM MQTT
def app_to_plc_data():
    client.subscribe([("StartMachine", 0), ("StopMachine", 2),("ConnectToMachine", 2),("SetPoint", 2),("DisconnectMachine", 2)], qos=1)

    client.loop_forever()

 

# PUSH DATA TO MQTT
def plc_setpointvalue():
    old_setpoint = ''
    while True:
        new_setpoint= str(read_input_value('ns=4;i=6',client1))
        if old_setpoint != new_setpoint:
            print("Going to publish")
            client.publish("SetPoint", payload=new_setpoint, qos=1)
            
            old_setpoint = new_setpoint
        time.sleep(.1)
# def plc_processvariable():
#     old_Pv = ''
#     while True:
#         P_variable = str(read_input_value('ns=4;i=6',client1))
#         if old_Pv != P_variable:
#             print("Going to publish")
#             client.publish("ProcessVarible", payload=P_variable, qos=1)
            
#             old_Pv = P_variable
#         time.sleep(.1)

if __name__ == '__main__':
              # initialising Opcua
              url1 = "opc.tcp://192.168.0.13:4846"
              client1 = Client(url1)
              client1.connect()
              root1 = client1.get_root_node()
              print("Object root node is: ", root1)
                 #initialising Mqtt
              client = paho.Client(client_id="", userdata=None,
                                           protocol=paho.MQTTv5)
              client.on_connect = on_connect
              #client.tls_set(tls_version=mqtt.client.ssl.PROTOCOL_TLS)
              #client.username_pw_set("mainamathengej@gmail.com", "wakaHATOLI001")
              client.connect("test.mosquitto.org", 1883)
              client.on_subscribe = on_subscribe
              client.on_message = on_message
              client.on_publish = on_publish
              print('\n\n connection to MQTT initialised\n\n')



              print('\n\nConnection to OPCUA was Successful \n\n......WAIT FOR SERVER INITIALIZATIONytytyty.......\n\n')
              thread1 = threading.Thread(target=plc_setpointvalue)
              thread2 = threading.Thread(target=app_to_plc_data)
              thread1.start()
              thread2.start()
           
