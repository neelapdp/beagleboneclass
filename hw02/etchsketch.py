
#!/usr/bin/env python3


#written by Daniel Neelappa 9/3/17
#Daniel Neelappa 9/9/17: interfacing with board
import sys


 
import Adafruit_BBIO.GPIO as GPIO
import time

#prevent errors by cleaning Pins first
GPIO.cleanup()

#variables for LED's and buttons
buttons = ['GP0_6', 'PAUSE', 'GP0_4', 'MODE']

     
#Set up GPIO for Buttons
for i in range(len(buttons)):
    GPIO.setup(buttons[i], GPIO.IN)





#function designed to draw the updated board
def drawBoard():
    global Matrix
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

#clear the board
def clearBoard():
    global Matrix
    rowCount = 0 #go row by row, and blank each tile
    while (rowCount != tileCount):
        isleCount = 0
        while (isleCount != tileCount):
            Matrix[rowCount][isleCount] = ' '
            isleCount = isleCount + 1
        rowCount = rowCount + 1

#moves your position based on args
def move(y,x):
    global posx
    global posy
    #makes sure move is valid
    if ( ((posy + y) >= 0) and ((posy + y) <= (tileCount -1)) ):
        posy = posy + y
    if ( ((posx + x) >= 0) and ((posx + x) <= (tileCount -1)) ):
        posx = posx + x

#draws x at the current position
def updateMove():
    global posx
    global posy
    global Matrix
    Matrix[posy][posx] = 'x'

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
while (True):
    try:
        
        if (GPIO.input(buttons[0]) and GPIO.input(buttons[1]) == 0 and GPIO.input(buttons[2]) and GPIO.input(buttons[3]) == 0):
            clearBoard()
            print("cleared")
        elif (GPIO.input(buttons[3]) == 0 and GPIO.input(buttons[2])):
            move(-1,-1)
            print("moved 1")
        elif (GPIO.input(buttons[2]) and GPIO.input(buttons[1]) == 0):
            move(-1,1)
            print("moved 2")
        elif (GPIO.input(buttons[1]) == 0 and GPIO.input(buttons[0])):
            move(1,1)
            print("moved 3")
        elif (GPIO.input(buttons[0]) and GPIO.input(buttons[3]) == 0):
            move(1, -1)
            print("moved 4")
        elif (GPIO.input(buttons[3]) == 0): #now generate moves, remember board grows down and to right
            move(0,-1)
            print("moved 5")
            
        elif (GPIO.input(buttons[1]) == 0):
            move(0,1)
            print("moved 6")
        elif (GPIO.input(buttons[2])):
            move(-1,0)
            print("moved 7")
        elif (GPIO.input(buttons[0])):
            move(1,0)
            print("moved 8")
        
        else:
            time.sleep(0.5)
        time.sleep(0.5)
        #update user's move and redraw
        updateMove()
        drawBoard()
    except KeyboardInterrupt:
        print("Cleaning up")
        GPIO.cleanup()
        sys.close(0)
GPIO.cleanup()