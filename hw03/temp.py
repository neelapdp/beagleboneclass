#!/usr/bin/env python3
#Read a TMP101 sensor
#sudo apt install python3-smbus

import smbus
import time
import Adafruit_BBIO.GPIO as GPIO

bus = smbus.SMBus(1)

address = 0x49

def updatePinState(channel):
    print("State toggled on:", channel)

#Set pin configuration
GPIO.setup("GP0_6", GPIO.IN)
GPIO.add_event_detect("GP0_6", GPIO.FALLING, callback=updatePinState)

while True:
	temp = bus.read_byte_data(address, 0)
	print(temp, end="\r")
	try:
		time.sleep(1)
	except ():
		print("error with sleeping")
