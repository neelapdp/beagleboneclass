

1) installing the latest shipped image on the BeagleBone
I finished task 1, and the image is on my BeagleBone.

2)setting up a host computer with Linux for kernel development
Yes, I have my host computer ready to go for kernel development

3) gathering all the needed SD cards, cables, etc.
Yes, I bought multiple SD cards and got the box from the ECE shop. It did not
come with cables for the breadboard, and Garry said that Dr. Yoder has them. I'll
wait until later to receive them.

4)installing git on a your host
Yes git is installed on my host

5)signing up for the two beagle Google groups (See Working With Open Source)
 Yes I signed up for the wiki and joined both google groups.

 6) writing a simple Etch-a-sketch program
 Yes, my program is done and ready to go.
 To run it make sure you have Python 3, then type:
 
python3 etchsketch.py

The install.sh will install it on your linux distribution if you are using ubuntu. 
If not the command might need to be altered.

The program will first ask you to type in a grid count. You have to enter a 
number,and it must be greater than 0. NOTE: if you make it double digits like 10
or greater, it might seem a little off. This is normal, and the result of double digits taking two columns to display its header. This will make the x's not line up with those columns. I would use 9 and below for clear viewing.

Afterwards, the help screen will display as well as the grid with the first x.
The help screen will let you know how to use the game. wasd (lowercase) keys will move your
position. So for example you might press ds to move down and right. to confirm your action, you must press enter for it to take effect. clear will remove all marks except the one you are positioned at. Also typing exit as a command and pressing enter will close the program.