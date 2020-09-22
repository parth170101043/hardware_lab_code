import RPi.GPIO as GPIO
import SimpleMFRC522
GPIO.setmode(GPIO.BCM)
GPIO.setup(18, GPIO.OUT)
reader = SimpleMFRC522.SimpleMFRC522()
print("Scanning for a card.....")
print("To cancel Press Ctrl-c")
#GPIO.output(18, True)
try:
	id, text = reader.read()
	print(id)
	print(text+"hhghgh")
	GPIO.output(18, False)
finally:
	GPIO.cleanup()
