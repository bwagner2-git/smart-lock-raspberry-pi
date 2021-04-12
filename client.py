import RPi.GPIO as gpio
import time
import random
from picamera import PiCamera
import face_recognition as fr
from Crypto.Cipher import AES
import sys
import numpy
import socket
from Crypto.Util.Padding import pad, unpad
import serial

#get ready for serial communication with the Arduino later on
try:
    ser=serial.Serial('/dev/ttyACM0',9600)
except:
    ser=serial.Serial('/dev/ttyACM1',9600) #it seems to always be one of these two ports
ser.flush()

def send(msg):
    message = msg.encode(FORMAT)
    en_cipher=AES.new(KEY, AES.MODE_CBC, IV=iv)
    ciphertext=en_cipher.encrypt(pad(message,16))    
    msg_len=len(ciphertext)
    print("message length: " + str(msg_len))
    send_len=str(msg_len).encode(FORMAT)
    send_len+=b' '*(HEADER-len(send_len)) #make the first message 64
    client.send(send_len) #send out length of message
    client.send(ciphertext) #send the message

###initial setup
HOST="104.194.110.170"
PORT=6000
KEY=b'3874460957140850'
iv= b'9331626268227018'
HEADER=135 #size of intial message to send
DISCONNECT_MESSAGE="!DISCONNECT" #send this message to disconnect
FORMAT="utf-8" #format for byte decoding
camera=PiCamera() #intialize camera
#intialize button that triggers camera
button=18 #using GPIO 18 for button
gpio.setmode(gpio.BOARD)
gpio.setup(button,gpio.IN,pull_up_down=gpio.PUD_DOWN) #set pin 4 as input and tell it that it should be low by default
#gpio.add_event_detect(18,gpio.RISING,callback=say_cheese,bouncetime=200)	


while True:
    access=False #always assume they are an intruder at first
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
        code=str(random.randrange(1000,9999)) #generate a random code to trigger unlock with
        msg=boxid+','+code+','+str(target_encoding)
        print(msg)
        #setup the socket
        client=socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        client.connect((HOST,PORT))
        send(msg)
        message_back=client.recv(1024) #1024 arbitrary number that should always be big enough
        dec_cipher=AES.new(KEY, AES.MODE_CBC, IV=iv)
        message_back=dec_cipher.decrypt(message_back)
        message_back=unpad(message_back,16) #undo padding used for encryption and decryption
        message_back=message_back.decode(FORMAT) #make it readable
        print("Message back: " + message_back)
        if message_back == code:
            access=True
            print("Access Granted")
            ser.write(b"activate\n") #send the activation message to the Arduino
        else:
            print("Access Denied")
            ser.write(b'no no no not in my house\n') #tell Arduino access denied
        send(DISCONNECT_MESSAGE)
        client.close()
        
        
        
    else:
        print('no face found')
        
gpio.cleanup()
print("gpio cleaned up!")




