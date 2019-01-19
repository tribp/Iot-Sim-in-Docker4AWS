'''
/* Thing sending mqtt to AWS via AWSIoTPythonSDK.MQTTLib library (and NOT Paho)
 *
 * 1) Configure AWS-IoT
 *      - Thing:
 *          - Create Thing + cert affiliates
 *          - copy your "EndPoint" (eg. 'XXXXX-xxx.iot.eu-west-1.amazonaws.com')
 *               ! Keep this 'endpoint' Secret
 *      - Rules:
 *          - when creating 'rules' = best practise !!!
 *              - if restriction on Thingname in rule, we need to connect with
 *                  'client_id = 'Thingname' -> default in aws !
 *              - if restriction on 'Topic' in rule, be sure the use the same topic here
 *
 * 2) One Shot or continious messages:
 *      - set line 88: False = 'One shot' / True = 'continious'
 *      - set line 91 to determine interval
 *
 * 3) Message payload:
 *      - determine your payload as a json object
 *      - convert payload into String
 *      - publish payload(string) on your topic;
 */
'''

from AWSIoTPythonSDK.MQTTLib import AWSIoTMQTTClient
import logging
import time
import json


# Custom MQTT message callback
def customCallback(client, userdata, message):
    print("Received a new message: ")
    print(message.payload)
    print("from topic: ")
    print(message.topic)
    print("--------------\n\n")


# Set basic AWS parameters
host = 'xxxxxxxxxxxxxx.iot.eu-west-1.amazonaws.com'
rootCAPath = '/certs/root-CA.crt'
certificatePath = '/certs/AirQSimDocker001.cert.pem'
privateKeyPath = '/certs/AirQSimDocker001.private.key'
port = 8883
clientId = 'AirQSimDocker001'
topic = 'telco/test'

# Configure logging
logger = logging.getLogger("AWSIoTPythonSDK.core")
logger.setLevel(logging.DEBUG)
streamHandler = logging.StreamHandler()
formatter = logging.Formatter('%(asctime)s - %(name)s - %(levelname)s - %(message)s')
streamHandler.setFormatter(formatter)
logger.addHandler(streamHandler)

# Init AWSIoTMQTTClient
myAWSIoTMQTTClient = None
myAWSIoTMQTTClient = AWSIoTMQTTClient(clientId)
myAWSIoTMQTTClient.configureEndpoint(host, port)
myAWSIoTMQTTClient.configureCredentials(rootCAPath, privateKeyPath, certificatePath)

# AWSIoTMQTTClient connection configuration
myAWSIoTMQTTClient.configureAutoReconnectBackoffTime(1, 32, 20)
myAWSIoTMQTTClient.configureOfflinePublishQueueing(-1)  # Infinite offline Publish queueing
myAWSIoTMQTTClient.configureDrainingFrequency(2)  # Draining: 2 Hz
myAWSIoTMQTTClient.configureConnectDisconnectTimeout(10)  # 10 sec
myAWSIoTMQTTClient.configureMQTTOperationTimeout(5)  # 5 sec


# Connect and subscribe to AWS IoT
print("Connecting to Fluvius Telco ....")
myAWSIoTMQTTClient.connect()
print("Connected to Fluvius Telco !!!")
myAWSIoTMQTTClient.subscribe(topic, 1, customCallback)
time.sleep(2)

# Publish to the same topic in a loop forever
loopCount = 0
while True:
    # define your message in json format
    message = {
    'temperature': 20,
    'humidity': 51,
    'pm10': 7,
    'pm25':12,
    #'timestamp': time.clock()
    'time_epoch':time.time(),
    'time': time.ctime(),
    'count':loopCount,
    'service': 'Fluvius Telco'
    }

    # convert json object to string
    messageJson = json.dumps(message)

    # send your message as a string
    myAWSIoTMQTTClient.publish(topic, messageJson, 0)
    print('Published topic %s: %s\n' % (topic, messageJson))
    loopCount += 1
    # send message ever x seconds
    time.sleep(30)
