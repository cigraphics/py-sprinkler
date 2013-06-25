import RPi.GPIO as GPIO
import time

"""
	A simple python script that will simply active a digital pin on the raspberry.
"""
def main(args):
	if (len(args) < 1):
		print('Usage: python act_pin.py <pin>')
		sys.exit(2)


	# configure gpio mode
	GPIO.setmode(GPIO.BOARD)
	GPIO.setwarnings(False)

	# Parse the pin we're talking about
	pin = int(args[0])

	# And setup it to OUT, and set its value to HIGH
	GPIO.setup(pin, GPIO.OUT)
	GPIO.output(pin, GPIO.HIGH)

	# sleep
	time.sleep(60)
	GPIO.output(pin, GPIO.LOW)

	# Cleanup the GPIO at the end of script.
	GPIO.cleanup()

# Standard boilerplate to call the main() function to begin the program.
if __name__ == '__main__':
	main(sys.argv[1:])				