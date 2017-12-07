import testClient
import time
import navigation
import smbus
import time
bus = smbus.SMBus(1)

#create getters for all of the important server data
navigator = navigation.navigate()
myClient = testClient.readClient()
writeClient = testClient.writeClient()
payload = ""
sleepVar = .9
address = 0x04
xPos = 0
def writeNumber(value):
    bus.write_byte(address, value)
# bus.write_byte_data(address, 0, value)
    return -1

def readNumber():
    number = bus.read_byte(address)
    #block = bus.read_block_data(address,1)
# number = bus.read_byte_data(address, 1)
    return number

while(1):
    #print("entry")
    time.sleep(.2)
    try:
        #ready = ser.readline(); #blocking function until Ard. is ready
        #print(ready)
        userOverride = int(myClient.readData('getUserOverride'))
        imgHold = myClient.readData('getImgDist')
        try:
            imgHold = imgHold.split(",")
            radius = int(float(imgHold[0]))
            xPos = int(float(imgHold[1]))
        except:
            radius = 0
            xPos = 0

        if userOverride == 1:
            #user override enabled, pull
            lStick = float(myClient.readData('getLStick'))*255+255
            rStick = float(myClient.readData('getRStick'))*255+255
            lastPayload = payload
            payload = "SC"+str(int(lStick))+','+str(int(rStick))+"E"
	    print(payload)
            #if payload != lastPayload:
            for each in payload:
                writeNumber(ord(each))
            time.sleep(.1)
            #else:
            #    pass
        elif radius > 20:
            #radius in known
            #xPos = int(float(myClient.readData('getImgHeading')))
            print("X = "+str(xPos/2)+ " R = "+str(radius/2))
            #now send info to arduino
            lastPayload = payload
            payload = 'SB'+str(xPos/2) +','+str(radius/2)+"E"
            if payload != lastPayload:
                for each in payload:
                    writeNumber(ord(each))
                time.sleep(.01)
            else:
                pass
        else:
            #print("check-gps")
            masterHeading = myClient.readData('getMHeading')
            masterHeading = masterHeading.strip()
            #slaveHeading = myClient.readData('getSHeading')
            #latS = myClient.readData('getSPosLat')
            #lonS = myClient.readData('getSPosLon')
            latM = myClient.readData('getMPosLat')
            lonM = myClient.readData('getMPosLon')
            latM = latM.strip()
            lonM = lonM.strip()
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
            lastPayload = payload
            payload = 'SA'+latM + ','+lonM + ',' + masterHeading+"E"
            #print(payload)
            if payload == payload:
                print(payload)
                for each in payload:
                    writeNumber(ord(each))
                time.sleep(.4)
                #pull slave Lat/Lon/Heading
                number = int(readNumber())
                print("index = " + str(number))
                output = ""
                for i in range(0,number):
                    output = output + chr(readNumber())
                    time.sleep(.01)
                print(output)
                data = output.split(',')
                print(data)
                sLat = data[0]
                sLon = data[1]
                sHead = data[2]
                print(sLat)
                print(sLon)
                print(sHead)
            else:
                pass
       
    except Exception as e:
        print("error")
        print(e)
        time.sleep(1)
        
