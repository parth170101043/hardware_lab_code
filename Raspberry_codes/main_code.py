import RPi.GPIO as GPIO
import time
import datetime
import SimpleMFRC522
import paho.mqtt.client as mqtt
from multiprocessing import Process
import webbrowser
from gps import *

GPIO.setmode(GPIO.BCM)
GPIO.setup(18, GPIO.OUT)  #for buzzer....
GPIO.setup(19, GPIO.OUT)  #for motion sensor power
GPIO.setup(5, GPIO.IN)
#GPIO.setup(5, GPIO.IN)    #for motion sensor input
GPIO.output(19, True)

def runInParallel(*fns):
  proc = []
  for fn in fns:
    p = Process(target=fn)
    p.start()
    proc.append(p)
  for p in proc:
    p.join()

def Readcard():
    reader=SimpleMFRC522.SimpleMFRC522()    
    print("Scanning for a card.....")
    #print("To cancel Press Ctrl-c")
    #while reader.read()==False:
    #if GPIO.input(5):
    #        beep_buzz()
    ida, text = reader.read()
    print(ida)
    print(text)
    text=text.replace(" ","")
    return str(ida),str(text)

def CheckValidData(idin,namein):
    print(idin)
    f=open('doc','r')
    for line in f:
        for word in line.split():
            if is_number(word)==True:
                        ida=word
            else:
                        name=word
    #print(ida,name,idin,namein)
        if ida==idin and  name==namein:
            return 1
    return 0

def beep_buzz():
    GPIO.output(18, True)
    time.sleep(1)
    GPIO.output(18, False)
    return 

def send(topic,message):
    client=mqtt.Client()
    client.username_pw_set("wewyhfbx","Ff3UseLPny3p")
    #client.on_connect= on_connect
    client.connect("soldier.cloudmqtt.com",10511,60)
    client.publish(str(topic),str(message))
#    client.disconnect()


def is_number(s):
    try:
        float(s)
        return True
    except ValueError:
        pass
 
    try:
        import unicodedata
        unicodedata.numeric(s)
        return True
    except (TypeError, ValueError):
        pass
 
    return False
def on_connect(client, userData, flags, rc):
    print("Connected with result code " + str(rc))
    client.subscribe("MyInstanceName/topic")


def motion():
    try:
        while True:

            if GPIO.input(5):
                print("yes")
                  #  GPIO.output(18,True)
                beep_buzz()
                time.sleep(1)
                 #   GPIO.output(18,False)
            else:
                print("No")
            time.sleep(0.5)
    except:
        GPIO.cleanup()

def scanauto():
    try:
        # client=mqtt.Client()
        # client.username_pw_set("bmyxxxis","icg681e_r1aT")#username,passwd
        # client.connect("soldier.cloudmqtt.com",10462,60)
        # client.on_connect = on_connect
        already_in_use=0


        while True:
            ida,name=Readcard()
              #print(ida,name)
            if already_in_use!=1:
                validity=CheckValidData(ida,name)
                if validity==1:
                    name1=name
                    ida1=ida
                    GPIO.output(19, False)
                    already_in_use=1
                    issue=str(datetime.datetime.now().strftime("%I:%M%p %B %d, %Y"))+" Cycle  Issued by id: "+ida+" ,name: "+name1
                    #print(name1)
                    #print(ida)
                    # client.publish("test",issue)
                    send("file",issue)
                    print("cycle issue")
                    #openlock()
                    #mqtt code for sending msg that cycle is taken by the user with name and ida1
                else:
                    print("unauthorised user")
                    beep_buzz()
            else:
                if name==name1 and ida==ida1 :
                    #store data=store cycle taken time and parked time by the user with name and ida1
                    #close lock()
                    GPIO.output(19, True)
                    #mqtt code for sending msg that cycle is parked by the user with name and ida1
                    print("cycle returned by "+ida1+":"+name1)
                    retu = str(datetime.datetime.now().strftime("%I:%M%p %B %d, %Y"))+" Cycle  Returned by id: "+ida1+" ,name: "+name1
                    name1=""
                    already_in_use=0
                    ida1=""
                    #retu="Cycle returned by "+name1
                    # client.publish("test",retu)
                    send("file",retu)
                    #print("cycle returned")
                else :
                    beep_buzz()
                    print("Sorry, cycle is already in use")
            time.sleep(5)
    finally:
        GPIO.cleanup()    
#        client.disconnect()

def code_gps():
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
                if lati<26.185338 or lati>26.190473 or long<91.690877 or long>91.698874:
                    beep_buzz()
                    #print("bla bla")
                    send("file","Proximity crossed")   
                if not sent:
                    # send("https://www.google.com/maps/search/?api=1&query="+str(getattr(report,'lat',0.0))+','+str(getattr(report,'lon',0.0)))
                    send('web',str(getattr(report,'lat',0.0))+','+str(getattr(report,'lon',0.0)))

                    sent=True
        
                time.sleep(5) 
     
    except (KeyboardInterrupt, SystemExit): #when you press ctrl+c
        print "Done.\nExiting."
        GPIO.cleanup()
if __name__ == "__main__":

    runInParallel(motion, scanauto,code_gps)

