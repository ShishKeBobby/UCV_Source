import serial

class GPS_SlaveIO:
    def __init__(self):
        self.com = serial.Serial("COM8",9600)

    def open(self):
        self.com.open()

    def close(self):
        self.com.close()

    def read(self):
        self.input = self.com.read(2048)
        print(self.input)

    def parser(self):
        self.splitter = self.input.split(',')
        self.latitude = float(self.splitter[1])/100
        self.longitude = float(self.splitter[3]) / 100
        if self.splitter[2] == 'S':
            self.latitude = self.latitude*-1
        if self.splitter[4] == 'W':
            self.longitude = self.longitude*-1



myGPS = GPS_SlaveIO()

myGPS.input = 'GPGLL,4237.48400,N,08308.87964,W'
myGPS.parser()
print(myGPS.latitude, myGPS.longitude)