#include <Servo.h>

#define greenLight 8
#define redLight 10
#define servoPin 9
#define lockedPosition 180
#define unlockedPosition 0

Servo servo; //initate servo object
bool locked = true;

void setup() {
  // put your setup code here, to run once:
  Serial.begin (9600);
  pinMode(greenLight,OUTPUT);
  pinMode(5,OUTPUT);
  pinMode(servoPin,OUTPUT);
  servo.attach(servoPin);
  digitalWrite(redLight, LOW);
  digitalWrite(greenLight, LOW);
  

}

void loop() {
  if(Serial.available()>0){
    String command = Serial.readStringUntil('\n');  
//    command.trim(); 
    if(command=="activate"){ //activate the lock
      if(locked){   
        servo.write(unlockedPosition);
        locked=false;
        digitalWrite(greenLight, HIGH);
        delay(4000);
        digitalWrite(greenLight, LOW);
      } else {
        servo.write(lockedPosition);
        locked=true;
        digitalWrite(greenLight, HIGH);
        delay(4000);
        digitalWrite(greenLight, LOW);
      } 
    } else { //warn that no access to lock granted
        digitalWrite(redLight, HIGH);
        delay(4000);
        digitalWrite(redLight, LOW);
       
    }
  }
  
  

}
