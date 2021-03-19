from AWSIoTPythonSDK.MQTTLib import AWSIoTMQTTClient
import logging
import time
import argparse
import json
import random 
import json, subprocess, psutil
import time, datetime
import math

mode = 'enter' # change this to exit to publish location to exit geofence

def getlocation(cnt):

    json_key={}
       
    json_key['deviceid']='deviceid1'
    json_key['timestamp']= math.trunc(time.time())

    if mode == 'enter':
        switcher={
            1: (-78.69228959083557,35.803326638426974),
            2: (-78.69122743606567,35.80302208862097),
            3: (-78.69088411331177,35.80286546255177),
            4: (-78.69049787521362,35.80279585086631),
            5: (-78.6901330947876, 35.80269143322378),
            6: (-78.68987560272217,35.802552209486876),
            7: (-78.68953227996826,35.80243038851692),
            8: (-78.68918895721436,35.80239558249118),  # Enter
            9: (-78.68897438049316,35.802343373424),
            10:(-78.68870615959167,35.80223025366069),
            11:(-78.6881160736084,35.80204752139509)
            }   
    else:
        switcher={
            1: (-78.6881160736084,35.80204752139509),
            2: (-78.68870615959167,35.80223025366069),
            3: (-78.68897438049316,35.802343373424),
            4: (-78.68918895721436,35.80239558249118),
            5: (-78.68953227996826,35.80243038851692), # Exit
            6: (-78.68987560272217,35.802552209486876),
            7: (-78.6901330947876, 35.80269143322378),
            8: (-78.69049787521362,35.80279585086631),
            9: (-78.69088411331177,35.80286546255177),
           10: (-78.69122743606567,35.80302208862097),
           11: (-78.69228959083557,35.803326638426974)
            }


        
    json_key['location']={}
    (json_key['location']['long'] ,json_key['location']['lat'])=switcher.get(cnt)
    
    return json_key


def publishlocation():

    host = 'a1jizs7tiywipi-ats.iot.us-east-1.amazonaws.com'
    rootCAPath='AmazonRootCA1.crt'
    certificatePath='myfleetiot.cert.pem'
    privateKeyPath='myfleetiot.private.key'
    clientId='locationtrack'
    port = 8883
    topic='iot/fleet/location'
    
    host = input("Enter IoT endpoint e.g. xxxxxxxx.iot.us-east-1.amazonaws.com. Get this from IoT console, choose settings on left-hand panel:")   
    
    myMQTTClient = None
    myMQTTClient = AWSIoTMQTTClient(clientId)
    myMQTTClient.configureEndpoint(host, port)
    myMQTTClient.configureCredentials(rootCAPath, privateKeyPath, certificatePath)
    
    myMQTTClient.configureAutoReconnectBackoffTime(1, 32, 20)
    myMQTTClient.configureOfflinePublishQueueing(-1)  # Infinite offline Publish queueing
    myMQTTClient.configureDrainingFrequency(2)
    myMQTTClient.configureConnectDisconnectTimeout(10) 
    myMQTTClient.configureMQTTOperationTimeout(15) 

# Connect and subscribe to AWS IoT
    message = {}
    myMQTTClient.connect()
    loopCount = 1
    while loopCount <= 11:
        message = getlocation(loopCount)
        messageJson = json.dumps(message)
        print(messageJson)
        myMQTTClient.publish(topic, messageJson, 1)
        print('Published topic %s: %s\n' % (topic, messageJson))
        loopCount += 1
        time.sleep(2)
    
publishlocation()