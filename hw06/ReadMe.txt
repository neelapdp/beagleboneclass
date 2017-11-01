Daniel Neelappa Display SPI interface homework

I moved the files over this directory from Dr. Yoder's main repo.

I modified the code to expand the drawing width and select multiple colors.
During use, I wanted it to seem like waves in the ocean. Instead of drawing
a wide box for the cursor, it will create a triangle like shape. This is made
using a single for loop, while a box would most likely take two for loops to
draw. There is a delay inside for the color fliping and the wave behavior. 
The delay is updated each time the drawing occurs. After an interval, the color
flips between white to blue or visa-versa. Also, the width grows until it reaches that interval and then goes back to a width of 1 pixel.
This way, it looks some-what like a wave crashing against the shore. I wanted
to make a fading look, however, I'm not sure how to fade the current color,
let's say blue, to another (black). I thought that would be interesting to have,
but I don't have the computer graphics knowledge to make that.

The display runs off of GP0 and SPi1 ports on the beaglebone blue.

To run the program use sudo ./etch-a-sketch
if the exec is not there, then use "make" to create it.

// Comments from Prof. Yoder
// It works!
// Grade:  10/10
