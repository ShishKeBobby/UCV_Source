#include <Wire.h>
#include <TinyGPS++.h>

#define SLAVE_ADDRESS 0x04

String commandOut;
char number = 0;
char msgOut = 'k';
int state = 0;
int i = 0;
char command[255];
char message;
int newmessage = 0;
int payloadLen = 0;
String tempVal1, tempVal2, tempVal3;
char handler;
float masterlatt= 0;
float masterlong= 0;
float masterhead = 0;
float R = 6371000; //radius of earth
float pixel = 0;
float radius = 0;
int leftmotor=0;
int rightmotor=0;
String sendPayload;
float sLat = 0;
float sLon = 0;
int outputLen = 0;
char buffOut[255];
int turnVal = 0;

// The TinyGPS++ object
TinyGPSPlus gps;
char lattout[15];
char longout[15];
char satsOut[10];
char velOut[10];
char headout[10];
int numSats = 0;
int azimuthS = 0;
float latitudeS = 0;
float longitudeS = 0;
float velocity = 0;
float xS,yS,xM,yM = 0; 
float xGoal,yGoal = 0;
float distanceG = 0;
float headingG = 0;
float toR = 0.01745329252;
float toD = 57.295779513;
float theta = 0;
float ptheta = 0;

//Motor A
int power_motor1 = 6; //power to 1st motor (EN1)
int motor1_f= 22;
int motor1_b= 23;

//Motor B
int power_motor2 = 5;//power to 2nd motor (EN2)
int motor2_f = 7;
int motor2_b = 8;

int motor_speed2 = 0;
int motor_speed1 = 0;

void setup()
{
  
  pinMode(13, OUTPUT);
  Serial.begin(9600); 
  Serial1.begin(9600);
  Serial.setTimeout(100);
  // motor pin
  pinMode(power_motor1, OUTPUT);
  pinMode(power_motor2, OUTPUT);
  pinMode(motor1_f, OUTPUT);
  pinMode(motor2_f, OUTPUT);
  pinMode(motor1_b, OUTPUT);
  pinMode(motor2_b, OUTPUT);
  //moveleft(100,100);
  //delay(1000);
  //moveright(200,200);
  //delay(1000);
  Serial.print("ready");
  //motor stop
  stopmotor();
  
  // initialize i2c as slave
  Wire.begin(SLAVE_ADDRESS);
  
  // define callbacks for i2c communication
  Wire.onReceive(receiveData);
  Wire.onRequest(sendData);  
}


