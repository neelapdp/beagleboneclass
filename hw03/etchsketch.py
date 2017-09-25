
#!/usr/bin/python3


#written by Daniel Neelappa 9/3/17
#Daniel Neelappa 9/9/17: interfacing with board, adding buttons
#NOTE: Set P9_28 and P9_23 to pull up resistors for correct function
import sys 
import Adafruit_BBIO.GPIO as GPIO
import time
import smbus

#i2c setup
bus = smbus.SMBus(1)  # Use i2c bus 1
matrixConnection = 0x70         # Use address 0x70
tempAddress = 0x49


#set up matrix display
bus.write_byte_data(matrixConnection, 0x21, 0)   # Start oscillator (p10)
bus.write_byte_data(matrixConnection, 0x81, 0)   # Disp on, blink off (p11)
bus.write_byte_data(matrixConnection, 0xe7, 0)   # Full brightness (page 15)


display = [0x01, 0x00, 0x00, 0x00, 0x00, 0x00, 0x00, 0x00,
    0x00, 0x00, 0x00, 0x00, 0x00, 0x00, 0x00, 0x00
]
bus.write_i2c_block_data(matrixConnection, 0, display)

#prevent errors by cleaning Pins first
GPIO.cleanup()

#variables for LED's and buttons
buttons = ['GP0_6', 'GP0_5', 'GP0_4', 'GP0_3', 'PAUSE']

     
#Set up GPIO for Buttons
for i in range(len(buttons)):
    GPIO.setup(buttons[i], GPIO.IN)

#different callback structures, seperate functions for later adaptation to encoders
def buttonMoveUp(channel):
    move(-1,0)
    updateMove()
    drawBoard()

def buttonMoveDown(channel):
    move(1,0)
    updateMove()
    drawBoard()


def buttonMoveLeft(channel):
    move(0,-1)
    updateMove()
    drawBoard()
    
def buttonMoveRight(channel):
    move(0,1)
    updateMove()
    drawBoard()

def buttonReset(channel):
    clearBoard()
    updateMove()
    drawBoard()

#assign callbacks
GPIO.add_event_detect(buttons[0], GPIO.FALLING, callback=buttonMoveUp)
GPIO.add_event_detect(buttons[1], GPIO.FALLING, callback=buttonMoveDown)
GPIO.add_event_detect(buttons[2], GPIO.FALLING, callback=buttonMoveLeft)
GPIO.add_event_detect(buttons[3], GPIO.FALLING, callback=buttonMoveRight)
GPIO.add_event_detect(buttons[4], GPIO.FALLING, callback = buttonReset)
#function designed to draw the updated board
def drawBoard():
    global Matrix
    global matrixConnection
    global display
    isleCount = 0 
    #draw horizontal isle indicators
    sys.stdout.write("  ")
    while (isleCount != tileCount):
        col = " " + str(isleCount)
        sys.stdout.write(col)
        isleCount = isleCount + 1
    sys.stdout.write('\n')
    
    #now go row by row and print row indicator and x or '' at each spot
    rowCount = 0
    while (rowCount != tileCount):
        rowlabel = str(rowCount) + ":"
        sys.stdout.write(rowlabel)
        isleCount = 0
        while (isleCount != tileCount):
            tileSpace = " " + str(Matrix[rowCount][isleCount])
            sys.stdout.write(tileSpace)
            isleCount = isleCount + 1
        sys.stdout.write('\n')
        rowCount = rowCount + 1
        
        #handle matrix display
    bus.write_i2c_block_data(matrixConnection, 0, display)

#clear the board
def clearBoard():
    global Matrix
    global display
    global matrixConnection
    rowCount = 0 #go row by row, and blank each tile
    while (rowCount != tileCount):
        isleCount = 0
        while (isleCount != tileCount):
            Matrix[rowCount][isleCount] = ' '
            isleCount = isleCount + 1
        rowCount = rowCount + 1
    for i in range(0,15):
        display[i] = 0
    bus.write_i2c_block_data(matrixConnection, 0, display)


#moves your position based on args
def move(y,x):
    global posx
    global posy
    global display


    #create orange square
    displayBit = 128
    displayBit = displayBit >> posy
    index = posx * 2 + 1
    display[index] = displayBit | display[index]
    
    Matrix[posy][posx] = 'x' #have the previous position become a x
    #makes sure move is valid
    if ( ((posy + y) >= 0) and ((posy + y) <= (tileCount -1)) ):
        posy = posy + y
    if ( ((posx + x) >= 0) and ((posx + x) <= (tileCount -1)) ):
        posx = posx + x

    #reset to make current position green
    displayBit = 65407
    displayBit = displayBit >> posy
    index = posx * 2 + 1
    display[index] = displayBit & display[index]   

#draws x at the current position
def updateMove():
    global posx
    global posy
    global Matrix
    global display
    global matrixConnection

    displayBit = 128
    displayBit = displayBit >> posy
    index = posx * 2
    display[index] = displayBit | display[index]
    Matrix[posy][posx] = 'o'

#print intro line
print("Etch Sketch program\nDaniel Neelappa -V.1 9/1/17\n")



tileCount = -1



# ask for tile dim.'s and verify for valid number, defaults to 8by8 if number is 0 or negative
try:
	tileCount = int(input("How many tiles would you like?"))
	if (tileCount <=0):
		print("Not valid number. Setting Default to 8.")
		tileCount = 8

except ValueError:
	print("Not a Number")
	sys.exit(1)

#print instructions
print ("Tile Count is ", tileCount, "by", tileCount, ".")
print ("To move left:press a.\nTo move right:press d.\nTo move up:press w.\nTo move down:press s\nYou can also combine directions like aw, as, dw, ds.\n Type clear to wipe the board\nThen press enter to confirm.")
print("Type \"exit\" to quit program")

#declare matrix and initialize it to blanks
Matrix = [[0 for x in range(tileCount)] for y in range(tileCount)]
clearBoard()

#add some spacing between grid and instructions
print("\n\n\n")

#cursor location
posx = 0
posy = 0

#draw the board first
updateMove()
drawBoard()


#user prompt for interaction
#user now can press any four buttons to select movement
while (True):
    try:
        time.sleep(1)
        #perform temp fading
        temp = (bus.read_byte_data(tempAddress, 0) - 22)
        print("temp:", temp)
        bus.write_byte_data(0x70, temp + 0xe0, 0)
    except KeyboardInterrupt:
        print("Cleaning up")
        GPIO.cleanup()
        sys.close(0)
GPIO.cleanup()#reset pins used
