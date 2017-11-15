Daniel Neelappa
10-31-17


This hw assignment is designed to test the speed of reading gpio ports using various methods.

mmap in the c language proved to be the fastest.
This is the "gpioThru" c file.

The program will read the signal on gpio1_5 and map to the 75% led of the battery

the kernel driver was the 2nd fastest
This is located in kernel/gpio

The program will need to be loaded into the kernel with insmod <.ko file>

The python gpio command was the slowest. It was mapping the input of GPO1_4
to GP0_3. However, the system did perform better in timing speeds when mmap
was running in the background. It might have increased the refresh rate of the device to improve the python version.

I attached a word document that has a table with timings as well as scope captures of each condition.

my project page
https://elinux.org/ECE497_Project-Queue

// Comments from Prof. Yoder
// Min and Max results are missing
// % CPU is missing
// Pictures look good
// Grade:  7/10