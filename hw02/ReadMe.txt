Dr. Yoder,

My program works with having four buttons that move up, down, left, right, and the diagnols
I just don't like the implementation. I had trouble with the pull up/down
buttons, and I think the MOD and PAU buttons might be pull up too.

In this code, I just continue to poll it. I don't think that I want to use 
callbacks on this one either. I like the phone idea that you had. I had bluetooth working on my old beaglebone black.
I want to try to look into that next. I will post more to my repo when I
get something working that is better.


9/18/17 - latest
Hi Dr. Yoder,
	etchsketchy.py is updated to be used with buttons. I documented my code and pushed it to the repo. I didn't get a chance to interact with a wireless phone, but I want to build towards that Internet of Things approach later in the course. Currently, the code in etchsketch.py and ledtest.py both use external GPIO pins for the buttons and leds. Also, both programs need "python3 <fileName>" to run them. The "./" still throws errors when used.

