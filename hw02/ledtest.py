#!/usr/bin/env python3

import Adafruit_BBIO.GPIO as GPIO
import time

#prevent errors by cleaning Pins first
GPIO.cleanup()

#variables for LED's and buttons
leds = ['GREEN', 'RED', 'GP1_4', 'GP1_3']
buttons = ['GP0_6', 'GP0_5', 'GP0_4', 'MODE']

#Set up GPIO for LED's
for i in range(len(leds)):
    GPIO.setup(leds[i], GPIO.OUT)
    
#Set up GPIO for Buttons
for i in range(len(buttons)):
    GPIO.setup(buttons[i], GPIO.IN)

#Map buttons to LED's
map = {} #hashmap buttons to leds
for i in range(len(buttons)):
    map[buttons[i]] = leds[i]

#blink LED's when buttons are pressed
def updateLED(channel):
    print("channel = " + channel)
    state = GPIO.input(channel)
    GPIO.output(map[channel], state)
    print(map[channel] + " Toggled")

#attach interrupts to GPIO pins
for i in range(len(buttons)):
    GPIO.add_event_detect(buttons[i], GPIO.BOTH, callback=updateLED)

try:
    while True:
        time.sleep(100) #Keep programming running

except KeyboardInterrupt:
    print("Cleaning up")
    GPIO.cleanup()
GPIO.cleanup()
    