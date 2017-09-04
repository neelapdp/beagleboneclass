
#!/usr/bin/env python3


#written by Daniel Neelappa 9/3/17
import sys


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
    user = input("Type a command:")
    if (user == "clear"):
        clearBoard()
    elif (user == "exit"):
        sys.exit(0)
    elif (user == "a"): #now generate moves, remember board grows down and to right
        move(0,-1)
    elif (user == "d"):
        move(0,1)
    elif (user == "w"):
        move(-1,0)
    elif (user == "s"):
        move(1,0)
    elif (user == "aw" or user == "wa"):
        move(-1,-1)
    elif (user == "wd" or user == "dw"):
        move(-1,1)
    elif (user == "sd" or user == "ds"):
        move(1,1)
    elif (user == "as" or user == "sa"):
        move(1, -1)
    else:
        print("Not a valid Command")
    #update user's move and redraw
    updateMove()
    drawBoard()
    