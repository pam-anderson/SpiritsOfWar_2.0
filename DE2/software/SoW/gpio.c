#include "SoW.h"

void get_input(int *instruction, int *data) {
	int gpio = 0;
	while(IORD_32DIRECT(GPIO_ADDRESS, 0) == 0){
		// Wait for READY to be set
		//printf("wait for rdy set\n");
	}
	gpio = IORD_32DIRECT(GPIO_ADDRESS, 4);
	// Set DONE flag
	IOWR_32DIRECT(GPIO_ADDRESS, 0, 1);
	while(IORD_32DIRECT(GPIO_ADDRESS, 0) == 1){
		// Wait for READY to be cleared
		//printf("wait for rdy clr\n");
	}
	// Clear DONE flag
	IOWR_32DIRECT(GPIO_ADDRESS, 0, 0);
	*instruction = gpio & 0xF;
	*data = (gpio & 0xFFFFFF0) >> 4;
}

int transmit_data(int data) {
	// Set data bits
	IOWR_32DIRECT(GPIO_ADDRESS, 2, data);
	// Set READY flag
	IOWR_32DIRECT(GPIO_ADDRESS, 0, 1);
	while(IORD_32DIRECT(GPIO_ADDRESS, 0) == 0) {
		// Wait for DONE flag to be set
	}
	// Clear READY flag
	IOWR_32DIRECT(GPIO_ADDRESS, 0, 0);
	// Check if we are changing readers/writers
	if(data == 0xFFFF) {
		// Switch DE2 to reader
		IOWR_32DIRECT(GPIO_ADDRESS, 1, 1);
		return 0;
	}
	return 1;
}
