import smbus
import time
bus = smbus.SMBus(1)

# This is the address we setup in the Arduino Program
address = 0x04
message = "SA42.234213,88.123331,120.5E"
message2 = "SB320,100E"
message3 = "SC128,128E"
def writeNumber(value):
    bus.write_byte(address, value)
# bus.write_byte_data(address, 0, value)
    return -1

def readNumber():
    number = bus.read_byte(address)
    #block = bus.read_block_data(address,1)
# number = bus.read_byte_data(address, 1)
    return number

while True:
    try:
        for each in message:
            writeNumber(ord(each))
        time.sleep(.3)
        
        #for each in message2:
        #    writeNumber(ord(each))
        #sleep one second
        #time.sleep(.3)
        
        
        #for each in message3:
        #    writeNumber(ord(each))
        #time.sleep(.3)
        number = int(readNumber())
        output = ""
        for i in range(0,number):
            output = output + chr(readNumber())
            time.sleep(.01)
        data = output.split(',')
        sLat = data[0]
        sLon = data[1]
        sHead = data[2]
        print(sLat)
        print(sLon)
        print(sHead)
        print("Arduino: Hey RPI, I received a digit ", number)
        print(output)
    except Exception as e:
        time.sleep(.1)
        print(e)
