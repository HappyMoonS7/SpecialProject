import time
import paho.mqtt.client as paho
from paho import mqtt
import mysql.connector
hostname ="rpp.h.filess.io"
username ="DataCenter_usualahead"
password ="c5210be739f4430e8443d6ba866744e19ba081f4"
database ="DataCenter_usualahead"
port = "3307"

# setting callbacks for different events to see if it works, print the message etc.
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
    print(msg.topic + " " + str(msg.qos) + " " + msg.payload.decode("utf-8"))
    if(msg.payload.decode("utf-8") == "hot"):
        mydb = mysql.connector.connect(host=hostname,database=database,user=username,password=password,port=port)
        mycursor = mydb.cursor()
        sql = "INSERT INTO customers (name, address) VALUES (%s, %s)"
        val = ("Jon", "Highway 21")
        mycursor.execute(sql, val)
        mydb.commit()
        mydb.close()
        print("Succesfully")
    

# using MQTT version 5 here, for 3.1.1: MQTTv311, 3.1: MQTTv31
# userdata is user defined data of any type, updated by user_data_set()
# client_id is the given name of the client
client = paho.Client(client_id="", userdata=None, protocol=paho.MQTTv5)
client.on_connect = on_connect

# enable TLS for secure connection
client.tls_set(tls_version=mqtt.client.ssl.PROTOCOL_TLS)
# set username and password
client.username_pw_set("Vittapong", "HappyS7*")
# connect to HiveMQ Cloud on port 8883 (default for MQTT)
client.connect("49ee04006403486ea360ca6114faf597.s2.eu.hivemq.cloud",8883)

# setting callbacks, use separate functions like above for better visibility
client.on_subscribe = on_subscribe
client.on_message = on_message
client.on_publish = on_publish

# subscribe to all topics of encyclopedia by using the wildcard "#"
client.subscribe("testTopic", qos=1)
client.subscribe("Test2", qos=1)

# a single publish, this can also be done in loops, etc.
client.publish("testTopic", payload="hot", qos=1)

# loop_forever for simplicity, here you need to stop the loop manually
# you can also use loop_start and loop_stop
client.loop_forever()