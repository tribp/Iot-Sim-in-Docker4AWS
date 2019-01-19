'''
/* Thing sending mqtt to AWS via Paho library (and NOT  AWSIoTPythonSDK.MQTTLib)
 *
 * 1) Configure AWS-IoT
 *      - Thing:
 *          - Create Thing + cert affiliates
 *          - copy your "EndPoint" (eg. 'XXXXX-xxx.iot.eu-west-1.amazonaws.com')
 *               ! Keep this 'endpoint' Secret
 *      - Rules:
 *          - when creating 'rules' = best practise !!!
 *              - if restriction on Thingname in rule, we need to connect with
 *                  'client_id = 'Thingname' -> t-default not needed with Paho !
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

# Import package
import paho.mqtt.client as mqtt
import ssl
import time
import json

# False = 1 message -> True= infinite loop
Run_Always = True

# Define Variables
MQTT_PORT = 8883
MQTT_KEEPALIVE_INTERVAL = 45
MQTT_TOPIC = "telco/test"

# AWS EndPoint + public ROOT Certificates + thing cert & private key
MQTT_HOST = "xxxxxxxxx-xxx.iot.eu-west-1.amazonaws.com"
CA_ROOT_CERT_FILE = "/certs/root-CA.crt"
THING_CERT_FILE = "/certs/AirQSimDocker001.cert.pem"
THING_PRIVATE_KEY = "/certs/AirQSimDocker001.private.key"


# Define on_publish event function
def on_publish(client, userdata, mid):
	print "Message Published..."


# Initiate MQTT Client
mqttc = mqtt.Client(client_id="AirQSimDocker001")

# Register publish callback function
mqttc.on_publish = on_publish

# Configure TLS Set
mqttc.tls_set(CA_ROOT_CERT_FILE, certfile=THING_CERT_FILE, keyfile=THING_PRIVATE_KEY, cert_reqs=ssl.CERT_REQUIRED, tls_version=ssl.PROTOCOL_TLSv1_2, ciphers=None)

# Connect with MQTT Broker
mqttc.connect(MQTT_HOST, MQTT_PORT, MQTT_KEEPALIVE_INTERVAL)
mqttc.loop_start()

# start sending messaages
counter = 0
while Run_Always:
    # define your message in json format
    MQTT_MSG_JSON = {
    'temperature': 20,
    'humidity': 51,
    'pm10': 7,
    'pm25':12,
    #'timestamp': time.clock()
    'time_epoch':time.time(),
    'time': time.ctime(),
    'count':counter,
    'service': 'Fluvius Telco'
    }
    # convert json object to string
    MQTT_MSG = json.dumps(MQTT_MSG_JSON)

    # send your message as a string
    mqttc.publish(MQTT_TOPIC,MQTT_MSG,qos=1)

    counter += 1
    # Set to True for infinite loop, else only 1 MQTT message
    Run_Always = False
    if Run_Always:
        # send message ever x seconds
        time.sleep(10)
    else :
        # single shot but need to wait for async callback
        time.sleep(2)

# Disconnect from MQTT_Broker
print("disconnecting ......")
mqttc.disconnect()# Import package
