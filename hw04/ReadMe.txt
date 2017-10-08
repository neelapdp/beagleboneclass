
9/21 - 9/22:

I have been working with the web based interface for the bone. I got to try out some of the examples, but now I'm working to understand the code better.


9/26/17: Currently, I'm looking into the rotary encoders.

9/29/17: Rotary Encoders working and functioning with etch-sketch program.
Waiting to demo with Dr. Yoder. To run the program, type python3 etchsketch.py 
to run the program.

10/3/17: Rotary Encoder etch-sketch: This program runs correctly with the encoders
To run this command, it will require sudo ./etchsketch.py to run it.

	MMAP: The c program is ready to go with sensing the registers and then
outputing to a led on the board. In the program, there are two memory mapping locations
that are used. One corresponds to GP0 and the other one is GP1. The hardest part of 
this assignment is trying to figure out where the chip's ports match with the traditional
ports that we are used to on the beaglebone blue diagram. Right now in the code,
I have two buttons and two leds both sharing the same GPIO mem. location.
This can easily be changed by using the second mem. variables to access more ports.

I also added the memory diagram to the repo. It is called "memory location of Beaglebone Blue".


I think a good final project might be to create a mapper to systematically check all these ports and perform a mapping operation.

