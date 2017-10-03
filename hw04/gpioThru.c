// From : http://stackoverflow.com/questions/13124271/driving-beaglebone-gpio-through-dev-mem
//
// Read one gpio pin and write it out to another using mmap.
// Be sure to set -O3 when compiling.
// Modified by Mark A. Yoder  26-Sept-2013
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

    gpio_addr = mmap(0, GPIO1_SIZE, PROT_READ | PROT_WRITE, MAP_SHARED, fd, 
                        GPIO1_START_ADDR);

    gpio_oe_addr           = gpio_addr + GPIO_OE;
    gpio_datain            = gpio_addr + GPIO_DATAIN;
    gpio_setdataout_addr   = gpio_addr + GPIO_SETDATAOUT;
    gpio_cleardataout_addr = gpio_addr + GPIO_CLEARDATAOUT;

    
    
    gpio_addr_two = mmap(0, GPIO0_SIZE, PROT_READ | PROT_WRITE, MAP_SHARED, fd, 
                        GPIO0_START_ADDR);

    gpio_oe_addr_two           = gpio_addr_two + GPIO_OE;
    gpio_datain_two            = gpio_addr_two + GPIO_DATAIN;
    gpio_setdataout_addr_two   = gpio_addr_two + GPIO_SETDATAOUT;
    gpio_cleardataout_addr_two = gpio_addr_two + GPIO_CLEARDATAOUT;

    if(gpio_addr == MAP_FAILED || gpio_addr_two == MAP_FAILED) {
        printf("Unable to map GPIO\n");
        exit(1);
    }
    printf("GPIO mapped to %p\n", gpio_addr);
    printf("GPIO OE mapped to %p\n", gpio_oe_addr);
    printf("GPIO SETDATAOUTADDR mapped to %p\n", gpio_setdataout_addr);
    printf("GPIO CLEARDATAOUT mapped to %p\n", gpio_cleardataout_addr);

    printf("GPIO 2nd mapped to %p\n", gpio_addr_two);
    printf("GPIO OE 2nd mapped to %p\n", gpio_oe_addr_two);
    printf("GPIO SETDATAOUTADDR 2nd mapped to %p\n", gpio_setdataout_addr_two);
    printf("GPIO CLEARDATAOUT 2nd mapped to %p\n", gpio_cleardataout_addr_two);
    

//29
//21
//22
//23
//24
    while(keepgoing) {

   	if(!((*gpio_datain) & (1<<25))) {
           *gpio_setdataout_addr = 1 << 24; 
   	} else {
           *gpio_cleardataout_addr = 1 << 24;
   	}
   	printf("x%x\n", (*gpio_datain));
        usleep(100000);
        
        if(!((*gpio_datain) & (1<<17))) {
           *gpio_setdataout_addr = 1 << 23; 
   	} else {
           *gpio_cleardataout_addr = 1 << 23;
   	}
        
    }

    munmap((void *)gpio_addr, GPIO1_SIZE);
    close(fd);
    return 0;
}
