import serial
import time

tempHold = ""
ser = serial.Serial('/dev/ttyUSB0',9600, timeout=1)
while(1):
    tempHold = ser.readline().decode()
    print("total = "+tempHold)
    tempHold = tempHold.split(",")
    try:
        if "GPVTG" in tempHold[0]:
            print("heading = "+tempHold[1])
        elif "GPGLL":
            print("latitude = " + tempHold[1])
            print("longitude = "+ tempHold[2])
        
    except:
        print(tempHold)