void loop(){
  while (Serial1.available() > 0)
  gps.encode(Serial1.read());
  if(newmessage == 1){
     //Serial.println(commandOut);
     if(commandOut[1]=='A'){
      //Serial.print("command ");
      //Serial.println("A");
      commandOut.remove(0,2); //remove handler chars
      tempVal1 = commandOut.substring(0,commandOut.indexOf(","));
      commandOut.remove(0,commandOut.indexOf(",")+1);
      tempVal2 = commandOut.substring(0,commandOut.indexOf(","));
      commandOut.remove(0,commandOut.indexOf(",")+1);
      commandOut.remove(commandOut.length()-1);
      tempVal3 = commandOut;
      commandOut = "";
      handler = 'A';
      masterlatt = tempVal1.toFloat();
      masterlong = tempVal2.toFloat();
      masterhead = tempVal3.toFloat();
//      Serial.print("1= ");
//      Serial.println(tempVal1);
//      Serial.print("2= ");
//      Serial.println(tempVal2);
//      Serial.print("3= ");
//      Serial.println(tempVal3);
    }
    else if(commandOut[1]=='B'){
      //Serial.println("B");     
      commandOut.remove(0,2); //remove handler chars
      tempVal1 = commandOut.substring(0,commandOut.indexOf(","));
      commandOut.remove(0,commandOut.indexOf(",")+1);
      commandOut.remove(commandOut.length()-1);
      tempVal2 = commandOut;
      commandOut = "";
      handler = 'B';
      pixel = tempVal1.toFloat();
      radius = tempVal2.toFloat();
//      Serial.print("1= ");
//      Serial.println(tempVal1);
//      Serial.print("2= ");
//      Serial.println(tempVal2);
    }
    else if(commandOut[1]=='C'){
      //Serial.println("C");
      commandOut.remove(0,2); //remove handler chars
      tempVal1 = commandOut.substring(0,commandOut.indexOf(","));
      commandOut.remove(0,commandOut.indexOf(",")+1);
      commandOut.remove(commandOut.length()-1);
      tempVal2 = commandOut;
      commandOut = "";
      handler = 'C';
      leftmotor = tempVal1.toInt();
      rightmotor = tempVal2.toInt();
//      Serial.print("1= ");
//      Serial.println(tempVal1);
//      Serial.print("2= ");
//      Serial.println(tempVal2);
    }
    
    if(handler == 'A' && newmessage == 1){
      int leftval, rightval = 0;
      //do GPS navigation
      //Serial.println("gathering data");
      //Serial.println("processing...");
      //Serial.println(gps.location.isUpdated());
      //radio.write("a,14);
      if (gps.location.isUpdated()){
        //Serial.println("running script");
        //while the number of satellites is greater than 4, we only want good data
        numSats = gps.satellites.value();
        azimuthS = gps.course.deg();
        //azimuthS = 270;
        latitudeS = gps.location.lat();
        longitudeS= gps.location.lng();
        velocity = gps.speed.kmph()*1000/3600;

//        Serial.print("latS ");
//        Serial.println(latitudeS,9);
//        Serial.print("lonS ");
//        Serial.println(longitudeS,9);
//        Serial.print("latM ");
//        Serial.println(masterlatt,9);
//        Serial.print("lonM ");
//        Serial.println(masterlong,9);
//        Serial.print("headingS ");
//        Serial.println(azimuthS);
//        Serial.print("headingM ");
//        Serial.println(masterhead,9);
//        Serial.println(" ");
//        //send these vals back to the Pi
//        dtostrf(latitudeS,10,6,lattout);
//        dtostrf(longitudeS,10,6,longout);
//        dtostrf(numSats,2,0,satsOut);
//        dtostrf(azimuthS,3,0,headout);
//        dtostrf(velocity,6,3,velOut);
        sendPayload = "0"+String(latitudeS,9) + "," + String(longitudeS,9) + "," + String(azimuthS,3);
        Serial.print("send payload ");
        Serial.println(sendPayload);
        //distanceG being the distance to the master vehicle,
        //headingG being the heading from where we are to travel.
        double dist = TinyGPSPlus::distanceBetween(latitudeS,longitudeS,masterlatt,masterlong);
        Serial.print("distanceBetween func. ");
        Serial.println(dist);
        double courseT = TinyGPSPlus::courseTo(latitudeS,longitudeS,masterlatt,masterlong);
        Serial.print("courseTo func. ");
        Serial.println(courseT); 
        xS = cos(azimuthS*toR);
        yS = sin(azimuthS*toR);
        xM = cos(courseT*toR);
        yM = sin(courseT*toR); 
        ptheta = theta; //save last value
        theta = atan2(yM*xS-xM*yS,xS*xM+yS*yM)*toD;  
        Serial.print("azimuthS ");
        Serial.println(azimuthS); 
        Serial.print("theta func. ");
        Serial.println(theta); 
        //theta is our direction to turn, dist is the total travel distance
        if(masterlatt == 0 || masterlong == 0){
          //if we got some garbage data, just use the last theta value
          theta = ptheta;
        }
        if(dist<3){
          //close enough for the camera to take over
          stopmotor();
        }
        else if (theta<0){
          //turn left
          rightval = map(theta,0,-180,200,255);
          leftval = map(theta,0,-180,200,50);
//          Serial.print("left ");
//          Serial.println(leftval);
//          Serial.print("right ");
//          Serial.println(rightval);
          moveleft(leftval,rightval);
        }
        else if(theta>0){
          leftval = map(theta,0,180,200,255);
          rightval = map(theta,0,180,200,50);
//          Serial.print("left ");
//          Serial.println(leftval);
//          Serial.print("right ");
//          Serial.println(rightval);
          moveright(leftval,rightval);          
        }
    }
   }

    else if(handler == 'B' && newmessage == 1){
     //do img navigation
     int leftVal,rightVal = 0;
     float radius_1 = constrain( radius, 20, 100);
     float radius_r = map(radius_1, 100, 20, 0 , 255);
     //Serial.print("Postradius = ");
     Serial.print("pixel = ");
     Serial.print(pixel);
     
     Serial.print(" turnval = ");
     Serial.println(turnVal);
     if (pixel >0 && pixel <98) 
      {//left
        
        Serial.print("moveleft = ");
        //float pixel_1 = map( pixel, 0, 97, 200, 0);  // map pixel value to delay to move angle fro 0 to 360
        //turn value is the difference between turning motors
        turnVal = map(pixel,1,98,255,200);
        rightVal = turnVal;
        turnVal = map(pixel,1,98,70,150);
        leftVal = turnVal;
        Serial.print(leftVal);
        Serial.print(" ");
        Serial.println(rightVal);
        moveleft(leftVal, rightVal);
        //delay(pixel_1);
      }
     else if (pixel > 233 && pixel <=320)
      {//right
        Serial.print("moveright = ");
        turnVal = map(pixel,320,234,70,150);
        rightVal = turnVal;
        turnVal = map(pixel,320,234,255,200);
        leftVal = turnVal;
        float pixel_1 = map( pixel, 232, 320, 0, 200);  // map pixel value to delay to move angle fro 0 to 360
        Serial.print(leftVal);
        Serial.print(" ");
        Serial.println(rightVal);
        moveright(leftVal, rightVal);
        //delay(pixel_1);
      }
     else if(pixel > 97 && pixel <232)
      {
        Serial.println("forward");
       //move forward
       digitalWrite(motor1_f, HIGH);
       digitalWrite(motor1_b, LOW);
       analogWrite(power_motor1, int(radius_r));
       digitalWrite(motor2_f, HIGH);
       digitalWrite(motor2_b, LOW);
       analogWrite(power_motor2, int(radius_r));
      }
    }

    else if(handler == 'C' && newmessage == 1){
      Serial.println("C");
      
    } 
    newmessage = 0;
    commandOut = "";
 } 
}

