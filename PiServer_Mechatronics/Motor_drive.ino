// Automotive Mechatronics//
//Project: Unmaned Companion Vehicle//
// This is to control the motor in all three modes: gps, image review, user override//
//Date of completion: Dec 4 , 2017//


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
float pixel = 0;
float radius = 0;
int leftmotor=0;
int rightmotor=0;
String sendPayload;
float sLat = 0;
float sLon = 0;
float sHeading = 0;
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
int azimuth = 0;
float latitude = 0;
float longitude = 0;
float velocity = 0;

//Motor A
int power_motor1 = 6; //power to 1st motor (EN1)
int motor1_f= 12;
int motor1_b= 13;

//Motor B
int power_motor2 = 9;//power to 2nd motor (EN2)
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
  
  //motor stop
  stopmotor();
  
  // initialize i2c as slave
  Wire.begin(SLAVE_ADDRESS);
  
  // define callbacks for i2c communication
  Wire.onReceive(receiveData);
  Wire.onRequest(sendData);  
}


void loop(){
  if(newmessage == 1){
    //Serial.println(commandOut);
     if(commandOut[1]=='A'){
      //Serial.println("A!");
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
      //Serial.println("B!");     
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
      //Serial.println("C!");
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
      //do GPS navigation
      while (Serial1.available() > 0)
      gps.encode(Serial1.read());
      //radio.write("a,14);
      if (gps.location.isUpdated()){
        //while the number of satellites is greater than 4, we only want good data
        numSats = gps.satellites.value();
        azimuth = gps.course.deg();
        latitude = gps.location.lat();
        longitude= gps.location.lng();
        velocity = gps.speed.kmph()*1000/3600;
        //Serial.println(latitude);
        dtostrf(latitude,10,6,lattout);
        dtostrf(longitude,10,6,longout);
        dtostrf(numSats,2,0,satsOut);
        dtostrf(azimuth,3,0,headout);
        dtostrf(velocity,6,3,velOut);
       // Serial.println(slavelatt);
       // Serial.println(slavelong);
       // Serial.println(satsOut);
       // Serial.println(headout);
       // Serial.println(velOut);
       //Serial.println(mLat);
       //Serial.println(mLon);
       //Serial.println(mHeading);
       //makeup some lat lon head until we can implement
       //sLat = 42.123123;
       //sLon = 89.234234;
       //sHeading = 90.5;
       //sendPayload = "A"+String(lattout,9)+","+String(longout,9)+","+String(headout);
       //outputLen = sendPayload.length();
       //Serial.println(sendPayload);
       // char to float
       float slavelatt = atof(lattout);
       float slavelong = atof(longout);
       float slavehead = atof(headout);
       float slave_vel = atof(velOut);
       sendPayload = "A"+String(slavelatt,9)+","+String(slavelong,9)+","+String(slavehead);
       outputLen = sendPayload.length();
       //Serial.println(sendPayload);
       //Convert degreeto radian//
       float masterlatt_rad = masterlatt * 0.0174533;
       float masterlong_rad = masterlong * 0.0174533;
       float slavelatt_rad = slavelatt * 0.0174533;
       float slavelong_rad = slavelong * 0.0174533;
       //Distance between slave and master
       float delta_latt = ( masterlatt_rad - slavelatt_rad);
       float delta_long = ( masterlong_rad - slavelong_rad);
       float a_rad = (1-cos(delta_latt))/2 + (cos(slavelatt_rad) * cos(masterlatt_rad)* (1-cos(delta_long))/2);
       float c_rad = 2 * atan2( sqrt(a_rad),sqrt(1- a_rad));
       float Distance_km = 6371 * c_rad ;
       float Distance_m = Distance_km *1000 ;
       //angle between slave and master
       float bearing = masterhead - slavehead;
       float masterhead_1 = map(masterhead, 0, 360, 0, 4000); 
      // float materhead_theta = 90 -masterhead;// in degree
       //float materhead_theta_1 = map(materhead_theta, 0, 360, 0, 4000); 
      // int angle_move_clk = map(bearing,0 , 360, 0, 4000);  /////check once???
      // int angle_move_ant = map(bearing, -1,-359, 0, 4000);
       float time_slave = (Distance_m / slave_vel); //m/(m/sec)= sec
       float masterlatt_rad_1= masterlatt_rad - 00.000002;
       if((masterlatt_rad_1 == slavelatt_rad) &&( masterlong_rad == slavelong_rad)){
        stopmotor();
       }
       else {
        //move slave to angle clockwise 
        moveright(255,0); //(left val, right val)
        delay(int(masterhead_1));
        while( masterlatt_rad_1 != slavelatt_rad){
        //move forward
         moveforward(); 
        }
        if(masterlong > slavelong){
          moveright(255, 0);
          delay(int(2000 - masterhead_1));  // 90- theta
          while( masterlong_rad !=slavelong_rad){
          //move forward
          moveforward(); 
          }
          stopmotor();
        }
        else{
          moveleft(0, 255);
          delay(int(2000 + masterhead_1));  // 90+ theta
          while( slavelong_rad !=slavelong_rad){
          //move forward
          moveforward(); 
          }
         stopmotor(); 
        }
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
     else if(pixel > 97 && pixel <234)
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
    
     
     //do user override
     //Serial.println(leftMotor);
     //Serial.println(rightMotor);
      if((rightmotor > 255) &&(leftmotor >255)){
      Serial.println("1");// move back
      motor_speed2 = map(rightmotor, 256, 510, 0, 255);
      motor_speed1 = map(leftmotor, 256, 510, 0, 255); 
      Serial.println(motor_speed1);
      Serial.println(motor_speed2);
      digitalWrite(motor1_f, LOW); //move forward
      digitalWrite(motor1_b, HIGH);
      analogWrite(power_motor1, motor_speed1);
      digitalWrite(motor2_f, LOW);
      digitalWrite(motor2_b, HIGH);
      analogWrite(power_motor2, motor_speed2);  
     }
     else if((rightmotor < 254) &&(leftmotor < 254)){
      Serial.println("2"); //move forward
      motor_speed2 = map(rightmotor, 253, 0, 0, 255);
      motor_speed1 = map(leftmotor, 253, 0, 0, 255); 
      Serial.println(motor_speed1);
      Serial.println(motor_speed2);
      digitalWrite(motor1_f, HIGH); // move backward
      digitalWrite(motor1_b, LOW);
      analogWrite(power_motor2, motor_speed1);
      digitalWrite(motor2_f, HIGH);
      digitalWrite(motor2_b, LOW);
      analogWrite(power_motor1, motor_speed2);  
     }
      else if((rightmotor < 255) &&(leftmotor > 255)){
      Serial.println("3");// left
      motor_speed1 = map(rightmotor, 254, 0, 0, 255);
      motor_speed2 = map(leftmotor, 256, 510, 0, 255);
      Serial.println(motor_speed1);
      Serial.println(motor_speed2); 
      digitalWrite(motor1_f, HIGH);//move left
      digitalWrite(motor1_b, LOW);
      analogWrite(power_motor1, motor_speed1);
      digitalWrite(motor2_f, HIGH);
      digitalWrite(motor2_b, LOW);
      analogWrite(power_motor2, motor_speed2);  
     }
     else if((rightmotor > 255) &&(leftmotor < 255)){
      Serial.println("4");//right
      motor_speed2 = map(rightmotor, 256, 510, 0, 255);
      motor_speed1 = map(leftmotor, 254, 0, 0, 255);
      Serial.println(motor_speed1);
      Serial.println(motor_speed2); 
      digitalWrite(motor1_f, HIGH);//move right
      digitalWrite(motor1_b, LOW);
      analogWrite(power_motor1, motor_speed1);
      digitalWrite(motor2_f, HIGH);
      digitalWrite(motor2_b, LOW);
      analogWrite(power_motor2, motor_speed2);  
     }
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
     // Serial.println(message);
      commandOut = commandOut + String(char(message));//append message to command payload
      if(message == 'E'){
        //Serial.println("newmsg");
        newmessage = 1;
      }
    }
    else{
      
      //Serial.println(int(message));
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

