/*
To test that the Linux framebuffer is set up correctly, and that the device permissions
are correct, use the program below which opens the frame buffer and draws a gradient-
filled red square:

retrieved from:
Testing the Linux Framebuffer for Qtopia Core (qt4-x11-4.2.2)

http://cep.xor.aps.anl.gov/software/qt4-x11-4.2.2/qtopiacore-testingframebuffer.html

Modified by Daniel Neelappa 10/15/17

*/

#include <stdlib.h>
#include <unistd.h>
#include <stdio.h>
#include <fcntl.h>
#include <linux/fb.h>
#include <sys/mman.h>
#include <sys/ioctl.h>

#include "/opt/source/Robotics_Cape_Installer/libraries/rc_usefulincludes.h"
#include "/opt/source/Robotics_Cape_Installer/libraries/roboticscape.h"

int main()
{
    
   
    int fbfd = 0;
    struct fb_var_screeninfo vinfo;
    struct fb_fix_screeninfo finfo;
    long int screensize = 0;
    char *fbp = 0;
    int x = 0, y = 1;       // Make it so the it runs before the encoder is moved
    int xold = 0, yold = 0;
    long int location = 0;

    // Open the file for reading and writing
    fbfd = open("/dev/fb0", O_RDWR);
    if (fbfd == -1) {
        perror("Error: cannot open framebuffer device");
        exit(1);
    }
    printf("The framebuffer device was opened successfully.\n");

    // Get fixed screen information
    if (ioctl(fbfd, FBIOGET_FSCREENINFO, &finfo) == -1) {
        perror("Error reading fixed information");
        exit(2);
    }

    // Get variable screen information
    if (ioctl(fbfd, FBIOGET_VSCREENINFO, &vinfo) == -1) {
        perror("Error reading variable information");
        exit(3);
    }

    printf("%dx%d, %dbpp\n", vinfo.xres, vinfo.yres, vinfo.bits_per_pixel);
    printf("Offset: %dx%d, line_length: %d\n", vinfo.xoffset, vinfo.yoffset, finfo.line_length);
    
    if (vinfo.bits_per_pixel != 16) {
        printf("Can't handle %d bpp, can only do 16.\n", vinfo.bits_per_pixel);
        exit(5);
    }

    // Figure out the size of the screen in bytes
    screensize = vinfo.xres * vinfo.yres * vinfo.bits_per_pixel / 8;

    // Map the device to memory
    fbp = (char *)mmap(0, screensize, PROT_READ | PROT_WRITE, MAP_SHARED, fbfd, 0);
    if ((int)fbp == -1) {
        perror("Error: failed to map framebuffer device to memory");
        exit(4);
    }
    printf("The framebuffer device was mapped to memory successfully.\n");

    // initialize hardware first
	if(rc_initialize()){
		fprintf(stderr,"ERROR: failed to run rc_initialize(), are you root?\n");
		return -1;
	}

	printf("\nRaw encoder positions\n");
	printf("   E1   |");
	printf("   E2   |");
	printf("   E3   |");
	printf("   E4   |");
	printf(" \n");
	
	// Black out the screen
	short color = (0<<11) | (0 << 5) | 8;  // RGB
	for(int i=0; i<screensize; i+=2) {
	    fbp[i  ] = color;      // Lower 8 bits
	    fbp[i+1] = color>>8;   // Upper 8 bits
	}
        int colorFlip = 0;
        int delay = 0;
        int sizeDelay = 1;
        int r = 0;     // 5 bits
        int g = 0;      // 6 bits
        int b = 31; 
	while(rc_get_state() != EXITING) {
		printf("\r");
		for(int i=1; i<=4; i++){
			printf("%6d  |", rc_get_encoder_pos(i));
		}
		fflush(stdout);
        // Update framebuffer
        // Figure out where in memory to put the pixel
        x = (rc_get_encoder_pos(1)/2 + vinfo.xres) % vinfo.xres;
        y = (rc_get_encoder_pos(3)/2 + vinfo.yres) % vinfo.yres;
        // printf("xpos: %d, xres: %d\n", rc_get_encoder_pos(1), vinfo.xres);
        
        if((x != xold) || (y != yold)) {
            printf("Updating location to %d, %d\n", x, y);
            // This drawing module will create triangle 
            int i = 0; //loop counter for setting wave effect
            //loop goes through surrounding pixels to make the witdth larger, one loop makes a wave
            //effect
            for (i; i < sizeDelay; i++) {
            if (xold+vinfo.xoffset + i > vinfo.xres ||
                yold+vinfo.yoffset + i > vinfo.yres ||
                xold+vinfo.xoffset - i < vinfo.xoffset          ||
                yold+vinfo.yoffset - i < vinfo.yoffset)
            { 
                //skip since out of bounds
                
            }
            else {
            location = (xold+vinfo.xoffset + i) * (vinfo.bits_per_pixel/8) +
                       (yold+vinfo.yoffset - i) * finfo.line_length;
           
                       
           
           //delay determines when to flip the colors, 10 writes to the screen is default
            if (delay > 10){
            delay = 0;
            //flip between two colors
            if (colorFlip) {
            colorFlip = 0;//blue
            r = 0;     // 5 bits
            g = 0;      // 6 bits
            b = 31;      // 5 bits
            } else {
            colorFlip = 1;//white
            r = 31;     // 5 bits
            g = 31;      // 6 bits
            b = 31;      // 5 bits
            }
            }
            else {
                delay = delay + 1;
            }
            unsigned short int t = r<<11 | g << 5 | b;
            *((unsigned short int*)(fbp + location)) = t;
            
          
            
            }
            }
            
            //This determines the wave's height
            sizeDelay = sizeDelay + 1; //grow
            if (sizeDelay > 10){//reset wave to normal
                sizeDelay = 1;
            }
           
            // Set new location to white
            location = (x+vinfo.xoffset ) * (vinfo.bits_per_pixel/8) +
                       (y+vinfo.yoffset ) * finfo.line_length;
    
            *((unsigned short int*)(fbp + location)) = 0xff;
            
           xold = x;
            yold = y;
            
    
        }
		 
		rc_usleep(5000);
	}
	
	rc_cleanup();
    
    munmap(fbp, screensize);
    close(fbfd);
    return 0;
}
