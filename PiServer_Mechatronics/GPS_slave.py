import serial
import testClient

class GPS_SlaveIO:
    def initialize(self):
        self.com = serial.Serial("/dev/ttyUSB0",9600,timeout = 10)
        self.latitude = 0
        self.longitude = 0
    
    def open(self):
        try:
            self.com.open()
        except Exception as e:
            print(e)       
    
    def close(self):
        try:
            self.com.close()
        except:
            print("unable to close port")
    
    def read(self):
        try:
            print(self.com.readline())
            self.splitter = input.split(',')
            print(self.splitter[0])
            if self.splitter[0]=='GPGLL':
                self.latitude = float(self.splitter[1])/100
                self.longitude = float(self.splitter[3]) / 100
                if self.splitter[2] == 'S':
                    self.latitude = self.latitude*-1
                if self.splitter[4] == 'W':
                    self.longitude = self.longitude*-1

        except Exception as e:
            print(e)
myDataSetter = testClient.writeClient()
myPort = serial.Serial("/dev/ttyUSB0",9600,timeout = 10)
while(1):
    input = myPort.readline()
    parser = str(input).split(',')
    if "GPGLL" in parser[0]:
        latitude = float(parser[1])/100
        longitude = float(parser[3]) / 100
        if parser[2] == 'S':
            latitude = latitude*-1
        if parser[4] == 'W':
            longitude = longitude*-1
        print(latitude,longitude)
        myDataSetter.setMessage('setSPosLat',str(latitude))
        myDataSetter.setMessage('setSPosLon',str(longitude))
#testWrite = writeClient()
#testWrite.setMessage('setRStick','123132')
        
