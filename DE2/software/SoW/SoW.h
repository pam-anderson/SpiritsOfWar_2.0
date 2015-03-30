#include "altera_up_avalon_audio_and_video_config.h"
#include "altera_up_avalon_audio.h"
#include "alt_types.h"
#include "altera_up_avalon_video_pixel_buffer_dma.h"
#include "altera_up_avalon_video_character_buffer_with_dma.h"
#include <stdio.h>
#include <stdlib.h>
#include "io.h"
#include "Altera_UP_SD_Card_Avalon_Interface.h"

/* Defines */
#define	FALSE 0
#define	TRUE 1

/* MEMORY LOCATIONS */
#define SERIAL_DATA_LOC (alt_u8 *) 0x0
#define SERIAL_PAR_LOC (alt_u8 *) 0x4
#define DRAWER_BASE (volatile int*) 0x4800
#define SERIAL_BASE (volatile int *) 0x4070
#define KEY_BASE 0x4078
#define TIMER_BASE 0x4000
#define GPIO_ADDRESS 0x4440

alt_up_char_buffer_dev *char_buffer;
alt_up_pixel_buffer_dma_dev* pixel_buffer;

/* SoW_sdcard.c */
void sdcard_init() ;
void load_sprite(char *, int *);

/* game_screen.c */
void update_healthbar(int, int, int, int);
void draw_sprite(int, int, int);
void draw_healthbar(int, int, int, int);
void draw_cursor(int, int);
int draw_exit_screen(int);
void healthbar_init(int, int, int, int);
void initialize_players(void);

/* gpio.c */
void get_input(int *, int *);
int transmit_data(int);
void switch_to_writer(void);

