/*
 * SoW_sdcard.c
 *
 *  Created on: 2015-01-27
 *      Author: Arjan
 */
#include "SoW.h"
#include "SoW_game_screen.h"

alt_up_sd_card_dev* sdcard;


void sdcard_init() {
	sdcard = alt_up_sd_card_open_dev("/dev/sdcard");
	alt_up_sd_card_is_Present();
	alt_up_sd_card_is_FAT16();
}

void load_sprite(char *filename, int* sprite) {
	short int fd = alt_up_sd_card_fopen(filename, FALSE);
	int i = 0;
	for(i = 0; i < 54; i++) {
		 alt_up_sd_card_read(fd);
	}

	for(i = 0; i < 256; i++) {
		sprite[i] = 0;
		sprite[i] = (alt_up_sd_card_read(fd) >> 3);
		sprite[i] |= (alt_up_sd_card_read(fd) >> 2) << 5;
		sprite[i] |= (alt_up_sd_card_read(fd) >> 3) << 11;
	}

	alt_up_sd_card_fclose(fd);
}

void sprite_init() {
	int i = 0, j = 0;
	sprites = (int **) calloc(57, sizeof(int *));
	sprites[0] = grass;
	 
	 sprites[1] = water;

	sprites[2] = rock;

	for(i = 3; i < 57; i++) {
		sprites[i] = (int *) calloc(256, sizeof(int));
		load_sprite(filenames[i], sprites[i]);
	}
}

 void hardware_init() {
	int i = 0, j = 0;
	for(i = 0; i <= 8; i++) {
		IOWR_32DIRECT(DRAWER_BASE, 8, i);
		for(j = 0; j < 16 * 16; j++) {
			IOWR_32DIRECT(DRAWER_BASE, 16, sprites[i][j]);
			while(IORD_32DIRECT(DRAWER_BASE, 24) == 0) {};
		}
	}
}

void load_sprite_hardware(int ram_location, int type) {
	int j = 0;
	IOWR_32DIRECT(DRAWER_BASE, 8, ram_location);
	for(j = 0; j < 16 * 16; j++) {
		IOWR_32DIRECT(DRAWER_BASE, 16, sprites[type][j]);
		while(IORD_32DIRECT(DRAWER_BASE, 24) == 0) {};
	}
}

void load_turn(int turn) {
	int j = 9;
	int i = turn * 24 + 9;
	for(j = 9; j <= 32; j++) {
		load_sprite_hardware(j, i);
		i++;
	}
}
