from simple import MQTTClient
from machine import Pin
import network
import time
import ujson

SSID="Huawei"                                         #set the wifi ID 
PASSWORD="yellow1981"                                 #set the wifi password

led=Pin(2, Pin.OUT, value=0)

SERVER = "192.168.43.63"
CLIENT_ID = "umqtt_clientD"
TOPIC = b"Temp"
c=None

def sub_cb(topic, msg):
    global state
    print((topic, msg))
    obj=ujson.loads(msg.decode())
    value1=obj['value'] 
    sensorsId1=obj['id'] 
    print("温度传感器:"+str(sensorsId1)+"值为:"+str(value1)+"摄氏度")  
    
    
def connectWifi(ssid,passwd):
  global wlan
  wlan=network.WLAN(network.STA_IF)         #create a wlan object
  wlan.active(True)                         #Activate the network interface
  wlan.disconnect()                         #Disconnect the last connected WiFi
  wlan.connect(ssid,passwd)                 #connect wifi
  while(wlan.ifconfig()[0]=='0.0.0.0'):
    time.sleep(1)


#Catch exceptions,stop program if interrupted accidentally in the 'try'
try:
  connectWifi(SSID,PASSWORD)
  server=SERVER
  c = MQTTClient(CLIENT_ID, server)     #create a mqtt client
  c.set_callback(sub_cb) #set callback
  c.connect()                               #connect mqtt
  c.subscribe(TOPIC)                        #client subscribes to a topic
  print("Connected to %s, subscribed to %s topic" % (server, TOPIC))
  while True:
    c.check_msg()                            #wait message 
    time.sleep(10)
finally:
  if(c is not None):
    c.disconnect()
  wlan.disconnect()
  wlan.active(False)