void moveforward()
{
  digitalWrite(motor1_f, HIGH);
  digitalWrite(motor1_b, LOW);
  analogWrite(power_motor1, 255);
  digitalWrite(motor2_f, HIGH);
  digitalWrite(motor2_b, LOW);
  analogWrite(power_motor2, 255); 
}

void movebackward()
{
  digitalWrite(motor1_f, LOW);
  digitalWrite(motor1_b, HIGH);
  analogWrite(power_motor1, 255);
  digitalWrite(motor2_f, LOW);
  digitalWrite(motor2_b, HIGH);
  analogWrite(power_motor2, 255);
}

void moveright(int left, int right)
{
  Serial.print("moveR left = ");
  Serial.print(left);
  Serial.print(" right = ");
  Serial.println(right);
  digitalWrite(motor1_f, HIGH);
  digitalWrite(motor1_b, LOW);
  analogWrite(power_motor1, right);
  digitalWrite(motor2_f, HIGH);
  digitalWrite(motor2_b, LOW);
  analogWrite(power_motor2, left);
  Serial.println(" ");
}
void moveleft(int left, int right)
{
  Serial.print("moveL left = ");
  Serial.print(left);
  Serial.print(" right = ");
  Serial.println(right);
  digitalWrite(motor1_f, HIGH);
  digitalWrite(motor1_b, LOW);
  analogWrite(power_motor1, right);
  digitalWrite(motor2_f, HIGH);
  digitalWrite(motor2_b, LOW);
  analogWrite(power_motor2, left);
  Serial.println(" ");
}

void stopmotor()
{
 digitalWrite(motor1_f, HIGH);
 digitalWrite(motor1_b, LOW);
 analogWrite(power_motor1, 0);
 digitalWrite(motor2_f, HIGH);
 digitalWrite(motor2_b, LOW);
 analogWrite(power_motor2, 0);
}

// callback for received data
void receiveData(int byteCount){
  while(Wire.available()) {
    message = Wire.read();
    if(int(message)>=44 && int(message)<90){
      //Serial.println(message);
      commandOut = commandOut + String(char(message));//append message to command payload
      if(message == 'E'){
        //Serial.println("newmsg");
        newmessage = 1;
      }
    }
    else{
      
      Serial.println("error");
      commandOut = "";
      newmessage = 0;
    }
  }
}


// callback for sending data
void sendData(){
  if(i==0){
    Wire.write(sendPayload.length());
    //Serial.print("Payload len = ");
    //Serial.println(sendPayload.length());
    //Serial.println(i);
    i++;
  }
  else{
    //Serial.println(i);
    Wire.write(sendPayload[i]);
    i++;
    if(i>sendPayload.length()){
      i=0; //reset counter if it's passed the length of the string
    }
  }
}

