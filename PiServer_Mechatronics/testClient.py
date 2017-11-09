import socket
import time

class readClient:
    def readData(self, command):
        #self.send(message)
        #command = 'rand'
        #host = socket.gethostname()
        host = '192.168.0.10'
        port = 9080                  # The same port as used by the server
        s = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        s.connect((host, port))
        s.sendall(command.encode())
        self.data = s.recv(1024).decode()
        s.close()
        return self.data

class writeClient:
    def setMessage(self,command,message):
        #host = socket.gethostname()
        host = '192.168.0.10'
        port = 9080
        s = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        s.connect((host, port))
        #send command to set appropriate if else condition
        s.sendall(command.encode())
        time.sleep(.1)
        #send information for the socket
        s.sendall(message.encode())
        #should be good now
        s.close()

#testWrite = writeClient()
#testWrite.setMessage('setRStick','123132')
#myClient = readClient()
#myClient.readData('getRStick')
#print(myClient.data)
