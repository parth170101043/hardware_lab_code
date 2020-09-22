from gps import *
import time
import paho.mqtt.client as mqtt

import webbrowser 

def on_connect(client, userData, flags, rc):
    print("Connected with result code " + str(rc))
    client.subscribe("MyInstanceName/topic")


def send(url):
    client=mqtt.Client()
    client.username_pw_set("wewyhfbx","Ff3UseLPny3p")
#    client.on_connect= on_connect
    client.connect("soldier.cloudmqtt.com",10511,60)
    client.publish('web',url)
    client.disconnect()
    





gpsd = gps(mode=WATCH_ENABLE|WATCH_NEWSTYLE) 
print 'latitude\tlongitude\ttime utc\t\t\taltitude\tepv\tept\tspeed\tclimb' # '\t' = TAB to try and output the data in columns.

try:

    sent=False
    
    while True:
       
        report = gpsd.next() #
        
        
#        print getattr(report, 'lat',0.0)
#        if report['class'] == 'TPV':
            
        print  getattr(report,'lat',0.0),"\t",
        print  getattr(report,'lon',0.0),"\t",
        print getattr(report,'time',''),"\t",
        print  getattr(report,'alt','nan'),"\t\t",
        print  getattr(report,'epv','nan'),"\t",
        print  getattr(report,'ept','nan'),"\t",
        print  getattr(report,'speed','nan'),"\t",
        print getattr(report,'climb','nan'),"\t"
            
        if not sent:
            send(str(getattr(report,'lat',0.0))+','+str(getattr(report,'lon',0.0)))
            sent=True
        time.sleep(4) 
 
except (KeyboardInterrupt, SystemExit): #when you press ctrl+c
    print "Done.\nExiting."
