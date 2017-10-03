// From : http://stackoverflow.com/questions/13124271/driving-beaglebone-gpio-through-dev-mem
//
// Read one gpio pin and write it out to another using mmap.
// Be sure to set -O3 when compiling.
// Modified by Mark A. Yoder  26-Sept-2013
// Modified by Daniel P. Neelappa 3-Oct-2017
#include <stdio.h>
#include <stdlib.h>
#include <sys/mman.h>
#include <sys/stat.h>
#include <fcntl.h> 
#include <signal.h>    // Defines signal-handling functions (i.e. trap Ctrl-C)
#include "beaglebone_gpio.h"

/****************************************************************
 * Global variables
 ****************************************************************/
int keepgoing = 1;    // Set to 0 when ctrl-c is pressed

/****************************************************************
 * signal_handler
 ****************************************************************/
void signal_handler(int sig);
// Callback called when SIGINT is sent to the process (Ctrl-C)
void signal_handler(int sig)
{
    printf( "\nCtrl-C pressed, cleaning up and exiting...\n" );
	keepgoing = 0;
}

int main(int argc, char *argv[]) {
    volatile void *gpio_addr;
    volatile unsigned int *gpio_oe_addr;
    volatile unsigned int *gpio_datain;
    volatile unsigned int *gpio_setdataout_addr;
    volatile unsigned int *gpio_cleardataout_addr;
    
    volatile void *gpio_addr_two;
    volatile unsigned int *gpio_oe_addr_two;
    volatile unsigned int *gpio_datain_two;
    volatile unsigned int *gpio_setdataout_addr_two;
    volatile unsigned int *gpio_cleardataout_addr_two;
    
    unsigned int reg;

    // Set the signal callback for Ctrl-C
    signal(SIGINT, signal_handler);

    int fd = open("/dev/mem", O_RDWR);

    printf("Mapping %X - %X (size: %X)\n", GPIO1_START_ADDR, GPIO1_END_ADDR, 
                                           GPIO1_SIZE);
    //this opens gp1's mem location
    gpio_addr = mmap(0, GPIO1_SIZE, PROT_READ | PROT_WRITE, MAP_SHARED, fd, 
                        GPIO1_START_ADDR);
    //gpio 1'st mem variables
    gpio_oe_addr           = gpio_addr + GPIO_OE;
    gpio_datain            = gpio_addr + GPIO_DATAIN;
    gpio_setdataout_addr   = gpio_addr + GPIO_SETDATAOUT;
    gpio_cleardataout_addr = gpio_addr + GPIO_CLEARDATAOUT;

    
    //this opens gp0's mem location
    gpio_addr_two = mmap(0, GPIO0_SIZE, PROT_READ | PROT_WRITE, MAP_SHARED, fd, 
                        GPIO0_START_ADDR);
    //gpio 2nd mem variables
    gpio_oe_addr_two           = gpio_addr_two + GPIO_OE;
    gpio_datain_two            = gpio_addr_two + GPIO_DATAIN;
    gpio_setdataout_addr_two   = gpio_addr_two + GPIO_SETDATAOUT;
    gpio_cleardataout_addr_two = gpio_addr_two + GPIO_CLEARDATAOUT;
    //if memory can't be opened
    if(gpio_addr == MAP_FAILED || gpio_addr_two == MAP_FAILED) {
        printf("Unable to map GPIO\n");
        exit(1);
    }
    //open 1st memory location printed to user
    printf("GPIO mapped to %p\n", gpio_addr);
    printf("GPIO OE mapped to %p\n", gpio_oe_addr);
    printf("GPIO SETDATAOUTADDR mapped to %p\n", gpio_setdataout_addr);
    printf("GPIO CLEARDATAOUT mapped to %p\n", gpio_cleardataout_addr);
    //open 2nd memory location printed to user
    printf("GPIO 2nd mapped to %p\n", gpio_addr_two);
    printf("GPIO OE 2nd mapped to %p\n", gpio_oe_addr_two);
    printf("GPIO SETDATAOUTADDR 2nd mapped to %p\n", gpio_setdataout_addr_two);
    printf("GPIO CLEARDATAOUT 2nd mapped to %p\n", gpio_cleardataout_addr_two);
    
//The pins below correspond to the GP1 port offset to board locations
//29 I believe this is the green led of the battery
//23 USr2 LED
//24 USr3 LED
    while(keepgoing) {
	//triggers a Usr3 led when a button is pressed
   	if(!((*gpio_datain) & (1<<25))) {
           *gpio_setdataout_addr = 1 << 24;  //on
   	} else {
           *gpio_cleardataout_addr = 1 << 24; //off
   	}
   	printf("x%x\n", (*gpio_datain)); //print data in to see how the whole value is changing
        usleep(100000);
        
	//triggers usr2 led when a butotn is pressed
        if(!((*gpio_datain) & (1<<17))) {
           *gpio_setdataout_addr = 1 << 23;  //on
   	} else {
           *gpio_cleardataout_addr = 1 << 23; //off
   	}
        
    }

    munmap((void *)gpio_addr, GPIO1_SIZE);
    close(fd);
    return 0;
}
