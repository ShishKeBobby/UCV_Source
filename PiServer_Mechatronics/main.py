from random import *
import socket
import subprocess
import time
class TCPInteraction:

    def __init__(self):
        self.s = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        self.s.setsockopt(socket.SOL_SOCKET, socket.SO_REUSEADDR, 1)
        self.addr = ""
        self.port = 9080
        self.serverAddr = (self.addr, self.port)
        self.s.bind(self.serverAddr)
        self.s.listen(5)

    def piServer(self):
        #initialize variables to pass around
                self.mPosLat = 0
                self.mPosLon = 0
                self.heading = 0
                self.sHeading = 0
                self.mHeading = 0
                self.sPosLat = 0
                self.sPosLon = 0
                self.magGPS = 0
                self.imgDistance = 0
                self.imgHeading = 0
                self.userOverride = 0
                self.leftStick = 0
                self.rightStick = 0
                # set fail counts and timeout vals
                # begin mainloop
                while True:
                    # attempt to receiver command
                    print("waiting...")
                    conn, addr = self.s.accept()
                    print("Command received")
                    self.commandInput = conn.recv(1024).decode()
                    print(self.commandInput)
                    if self.commandInput == "getMPosLat":
                        conn.send(self.mPosLat) #send master position

                    elif self.commandInput == "setMPosLat":
                        self.mPosLat = conn.recv(4096) #set master position

                    if self.commandInput == "getMPosLon":
                        conn.send(self.mPosLon) #send master position

                    elif self.commandInput == "setMPosLon":
                        self.mPosLon = conn.recv(4096) #set master position

                    elif self.commandInput == "getSPosLat":
                        conn.send(self.sPosLat) #send master position

                    elif self.commandInput == "setSPosLat":
                        self.sPosLat = conn.recv(4096) #set master position

                    elif self.commandInput == "getSPosLon":
                        conn.send(self.sPos)  # send master position

                    elif self.commandInput == "setSPosLon":
                        self.sPos = conn.recv(4096)  # set master position

                    elif self.commandInput == "getHeading":
                        conn.send(self.heading) #send master position

                    elif self.commandInput == "setHeading":
                        self.heading = conn.recv(4096) #set master position

                    elif self.commandInput == "getMagGPS":
                        conn.send(self.magGPS) #send master position

                    elif self.commandInput == "setMagGPS":
                        self.magGPS = conn.recv(4096) #set master position

                    elif self.commandInput == "getImgDist":
                        conn.send(self.imgDistance) #send master position

                    elif self.commandInput == "setImgDist":
                        self.imgDistance = conn.recv(4096) #set master position

                    elif self.commandInput == "getImgHeading":
                        conn.send(self.sPos) #send master position

                    elif self.commandInput == "setImgHeading":
                        self.sPos = conn.recv(4096) #set master position

                    elif self.commandInput == "getMHeading":
                        conn.send(self.mHeading) #send master position

                    elif self.commandInput == "setMHeading":
                        self.mHeading = conn.recv(4096) #set master position

                    elif self.commandInput == "getSHeading":
                        conn.send(self.sHeading) #send master position

                    elif self.commandInput == "setSHeading":
                        self.sHeading = conn.recv(4096) #set master position

                    elif self.commandInput == "getRStick":
                        conn.send(self.rightStick) #send master position

                    elif self.commandInput == "setRStick":
                        self.rightStick = conn.recv(4096) #set master position

                    elif self.commandInput == "getLStick":
                        conn.send(self.leftStick) #send master position

                    elif self.commandInput == "setLStick":
                        self.leftStick = conn.recv(4096) #set master position

                    elif self.commandInput == "setUserOverride":
                        self.userOverride = conn.recv(4096) #set master position

                    elif self.commandInput == "getUserOverride":
                        conn.send(self.userOverride) #send master position

                    elif self.commandInput == "rand":
                        conn.send(str(random()).encode())

                    elif self.commandInput == 'restart':
                        conn.send('ack1')
                        subprocess.call('sudo reboot', shell=True)
                    elif self.commandInput == 'shutdown':
                        conn.send('ack1')
                        subprocess.call('sudo shutdown now', shell=True)
                    elif self.commandInput == 'terminal':
                        conn.send('trml')
                        payload = conn.recv(4096)
                        outPut1 = subprocess.check_output(payload, shell=True)
                        #prepend data send of N bytes with byte size
                        conn.send(outPut1)



#start server....
tcpStuff = TCPInteraction()
tcpStuff.piServer()