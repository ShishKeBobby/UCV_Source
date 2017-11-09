import testClient
import time
import navigation
#create getters for all of the important server data
navigator = navigation.navigate()
myClient = testClient.readClient()
writeClient = testClient.writeClient()
while(1):
    userOverride = myClient.readData('getUserOverride')
    if userOverride == 1:
        #user override enabled, pull
        lStick = myClient.readData('getLStick')
        rStick = myClient.readData('getRStick')
    else:
        masterHeading = myClient.readData('getMHeading')
        slaveHeading = myClient.readData('getSHeading')
        latS = myClient.readData('getSPosLat')
        lonS = myClient.readData('getSPosLon')
        latM = myClient.readData('getMPosLat')
        lonM = myClient.readData('getMPosLon')
        navigator.heading(latS,lonS,latM,lonM,masterHeading,slaveHeading)
        newBearing = navigator.headingDeg
        newDistance = navigator.distanceToTravel
        writeClient.setMessage('setMagGPS',newDistance)
        writeClient.setMessage('setHeading',newBearing)
        #we have a heading and a distance, we can either
        #convert directly to motor signal or pass these terms
        #to the arduino and let Priya figure it out
        #possible to indicate if it's a distance + angle or user inputs?
        #serial.writetoarduino(GPS stuff);
