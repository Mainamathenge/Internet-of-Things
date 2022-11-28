import threading
import paho.mqtt.client as paho
from paho import mqtt
import json
from apscheduler.schedulers.blocking import BlockingScheduler
from opcua import Client, ua

scheduler = BlockingScheduler()

# distribution_nodes
dist_start_node_id = 'ns=3;s="PYTHON_COMM"."START"'
dist_stop_node_id = 'ns=3;s="PYTHON_COMM"."STOP"'
dist_reset_node_id = 'ns=3;s="PYTHON_COMM"."RESET"'
dist_code_step_node_id = 'ns=3;s="PYTHON_COMM"."CODE_STEP"'
dist_manual_auto_mode_node_id = 'ns=3;s="PYTHON_COMM"."MANUAL_AUTO_MODE"'
dist_manual_step_node_id = 'ns=3;s="PYTHON_COMM"."MANUAL_STEP"'
dist_system_on_node_id = 'ns=3;s="PYTHON_COMM"."SYSTEM_ON"'

# sorting_nodes
sort_start_node_id = 'ns=3;s="PYTHON_COMM_2"."START"'
sort_stop_node_id = 'ns=3;s="PYTHON_COMM_2"."STOP"'
sort_reset_node_id = 'ns=3;s="PYTHON_COMM_2"."RESET"'
sort_code_step_node_id = 'ns=3;s="PYTHON_COMM_2"."CODE_STEP"'
sort_manual_auto_mode_node_id = 'ns=3;s="PYTHON_COMM_2"."MANUAL_AUTO_MODE"'
sort_manual_step_node_id = 'ns=3;s="PYTHON_COMM_2"."MANUAL_STEP"'
sort_system_on_node_id = 'ns=3;s="PYTHON_COMM_2"."SYSTEM_ON"'
sort_workpiece_node_id = 'ns=3;s="PYTHON_COMM_2"."WORKPIECE"'
sort_metallic_number_node_id = 'ns=3;s="PYTHON_COMM_2"."METALLIC NUMBER" '
sort_red_number_node_id = 'ns=3;s="PYTHON_COMM_2"."RED NUMBER" '
sort_black_number_node_id = 'ns=3;s="PYTHON_COMM_2"."BLACK NUMBER" '
sort_total_number_node_id = 'ns=3;s="PYTHON_COMM_2"."TOTAL NUMBER" '


def establish_opc_conn(port):
    url = "opc.tcp://192.168.0." + port
    client_opcUa = Client(url)
    client_opcUa.connect()
    client_opcUa.get_root_node()
    return client_opcUa


def read_input_value(node_id, client_opc):
    client_node = Client.get_node(client_opc, node_id)  # get node
    client_node_value = client_node.get_value()  # read node value
    return client_node_value


def write_value_bool(node_id, value, client_opc):
    client_node = client_opc.get_node(node_id)  # get node
    client_node_value = value
    client_node_dv = ua.DataValue(ua.Variant(
        client_node_value, ua.VariantType.Boolean))
    client_node.set_value(client_node_dv)


def write_value_int(node_id, value, client_opc):
    client_node = Client.get_node(client_opc, node_id)  # get node
    client_node_value = value
    client_node_dv = ua.DataValue(ua.Variant(
        client_node_value, ua.VariantType.Int16))
    client_node.set_value(client_node_dv)


plc_client_1 = establish_opc_conn("6:10000")
plc_client_2 = establish_opc_conn("5:20000")


def on_connect(client_conn, userdata, flags, rc, properties=None):
    print("CONNACK<Response> received with code %s." % rc)


def on_publish(client_pub, userdata, mid, properties=None):
    print("mid: " + str(mid))


def on_subscribe(client_sub, userdata, mid, granted_qos, properties=None):
    print("Subscribed: " + str(mid) + " " + str(granted_qos))


def on_message(client_msg, userdata, msg):
    server_data = json.loads(str(msg.payload))
    # todo, if received message, push to plc the variables
    print(str(msg.topic))  # DISTINGUISH TOPICS FROM PLC
    print(str(msg.payload))
    # print(msg.topic + " " + str(msg.qos) + " " + str(msg.payload))


client = paho.Client(client_id="VINCENT 23",
                     userdata=None, protocol=paho.MQTTv5)
client.on_connect = on_connect

client.tls_set(tls_version=mqtt.client.ssl.PROTOCOL_TLS)
client.username_pw_set("Vincent Mworia", "mwendamworia")
client.connect("8a32997794c84b92a769a6a46bb1582f.s1.eu.hivemq.cloud", 8883)

client.on_subscribe = on_subscribe
client.on_message = on_message
client.on_publish = on_publish


# RECEIVE DATA FROM MQTT
def app_to_plc_data():
    client.subscribe([("CONTROL1", 0), ("CONTROL2", 2)], qos=1)

    client.loop_forever()


# PUSH DATA TO MQTT
def plc_to_app_data():
    plc_data_previous = {}
    plc_data_new = {}
    while True:
        # todo get plc data using opcua
        plc_data_new = {}  # opcdata
        if plc_data_previous != plc_data_new:
            # PUBLISH INDIVIDUALLY FOR EFFICIENCY, E.G.
            client.publish("MONITOR", payload=str(plc_data_new), qos=1)
            # client.publish("Stations/Distribution/Monitor", payload="WEWERR!!", qos=1)
            plc_data_previous = plc_data_new


if __name__ == '__main__':
    thread1 = threading.Thread(target=plc_to_app_data)
    thread2 = threading.Thread(target=app_to_plc_data)

    thread1.start()
    thread2.start()
