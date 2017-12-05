import RPi.GPIO as GPIO
from lib_nrf24 import NRF24
import time
import spidev

GPIO.setmode(GPIO.BCM)

pipes = [[0xE8, 0xE8, 0xF0,0xF0, 0xE1],[0xF0,0xF0,0xF0,0xF0,0xE1]]

radio = NRF24(GPIO, spidev.SpiDev())
radio.begin(0, 17)

radio.setPayloadSize(32)
radio.setChannel(0x76)
radio.setDataRate(NRF24.BR_1MBPS)
radio.setPALevel(NRF24.PA_MIN)

radio.setAutoAck(True)
radio.enableDynamicPayloads()
radio.enableAckPayload()

radio.openReadingPipe(1, pipes[1])
radio.printDetails()
radio.startListening()

while True:
	while not radio.available():
		time.sleep(1/100)
	receivedMessage = []
	radio.read(receivedMessage, radio.getDynamicPayloadSize())
	string = " "
	for n in receivedMessage:
		if(n >=32 and n <= 126):
			string += chr(n)
	
	string = string.strip(' \t\n\r')
	if string.endswith('a'):
		string = string[:-1]
		print("latitude ="+string)
	elif string.endswith('o'):
		string = string[:-1]
		print("longitude ="+string)
	elif string.endswith('m'):
		string = string[:-1]
		print("heading ="+string)
	elif string.endswith('v'):
		string = string[:-1]
		print("velocity ="+string)
	elif string.endswith('s'):
		string = string[:-1]
		print("sats ="+string)
	else:
		print("ERROR:"+string)