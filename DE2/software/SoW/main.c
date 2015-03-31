#include "SoW.h"
#include "SoW_game_screen.h"

int frames[24][VIDEO_X_PIXELS * VIDEO_Y_PIXELS];

void menu_init() {
	// Initialize character and pixel buffers
	char_buffer = alt_up_char_buffer_open_dev("/dev/char_drawer");
	alt_up_char_buffer_init(char_buffer);
	alt_up_char_buffer_clear(char_buffer);
	pixel_buffer = alt_up_pixel_buffer_dma_open_dev("/dev/pixel_buffer_dma");
	
	alt_up_pixel_buffer_dma_change_back_buffer_address(pixel_buffer, PIXEL_BUFFER_BASE);
	alt_up_pixel_buffer_dma_swap_buffers(pixel_buffer);

	while (alt_up_pixel_buffer_dma_check_swap_buffers_status(pixel_buffer));
	alt_up_pixel_buffer_dma_clear_screen(pixel_buffer, 0);
}

void test_sprites() {
	int i = 0, x = 0, y = 0;
	for(i = 1; i <= 40; i++) {
		if(i % 10 == 0) {
			y += 16;
			x = 0;
		}
		draw_sprite(x + 32, y + 40, i - 1);
		x += 16;
	}
}

void test_video_init() {
    int frame = 0;
    int pixel = 0;
    for(frame = 0; frame < 24; frame++) {
        for(pixel = 0; pixel < VIDEO_X_PIXELS * VIDEO_Y_PIXELS; pixel++) {
            if(frame % 2 == 0) {
            	frames[frame][pixel] = 0xFF00FF;
            }
            else {
            	frames[frame][pixel] = 0xFFFFFF;
            }
        }
    }
}

void test_draw_frame(int frame) {
    int pixel = 0;
    for(pixel = 0; pixel < VIDEO_X_PIXELS * VIDEO_Y_PIXELS; pixel++) {
        alt_up_pixel_buffer_dma_draw_box(pixel_buffer, pixel % VIDEO_X_PIXELS,
        	pixel / VIDEO_X_PIXELS, pixel % VIDEO_X_PIXELS,
			pixel / VIDEO_X_PIXELS, frames[frame][pixel], 0);
    }
}

void test_draw_video() {
    int frame = 0;
    for(frame = 0; frame < 24; frame++) {
        test_draw_frame(frame);
    }
}

void play_game() {
	int instruction;
	int data;
	int data2; // Used when we need to perform 2 reads in a row
	int i = 5;
	while(1) {
		get_input(&instruction, &data);
		printf("inst: %d, data:%d\n", instruction, data);
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
				draw_cursor((data & 0x38) << 1, (data & 0x7) << 4);
				break;
			case 3:
				//highlight_characters(data);
				break;
			case 4:
				display_video((data & 0x4) >> 2, (data & 0x3));
				break;
			case 6:
				record_video((data & 0x4) >> 2, (data & 0x3));
				break;
			case 7:
				get_input(&instruction, &data2);
                printf("x:%d, y:%d\n", (data&0x1FF), (data2&0xFF));
				draw_sprite(data & 0x1FF, data2 & 0xFF, (data2 & 0x3FF00) >> 8);
				break;
			case 8:
				if (!draw_exit_screen()) {
					return;
				}
				break;
			case 9:
				load_turn(data & 0x1);
				break;
			default:
				break;
		}
	}
}

int main(void) {
	sdcard_init();
	sprite_init();
	hardware_init();
	menu_init();

	while(1) {
		show_menu();
		initialize_players();
		load_turn(0);
		play_game();
	}
    //test_video_init();
    //test_draw_video();

	return 0;
}
