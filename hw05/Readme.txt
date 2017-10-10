ReadMe:
Daniel Neelappa
Hw05:

10/3/17:
I played around with the realtime examples. I haven't coded in javascript before. The thing that
confuses me the most is how people make the interfaces look so nice. They use CSS, but I 
don't see how that maps to the actual page.
I looked at the code and noticed that only the web-interface has to be changed to make the matrix
respond to red led outputs. The sad part, I saw that the hw instructions had that same feedback.
haha. At least I learned it on my own.
10/10/17:
Demo with Dr. Yoder. The led matrix now cycles through orange, green, red, and blank outputs.
To run this system, I have the file placed in Dr. Yoder's /exercies/realtime/.
This way, the boneserver.js already knows the correct files to pull for a request. I don't 
have to modify the actual boneserver.js then to point to different files to give to the user.
So to run this program, I cd into that folder and run "./bonServer.js".

I have copied the main files, the matrixled.js and the css files into my repo for use.

Questions


Before writing any code, write a paragraph describing how boneServer.js and the browser interact in the given example. For example, in matrixLED.js connect() is called to make a connection between the browser and the bone.  The message “matrix” is sent to the bone. What happens in response to the message? 

The boneServer.js essentially opens a web server that listens on the bone on port 9090. This
can be reconfigured however. Then as the clinet (web browswer) connects, the server will issue
the connect method. That method will essentially default with giving the root directory of the
web server. However, after the user selects a new page like "matrix", this will get parsed on 
the receiving end (boneserver.js) and pull the correct html, javascript, and css files and 
push it to the user's browswer. Then the user can enjoy that request.

What happens when an “LED” is clicked on in the browser

When an LED is clicked, it is essentially calling a callback that is toggling a bit stored
in a virtual board of the matrix. The virtual board stored on the webpage is then updating
the visual board on the screen with the correct color. Lastly, there is the emit calls that
talk to the actual beaglebone server to have the bonserver perform the i2c communication.

What entry in matrix.css is used to color the LED?

There is an entry called "on". This will be toggled to output a green square on the screen.

Write a high level paragraph about how you will control the two LEDs. What messages will be sent between the browser and the bone?

The two leds in the matrix spot will be called using the same calls that are in place now. I will keep track of the 
red and green led conditions on the board in seperate matrices. Then I will peform a logic decoding that when a button
is pressed, it will parse the state and update accordingly. It will then access the actual beaglebone using the emit calls.

Write your code.  Do you need to change boneServer.js? (I don’t think so.)  Customize the html to have your name on it, etc.

Code All good!