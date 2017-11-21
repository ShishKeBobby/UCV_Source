import serial
import time
ser = serial.Serial('/dev/ttyACM0',9600, timeout=1)
lStick = .5*127+127
rStick = .25*127+127
#command = 'c' + str(int(lStick)) + 'Z' + str(int(rStick))
command = 'hello'
print(command.encode())
while(1):
    command = str(input('gimmi a command '))
    ser.write(command.encode())
    if command.startswith("a"):
        print(ser.readline().decode())

        print(ser.readline().decode())

        print(ser.readline().decode())
    elif command.startswith("b"):

        print(ser.readline().decode())

        print(ser.readline().decode())

    elif command.startswith("c"):

        print(ser.readline().decode())

        print(ser.readline().decode())
ser.close()

#from time import sleep
#import serial
#ser = serial.Serial('COM6', 9600) # Establish the connection on a specific port
#counter = 32 # Below 32 everything in ASCII is gibberish
#while True:
#     counter +=1
#     ser.write(str(chr(counter))) # Convert the decimal number to ASCII then send it to the Arduino
#     print(ser.readline()) # Read the newest output from the Arduino
#     sleep(.1) # Delay for one tenth of a second
#     if counter == 255:
#        counter = 32
