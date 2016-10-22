#!/usr/bin/python

# this source is part of my Hackster.io project:  https://www.hackster.io/mariocannistra/radio-astronomy-with-rtl-sdr-raspberrypi-and-amazon-aws-iot-45b617

# use this program to test the AWS IoT certificates received by the author
# to participate to the spectrogram sharing initiative on AWS cloud

# this program will subscribe and show all the messages sent by its companion
# awsiotpub.py using the AWS IoT hub

import paho.mqtt.client as paho
import os
import socket
import ssl
import json
import subprocess

connflag = False

updatecmd = ['aws', 's3', 'sync', 's3://vader-blackspace', '/home/pi/Desktop/s3', '--exclude', '"*"', '--include', '"*.mp3"', '--delete']

def on_connect(client, userdata, flags, rc):
    print("Connection returned result: " + str(rc) )
    # Subscribing in on_connect() means that if we lose the connection and
    # reconnect then subscriptions will be renewed.
    client.subscribe("$aws/things/Vader_Blackspace/shadow/update/accepted" , 1 )

def on_message(client, userdata, msg):
    global updatecmd
    print("topic: "+msg.topic)
    print("payload: "+str(msg.payload))
    data = json.loads(msg.payload)
    print(data)
    print(data["state"]["desired"]["switch"])
    if (data["state"]["desired"]["switch"]) == "on":
        print("update folder")
        subprocess.Popen(updatecmd)
    else:
        print("no update")

#def on_log(client, userdata, level, msg):
#    print(msg.topic+" "+str(msg.payload))

mqttc = paho.Client()
mqttc.on_connect = on_connect
mqttc.on_message = on_message
#mqttc.on_log = on_log

awshost = "a29fwj7qy7kt9i.iot.us-west-2.amazonaws.com"
awsport = 8883
clientId = "Vader_Blackspace"
thingName = "Vader_Blackspace"
caPath = "aws-iot-rootCA.crt"
certPath = "cert.pem"
keyPath = "privkey.pem"

mqttc.tls_set(caPath, certfile=certPath, keyfile=keyPath, cert_reqs=ssl.CERT_REQUIRED, tls_version=ssl.PROTOCOL_TLSv1_2, ciphers=None)

mqttc.connect(awshost, awsport, keepalive=60)

mqttc.loop_forever()
