import RPi.GPIO as GPIO
import time
GPIO.setmode(GPIO.BCM)
GPIO.setup(5, GPIO.IN)

try:
        #GPIO.output(24,True)
        while True:

                if GPIO.input(5):
                        print("yes")
                  #      time.sleep(2)
                else:
                        print("No")
                time.sleep(2)
except:
        GPIO.cleanup()

		
