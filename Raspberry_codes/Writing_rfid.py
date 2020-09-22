import RPi.GPIO as GPIO
import SimpleMFRC522

reader = SimpleMFRC522.SimpleMFRC522()
try:
	text = raw_input('Enter New Data for writing to card:')
	print("Now Place your tag to Write")
	reader.write(text)
	print("Data was written Successfully")
finally:
	GPIO.cleanup()
