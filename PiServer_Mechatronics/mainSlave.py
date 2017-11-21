import testClient
import time
import navigation
import serial
#create getters for all of the important server data
navigator = navigation.navigate()
myClient = testClient.readClient()
writeClient = testClient.writeClient()
payload = ""
sleepVar = .9
try:
    ser = serial.Serial('/dev/ttyACM0',115200, timeout=10)
except:
    try:
        ser = serial.Serial('/dev/ttyACM1',115200, timeout=10)
    except:
        pass
while(1):
    try:
        #ready = ser.readline(); #blocking function until Ard. is ready
        #print(ready)
        userOverride = int(myClient.readData('getUserOverride'))
        radius = int(float(myClient.readData('getImgDist')))
        if userOverride == 1:
            #user override enabled, pull
            lStick = float(myClient.readData('getLStick'))*255
            rStick = float(myClient.readData('getRStick'))*255
            lastPayload = payload
            payload = 'c'+str(int(lStick))+'Z'+str(int(rStick))
            if payload != lastPayload:
                ser.write(payload.encode())
                print('User ='+payload)
                time.sleep(2)
            else:
                pass
        elif radius > 20:
            #radius in known
            xPos = int(float(myClient.readData('getImgHeading')))
            #now send info to arduino
            lastPayload = payload
            payload = 'b'+str(xPos) +'Z'+str(radius)
            if payload != lastPayload:
                ser.write(payload.encode())
                print('image ='+payload)
		time.sleep(sleepVar)
            else:
                pass
        else:
            masterHeading = myClient.readData('getMHeading')
            #slaveHeading = myClient.readData('getSHeading')
            #latS = myClient.readData('getSPosLat')
            #lonS = myClient.readData('getSPosLon')
            latM = myClient.readData('getMPosLat')
            lonM = myClient.readData('getMPosLon')
            #navigator.heading(latS,lonS,latM,lonM,masterHeading,slaveHeading)
            #newBearing = navigator.headingDeg
            #newDistance = navigator.distanceToTravel
            #writeClient.setMessage('setMagGPS',newDistance)
            #writeClient.setMessage('setHeading',newBearing)
            #we have a heading and a distance, we can either
            #convert directly to motor signal or pass these terms
            #to the arduino and let Priya figure it out
            #possible to indicate if it's a distance + angle or user inputs?
            #serial.writetoarduino(GPS stuff);
            payload = 'a'+latM + 'Z'+lonM + 'Z' + masterHeading
            ser.write(payload.encode())
            print('lat/lon= '+payload)
            time.sleep(2)
        
    except Exception as e:
        print(e)
        time.sleep(1)
        try:
            ser = serial.Serial('/dev/ttyACM0',115200, timeout=1)
        except:
            try:
                ser = serial.Serial('/dev/ttyACM1',115200, timeout=1)
            except:
                pass
