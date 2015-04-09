#define NUM_PLAYERS        2
#define CHARS_PER_PLAYER   3
#define NUM_SPRITE_TYPES   3
#define SPRITES_PER_CHAR   9
#define ANIMATION_HARDWARE 9
#define HEALTHBAR_LEN      50
#define SIZE_OF_TILE       16
#define SIZE_OF_MAP		   8

#define MAP_CORNER_X 	32
#define MAP_CORNER_Y 	40
#define NUM_VIDEO_FRAMES 60
#define VIDEO_X_PIXELS 128
#define VIDEO_Y_PIXELS 128
#define NUM_VIDEO_PIXEL 16384
#define VIDEO_CORNER_X 0
#define VIDEO_CORNER_Y 0

//0. Grass					0
//1. Water					1
//2. Rock					2
//3. P0C0S0					3
//4. P0C1S0					4
//5. P0C2S0					5
//6. P1C0S0					6
//7. P1C1S0					7
//8. P1C2S0					8
//9 - 16. P0C0S1-8			9-16
//17 - 24. P0C1S1-8			17-24
//25 - 32. P0C2S1-8			25-32
//33 - 40. P1C0S1-8
//41 - 48. P1C1S1-8
//49 - 56. P1C2S1-8



int **sprites;
int video[VIDEO_X_PIXELS * VIDEO_Y_PIXELS];
//alt_u16 videos[1][NUM_VIDEO_FRAMES][VIDEO_X_PIXELS * VIDEO_Y_PIXELS];

//char blinker = 0xFFFF;
