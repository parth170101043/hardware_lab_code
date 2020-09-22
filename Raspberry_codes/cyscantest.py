import RPi.GPIO as GPIO
import time
import SimpleMFRC522
import paho.mqtt.client as mqtt
GPIO.setmode(GPIO.BCM)
GPIO.setup(18, GPIO.OUT)  #for buzzer....

def Readcard():
	reader=SimpleMFRC522.SimpleMFRC522()	
	print("Scanning for a card.....")
	#print("To cancel Press Ctrl-c")
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

already_in_use=0

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


if __name__ == "__main__":
	try:
		client=mqtt.Client()
		client.username_pw_set("bmyxxxis","icg681e_r1aT")#username,passwd
		client.connect("soldier.cloudmqtt.com",10462,60)
		client.on_connect = on_connect



		while True:
	      		ida,name=Readcard()
	      		#print(ida,name)
	      		if already_in_use!=1:
	      			validity=CheckValidData(ida,name)
		      		if validity==1:
		      			name1=name
		      		  	ida1=ida
		      		  	already_in_use=1
		      		  	issue="cycle issued by "+name1
					#print(name1)
					#print(ida)
		      			client.publish("test",issue)
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
	      				
					#mqtt code for sending msg that cycle is parked by the user with name and ida1
	      				print("cycle returned by "+name1)
					name1=""
	      				already_in_use=0
	      				ida1=""
					retu="Cycle returned by "+name1
					client.publish("test",retu)
					#print("cycle returned")
	      			else :
	      				beep_buzz()
					print("Sorry, cycle is already in use")
			time.sleep(5)
	finally:
		GPIO.cleanup()	
		client.disconnect()
