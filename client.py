import RPi.GPIO as gpio
import time
import random
from picamera import PiCamera
import face_recognition as fr
from Crypto.Cipher import AES
import sys
import numpy

###initial setup
HOST="104.194.110.170"
PORT=6000
HEADER=64 #size of intial message to send
DISCONNECT_MESSAGE="!DISCONNECT" #send this message to disconnect
FORMAT="utf-8" #format for byte decoding
camera=PiCamera() #intialize camera
#intialize button that triggers camera
button=18 #using GPIO 18 for button
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
    camera.start_preview() #capture the image when the button pressed
    time.sleep(.5)
    camera.capture('incoming.jpg')
    camera.stop_preview()
    print('Picture Captured')

    #gpio.cleanup()
    #print("gpio cleaned up!")

    #generate a message to send to the server
    #message includes identity of the box, face encoding, code to unlock box
    boxid='box1' #this is different for every box
    target=fr.load_image_file('incoming.jpg')
    encodings=fr.face_encodings(target)
    if len(encodings)!=0:
        target_encoding=encodings[0] #grab the encoding of the face in the picture
        code=str(random.randrange(1,10000)) #generate a random code to trigger unlock with
        msg=boxid+code+str(target_encoding)
        print(msg)
    else:
        print('no face found')
        
gpio.cleanup()
print("gpio cleaned up!")


