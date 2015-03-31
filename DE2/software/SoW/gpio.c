#include "SoW.h"

void get_input(int *instruction, int *data) {
	int gpio = 0;
	while(IORD_32DIRECT(GPIO_ADDRESS, 0) == 0){
		// Wait for READY to be set
	}
	gpio = IORD_32DIRECT(GPIO_ADDRESS, 4);
	// Set DONE flag
	IOWR_32DIRECT(GPIO_ADDRESS, 0, 1);
	while(IORD_32DIRECT(GPIO_ADDRESS, 0) == 1){
		// Wait for READY to be cleared
	}
	// Clear DONE flag
	IOWR_32DIRECT(GPIO_ADDRESS, 0, 0);
	*instruction = gpio & 0xF;
	*data = (gpio & 0xFFFFFF0) >> 4;
}
