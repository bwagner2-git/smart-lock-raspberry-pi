import RPi.GPIO as gpio
import time
import random
from picamera import PiCamera
import face_recognition as fr
from Crypto.Cipher import AES

###initial setup

camera=PiCamera() #intialize camera
#intialize button that triggers camera
button=18 #using GPIO 18
gpio.setmode(gpio.BOARD)
gpio.setup(button,gpio.IN,pull_up_down=gpio.PUD_DOWN) #set pin 4 as input and tell it that it should be low by default
#gpio.add_event_detect(18,gpio.RISING,callback=say_cheese,bouncetime=200)
	
while True:	
	try:
		while True:
			#print('hi')
			#time.sleep(1)
			if gpio.input(button)==gpio.HIGH:
				print('Say Cheese')
				break
	except KeyboardInterrupt:
		break
	camera.start_preview()
	time.sleep(.5)
	camera.capture('incoming.jpg')
	camera.stop_preview()
	print('Picture Captured')

gpio.cleanup()
print("gpio cleaned up!")


code=random.randrange(1,10000)



