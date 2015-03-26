#include "SoW.h"
#include <stdio.h>

#define GPIO_ADDRESS 0x4440

void get_input(int *instruction, int *data) {
	int gpio = 0;
	while(IORD_32DIRECT(GPIO_ADDRESS, 0) == 0){
		// Wait for ready to be set
	}
	gpio = IORD_32DIRECT(GPIO_ADDRESS, 4);
	// Set done flag
	IOWR_32DIRECT(GPIO_ADDRESS, 0, 1);
	while(IORD_32DIRECT(GPIO_ADDRESS, 0) == 1){
		// Wait for ready to be cleared
	}
	// Clear done flag
	IOWR_32DIRECT(GPIO_ADDRESS, 0, 0);
	*instruction = gpio & 0x1F;
	*data = gpio & 0xFFFE0 >> 5;
}

void menu_init() {
	// Initialize character and pixel buffers
	char_buffer = alt_up_char_buffer_open_dev("/dev/char_drawer");
	alt_up_char_buffer_init(char_buffer);
	alt_up_char_buffer_clear(char_buffer);
	pixel_buffer = alt_up_pixel_buffer_dma_open_dev("/dev/pixel_buffer_dma");
}

int main(void) {
	int instruction;
	int data;
	int data2; // Used when we need to perform 2 reads in a row

	sdcard_init();
	sprite_init();
	hardware_init();
	menu_init();
	initialize_players();
	
	while(1) {
		get_input(&instruction, &data);
		switch(instruction) {
			case 0:
				// Update health bar of specific character
				update_healthbar((data & 0x400) >> 10, (data & 0x300) >> 8, (data & 0xF0) >> 4,
						data & 0xF);
				break;
			case 1:
				// Draw specified screen (instruction, game, start, etc)
				break;
			case 2:
				draw_cursor((data & 0x38 >> 3) << 4, (data & 0x7) << 4);
				break;
			case 3:
				//highlight_characters(data);
				break;
			case 4:
				//play_video(data);
				break;
			case 6:
				//record_video(data);
				break;
			case 7:
				get_input(&instruction, &data2);
				draw_sprite(data & 0x1FF, data2 & 0xFF, (data2 & 0x3F00) >> 8);
				break;
			case 8:
				//exit_menu(data);
				break;
			case 9:
				load_turn(data & 0x1);
				break;
			case 10:
				// DE2 is now WRITER. Send data from mic.
				break;
			default:
				break;
		}
	}
}
