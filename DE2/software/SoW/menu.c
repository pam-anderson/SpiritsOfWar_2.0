#include "SoW.h"

typedef enum {
    SINGLE,
    MULTI,
    INSTR,
    AV,
    ENTER
} menu_option;

static int menu_pos[4] = {100, 120, 140, 160};
menu_option menu = SINGLE;

/*
 * @brief Draws the SINGLE menu to the screen.
 */
void draw_menu() {
	// Initialize
	  char_buffer = alt_up_char_buffer_open_dev("/dev/char_drawer");
	  alt_up_char_buffer_init(char_buffer);
	  alt_up_char_buffer_clear(char_buffer);
	  pixel_buffer = alt_up_pixel_buffer_dma_open_dev("/dev/pixel_buffer_dma");

	  alt_up_char_buffer_string(char_buffer, "Spirits of War", 30, 10);
	  alt_up_char_buffer_string(char_buffer, "Single Player", 29, 25);
	  alt_up_char_buffer_string(char_buffer, "Multiplayer", 30, 30);
	  alt_up_char_buffer_string(char_buffer, "Instructions", 30, 35);
	  alt_up_char_buffer_string(char_buffer, "Capture Audio/Video", 27, 40);
	  alt_up_char_buffer_string(char_buffer, "W - Up    A - Left", 0, 55);
	  alt_up_char_buffer_string(char_buffer, "S - Down  D - Right", 0, 56);

	  alt_up_pixel_buffer_dma_change_back_buffer_address(pixel_buffer, PIXEL_BUFFER_BASE);
	  alt_up_pixel_buffer_dma_swap_buffers(pixel_buffer);

	  while (alt_up_pixel_buffer_dma_check_swap_buffers_status(pixel_buffer));
	  alt_up_pixel_buffer_dma_clear_screen(pixel_buffer, 0);
}

/*
 * @brief Move selection arrow between menu options. Uses positions based off menu_pos array.
 *
 * @param curr_position -- Old position of selection arrow - index of menu_pos array
 * @param new_position -- New position of selection arrow - index of menu_pos array
 */
void move_arrow(int curr_position, int new_position) {
	alt_up_pixel_buffer_dma_draw_box(pixel_buffer, 110, menu_pos[curr_position], 114,
			menu_pos[curr_position] + 4, 0x0000, 0);
	alt_up_pixel_buffer_dma_draw_box(pixel_buffer, 110, menu_pos[new_position], 114,
			menu_pos[new_position] + 4, 0x3456, 0);
}

/*
 * @brief Draw the main menu, then wait on key presses to move selection arrow and change screens.
 */
void show_menu() {
	printf("show menu\n");
	  int key;
	  draw_menu();
	  move_arrow(menu, menu);
	  while(1) {
		  get_input(0, &key);
		  printf("key %d\n", key);
		  if(key == ENTER) {
			  alt_up_char_buffer_clear(char_buffer);
			  alt_up_pixel_buffer_dma_clear_screen(pixel_buffer, 0);
			  return;
		  } else {
			  move_arrow(menu, key);
			  menu = key;
		  }
	  }
}
