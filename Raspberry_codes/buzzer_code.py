import RPi.GPIO as GPIO 
import time
GPIO.setmode(GPIO.BCM) 
GPIO.setup(23, GPIO.OUT)
try: 
	while True:
		GPIO.output(23, True)
finally:
	GPIO.cleanup()
