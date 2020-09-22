from gps import *
import time
import paho.mqtt.client as mqtt
import RPi.GPIO as GPIO
import webbrowser 
GPIO.setmode(GPIO.BCM)
GPIO.setup(18,GPIO.OUT)
GPIO.output(18,False)
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
def beep_buzz():
   # GPIO.output(18,True)
    time.sleep(0.5)
    #GPIO.output(18,False)
    





gpsd = gps(mode=WATCH_ENABLE|WATCH_NEWSTYLE) 
print 'latitude\tlongitude\ttime utc\t\t\taltitude\tepv\tept\tspeed\tclimb' # '\t' = TAB to try and output the data in columns.

try:

    
    while True:
       
        report = gpsd.next() #
        sent=False
        
#        print getattr(report, 'lat',0.0)
        if report['class'] == 'TPV':
            
            print  getattr(report,'lat',0.0),"\t",
            print  getattr(report,'lon',0.0),"\t",
            print getattr(report,'time',''),"\t",
            print  getattr(report,'alt','nan'),"\t\t",
            print  getattr(report,'epv','nan'),"\t",
            print  getattr(report,'ept','nan'),"\t",
            print  getattr(report,'speed','nan'),"\t",
            print getattr(report,'climb','nan'),"\t"
	    lati=getattr(report,'lat',0.0)
	    long=getattr(report,'lon',0.0)
            if lati<26.188000 or lati>26.1902989 or long<91.6972100 or long>91.69900:
		beep_buzz()
	       #print("bla bla")
		send("bla bla")   
            if not sent:
                send("https://www.google.com/maps/search/?api=1&query="+str(getattr(report,'lat',0.0))+','+str(getattr(report,'lon',0.0)))
                sent=True
	
       	    time.sleep(5) 
 
except (KeyboardInterrupt, SystemExit): #when you press ctrl+c
    print "Done.\nExiting."
    GPIO.cleanup()
