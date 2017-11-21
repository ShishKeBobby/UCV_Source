#launcher

from subprocess import Popen

Popen("/home/pi/Desktop/UCV_Source/PiServer_Mechatronics/cameraClient.py")
print('launched camera')
Popen("/home/pi/Desktop/UCV_Source/PiServer_Mechatronics/rfGPSReceiver.py")
print('launched rf')
Popen("/home/pi/Desktop/UCV_Source/PiServer_Mechatronics/mainSlave.py")
print('launched main')