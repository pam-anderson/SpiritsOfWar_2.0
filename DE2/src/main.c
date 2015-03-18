#include "SoW.h"
#include <stdio.h>


void get_input(int *instruction, int *data) {
	int i = 0;
	char c = 0;
	while(IORD_32DIRECT(0x4440, 0) == 0);
	*instruction = IORD_32DIRECT(0x4440, 4);
	*data = IORD_32DIRECT(0x4440, 4);
	IOWR_32DIRECT(0x4440, 0, 1);
	while(IORD_32DIRECT(0x4440, 0) == 1);
	IOWR_32DIRECT(0x4440, 0, 0);
}


int main(void) {
	sdcard_init();
	sprite_init();
	hardware_init();
	int instruction;
	int data;
	menu_init();
	initialize_players();
	
	while(1) {
		get_input(&instruction, &data);
		switch(instuction) {
			case 0:
				update_health(data, data, data, data);
				break;
			case 1:
				//update_screen(data);
				break;
			case 2:
				draw_cursor(data, data);
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
				draw_sprite(data, data, data);
				break;
			case 8:
				//exit_menu(data);
				break;
			case 9:
				load_turn(data);
				break;
			case default:
				break;
		}
	}
}
