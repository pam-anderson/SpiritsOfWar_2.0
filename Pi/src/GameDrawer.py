START_TILE_X = 0
START_TILE_Y = 0
MAP_SIZE = 8

#Draw functions
def drawMap():
    for y in range(0, MAP_SIZE):
        for x in range(0, MAP_SIZE):
            drawSprite(x + START_TILE_X, y + START_TILE_Y,
                gameMap.tiles[x][y].sprite)

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
    #draw on DE2 send max health and current health
    return

def drawCharacters():
    for p in players:
        for c in players.characters:
            drawSprite(c.position[0] + START_TILE_X, c.position[1]
                + START_TILE_Y, c.standingSprite)
        
    return
