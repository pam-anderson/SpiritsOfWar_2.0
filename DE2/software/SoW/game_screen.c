#include "SoW.h"
#include "Sow_game_screen.h"

 int cursor_x = 0;
 int cursor_y = 0;
 int cursor_ram = 0;

 static int healthbar_pos[2][3][2] = {{{29, 15}, {123, 15}, {217, 15}},
 		{{29, 214}, {123, 214}, {217, 214}}};
/*
 * @brief Draw a specific sprite to the screen using the pixel_drawer accelerator.
 * @param x The absolute position of the pixel in the x axis of the top left corner of the sprite
 * @param y The absolute position of the pixel in the y axis of the top left corner of the sprite
 * @param type The sprite to draw
 */
void draw_sprite(int x, int y, int type) {
	IOWR_32DIRECT(DRAWER_BASE, 0, x);
	IOWR_32DIRECT(DRAWER_BASE, 4, y);
	IOWR_32DIRECT(DRAWER_BASE, 8, type);
	IOWR_32DIRECT(DRAWER_BASE, 12, 1); //Start
	while(IORD_32DIRECT(DRAWER_BASE, 24) == 0) {}
}


/*
 * @brief Draw the initial health bar at a given position, as well as the character associated with
 *        that health bar
 * @param x The absolute position of the pixel in the x axis of the top left corner of the character
 * 		  to be drawn beside the health bar.
 * @param y The absolute position of the pixel in the y axis of the top left corner of the character
 * 		  to be drawn beside the health bar.
 */
void draw_healthbar(int player_id, int character_id, int x, int y) {
	// Draw character
	draw_sprite(x - 8, y - 4, player_id * 3 + character_id + 3);
	//alt_up_pixel_buffer_dma_draw_box(pixel_buffer, x, y, x + SIZE_OF_TILE/2, y + SIZE_OF_TILE/2, colour, 0);
	// Draw healthbar
	alt_up_pixel_buffer_dma_draw_box(pixel_buffer, x + SIZE_OF_TILE/2 + 8, y, x + SIZE_OF_TILE/2 + 8 + HEALTHBAR_LEN,
			y + SIZE_OF_TILE/2, 0xF822, 0);
	alt_up_pixel_buffer_dma_draw_rectangle(pixel_buffer, x + SIZE_OF_TILE/2 + 7, y, x + SIZE_OF_TILE/2 + 9 + HEALTHBAR_LEN,
				y + SIZE_OF_TILE/2, 0xFFFF, 0);
}


/*
 * @brief Move the selection cursor to a new position
 * @param old_x The current x coordinate of the cursor
 * @param old_y The current y coordinate of the cursor
 * @param new_x The new x coordinate of the cursor
 * @param new_y The new y coordinate of the cursor
 */
void draw_cursor(int new_x, int new_y) {
	alt_up_pixel_buffer_dma_draw_rectangle(pixel_buffer, new_x + MAP_CORNER_X, new_y + MAP_CORNER_X,
			new_x + SIZE_OF_TILE - 1 + MAP_CORNER_X, new_y + SIZE_OF_TILE - 1 + MAP_CORNER_X, 0xF81F, 0);
}

/*
 * @brief Draws exit prompt to screen
 * @param player_id Player id
 * @return 0 if player chose to exit, 1 if player did not choose to exit
 */
int draw_exit_screen(int player_id) {
	// Use player id for input
	keypress key;
	alt_up_char_buffer_clear(char_buffer);
	alt_up_char_buffer_string(char_buffer, "Are you sure you want to quit?", 25, 23);
	alt_up_char_buffer_string(char_buffer, "[A] - Yes     [D] - No", 30, 25);
	while(1) {
		//key = get_player_input(player_id);
		if (key == LEFT) {
			alt_up_char_buffer_clear(char_buffer);
			return 0;
		} else if (key == RIGHT) {
			alt_up_char_buffer_clear(char_buffer);
			return 1;
		}
	}
}

/*
 * @brief Draw the initial health bar at a given position, as well as the character associated with
 *        that health bar
 * @param x The absolute position of the pixel in the x axis of the top left corner of the character
 * 		  to be drawn beside the health bar.
 * @param y The absolute position of the pixel in the y axis of the top left corner of the character
 * 		  to be drawn beside the health bar.
 */
void healthbar_init(int player_id, int character_id, int x, int y) {
	// Draw character
	draw_sprite(x - 8, y - 4, player_id * 3 + character_id + 3);
	//alt_up_pixel_buffer_dma_draw_box(pixel_buffer, x, y, x + SIZE_OF_TILE/2, y + SIZE_OF_TILE/2, colour, 0);
	// Draw healthbar
	alt_up_pixel_buffer_dma_draw_box(pixel_buffer, x + SIZE_OF_TILE/2 + 8, y, x + SIZE_OF_TILE/2 + 8 + HEALTHBAR_LEN,
			y + SIZE_OF_TILE/2, 0xF822, 0);
	alt_up_pixel_buffer_dma_draw_rectangle(pixel_buffer, x + SIZE_OF_TILE/2 + 7, y, x + SIZE_OF_TILE/2 + 9 + HEALTHBAR_LEN,
				y + SIZE_OF_TILE/2, 0xFFFF, 0);
}

void initialize_players() {
	int i;
	int j;
	int x;
	int y;

	for(i = 0; i < 2; i++) {
		for(j = 0; j < 3; j++) {
			//draw_sprite(0, 0, i * 3 + 3 + j); draw characters at x and y
			healthbar_init(i, j, healthbar_pos[i][j][0], healthbar_pos[i][j][1]);
		}
	}
}



void update_healthbar(int player_id, int character_id, int hp, int max_hp) {
	// Black out health lost
	int pixel_per_hp = HEALTHBAR_LEN / max_hp;
	int pixel_health = hp * pixel_per_hp;

	alt_up_pixel_buffer_dma_draw_box(pixel_buffer,
			healthbar_pos[player_id][character_id][0] + SIZE_OF_TILE/2 + 8,
			healthbar_pos[player_id][character_id][1] + 1,

			healthbar_pos[player_id][character_id][0] + SIZE_OF_TILE/2 + 8 + HEALTHBAR_LEN,
			healthbar_pos[player_id][character_id][1] + SIZE_OF_TILE/2 - 1, 0x0, 0);
	if(pixel_health <= 0) {
		return;
	}
	alt_up_pixel_buffer_dma_draw_box(pixel_buffer,
			healthbar_pos[player_id][character_id][0] + SIZE_OF_TILE/2 + 8,
			healthbar_pos[player_id][character_id][1] + 1,
			healthbar_pos[player_id][character_id][0] + SIZE_OF_TILE/2 + 8 + pixel_health,
			healthbar_pos[player_id][character_id][1] + SIZE_OF_TILE/2 - 1, 0xF822, 0);
}
