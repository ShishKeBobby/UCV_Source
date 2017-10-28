import socket


class client:
    def sendMessage(self, message):
        #self.send(message)
        message = 'rand'
        host = socket.gethostname()
        port = 9080                  # The same port as used by the server
        s = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        s.connect((host, port))
        s.sendall(message.encode())
        self.data = s.recv(1024).decode()
        s.close()
        return self.data

myClient = client()
testMessage = 'rand'
myClient.sendMessage(testMessage)
print(myClient.data)
