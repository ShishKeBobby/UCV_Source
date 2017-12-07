#include <TinyGPS++.h>
#include<SPI.h>
#include<RF24.h>

/*
   This sample code demonstrates the normal use of a TinyGPS++ (TinyGPSPlus) object.
   It requires the use of SoftwareSerial, and assumes that you have a
   4800-baud serial GPS device hooked up on pins 4(rx) and 3(tx).
*/
//static const int RXPin = 4, TXPin = 3;
//static const uint32_t GPSBaud = 4800;

// The TinyGPS++ object
RF24 radio(7,8);
TinyGPSPlus gps;
char latOut[15];
char lonOut[15];
char satsOut[10];
char velOut[10];
char headOut[10];
int numSats = 0;
int azimuth = 0;
float latitude = 0;
float longitude = 0;
float velocity = 0;

// The serial connection to the GPS device
//SoftwareSerial ss(RXPin, TXPin);

void setup()
{
  Serial.begin(9600);
  Serial1.begin(9600);
  radio.begin();
  radio.setPALevel(RF24_PA_MAX);
  radio.setChannel(0x76);
  radio.openWritingPipe(0xF0F0F0F0E1LL);
  radio.enableDynamicPayloads();
  radio.powerUp();
}

void loop()
{
    while (Serial1.available() > 0)
    gps.encode(Serial1.read());
    //radio.write("a,14);
  if (gps.location.isUpdated())
  {
    //while the number of satellites is greater than 4, we only want good data
    numSats = gps.satellites.value();
    azimuth = gps.course.deg();
    latitude = gps.location.lat();
    longitude= gps.location.lng();
    velocity = gps.speed.kmph()*1000/3600;
    //Serial.println(latitude);
    Serial.println(azimuth);
    dtostrf(latitude,10,6,latOut);
    dtostrf(longitude,10,6,lonOut);
    dtostrf(numSats,2,0,satsOut);
    dtostrf(azimuth,3,0,headOut);
    dtostrf(velocity,6,3,velOut);
    transmit();
    //call function to send new data
  }
  

}

// This custom version of delay() ensures that the gps object
// is being "fed".
static void smartDelay(unsigned long ms)
{
  unsigned long start = millis();
  do 
  {
    while (Serial1.available())
      gps.encode(Serial1.read());
  } while (millis() - start < ms);
}

static void printFloat(float val, bool valid, int len, int prec)
{
  if (!valid)
  {
    while (len-- > 1)
      Serial.print('*');
    Serial.print(' ');
  }
  else
  {
    Serial.print(val, prec);
    int vi = abs((int)val);
    int flen = prec + (val < 0.0 ? 2 : 1); // . and -
    flen += vi >= 1000 ? 4 : vi >= 100 ? 3 : vi >= 10 ? 2 : 1;
    for (int i=flen; i<len; ++i)
      Serial.print(' ');
  }
  smartDelay(0);
}

static void printInt(unsigned long val, bool valid, int len)
{
  char sz[32] = "*****************";
  if (valid)
    sprintf(sz, "%ld", val);
  sz[len] = 0;
  for (int i=strlen(sz); i<len; ++i)
    sz[i] = ' ';
  if (len > 0) 
    sz[len-1] = ' ';
  Serial.print(sz);
  smartDelay(0);
}

static void printDateTime(TinyGPSDate &d, TinyGPSTime &t)
{
  if (!d.isValid())
  {
    Serial.print(F("********** "));
  }
  else
  {
    char sz[32];
    sprintf(sz, "%02d/%02d/%02d ", d.month(), d.day(), d.year());
    Serial.print(sz);
  }
  
  if (!t.isValid())
  {
    Serial.print(F("******** "));
  }
  else
  {
    char sz[32];
    sprintf(sz, "%02d:%02d:%02d ", t.hour(), t.minute(), t.second());
    Serial.print(sz);
  }

  printInt(d.age(), d.isValid(), 5);
  smartDelay(0);
}

static void printStr(const char *str, int len)
{
  int slen = strlen(str);
  for (int i=0; i<len; ++i)
    Serial.print(i<slen ? str[i] : ' ');
  smartDelay(0);
}

void transmit(){
//    dtostrf(latitude,10,6,latOut);
//    dtostrf(longitude,10,6,lonOut);
//    dtostrf(numSats,2,0,satsOut);
//    dtostrf(azimuth,3,0,headOut);
//    dtostrf(velocity,6,3,velOut);
  //all of the variables are globals, no need to pass anything in
  //radio.write("hello",6);
  //radio.write('st',5);
  char appender[15];
  char indicator[1];
  indicator[0]='a';
  memset(appender,0,sizeof(appender));
  sprintf(appender,"%s%s",latOut,indicator);
  radio.write(appender,14);
  indicator[0]='o';
  sprintf(appender,"%s%s",lonOut,indicator);
  radio.write(appender,14);
  indicator[0]='m';
  memset(appender,0,sizeof(appender));
  sprintf(appender,"%s%s",headOut,indicator);
  radio.write(appender,10);
  indicator[0]='v';
  memset(appender,0,sizeof(appender));
  sprintf(appender,"%s%s",velOut,indicator);
  radio.write(appender,10);
  indicator[0]='s';
  memset(appender,0,sizeof(appender));
  sprintf(appender,"%s%s",satsOut,indicator);
  radio.write(appender,10);
}

