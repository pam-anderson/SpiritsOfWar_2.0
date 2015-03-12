START_PIXEL_X = 0
START_PIXEL_Y = 0

#Draw functions
def drawMap():
    #send command to
    for y in range(0, MAP_SIZE):
        for x in range(0, MAP_SIZE):
            drawSprite(x << 4 + START_PIXEL_X, y << 4 + START_PIXEL_Y, gameMap.tiles[x][y].sprite)

    drawCharacters()
    return

def drawSprite(x, y, memory):
    #write to pin on DE2
	#IOWR_32DIRECT(DRAWER_BASE, 0, x);
	#IOWR_32DIRECT(DRAWER_BASE, 4, y);
	#IOWR_32DIRECT(DRAWER_BASE, 8, memory);
	#IOWR_32DIRECT(DRAWER_BASE, 12, 1); //Start
	#while(IORD_32DIRECT(DRAWER_BASE, 24) == 0) {}
    return

def drawHealthbar(player_id, character_id):
    #draw on DE2
    return

def drawCharacters():
    return
