START_PIXEL_X = 0
START_PIXEL_Y = 0
MAP_SIZE = 8

#Draw functions
def drawMap():
    for y in range(0, MAP_SIZE):
        for x in range(0, MAP_SIZE):
            drawSprite(x << 4 + START_PIXEL_X, y << 4 + START_PIXEL_Y,
                gameMap.tiles[x][y].sprite)

    drawCharacters()
    return

def drawSprite(x, y, memory):
    #
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

def drawCursor(oldX, oldY, newX, newY):
    #clear old cursor position, draw new position
    return

def drawCharacters():
    for p in players:
        for c in players.characters:
            drawSprite(c.position[0] << 4 + START_PIXEL_X, c.position[1] << 4
                + START_PIXEL_Y, c.standingSprite) 
    return

def animateToTile(ram_location, dx, dy, oldx, oldy, newx, newy, sprite_type):
    for i in range(0, 16):
        drawSprite(oldx << 4 + START_PIXEL_X, oldy << 4 + START_PIXEL_Y,
            gameMap.tiles[oldx][oldy].sprite)
        drawSprite(newx << 4 + START_PIXEL_X, newy << 4 + START_PIXEL_Y,
            gameMap.tiles[newx][newy].sprite)
        if i % 8 <= 3:
            drawSprite(oldx << 4 + i * dx + START_PIXEL_X, oldy << 4 + i * dy +
                START_PIXEL_Y, ram_location + sprite_type)
        else:
            drawSprite(oldx << 4 + i * dx + START_PIXEL_X, oldy << 4 + i * dy + 
                START_PIXEL_Y, ram_location + sprite_type + 1)
        #wait some time
    drawSprite(oldx << 4 + START_PIXEL_X, oldy << 4 + START_PIXEL_Y,
        gameMap.tiles[oldx][oldy].sprite)
    return

def animate(gameMap, ram_location, oldx, oldy, newx, newy):
    dist = 1
    #movement music
    path = [0] * (gameMap.tiles[newx][newy].distance + 1)
    getPath(newx, newy, path)
    while dist <= map[newx][newy].distance:
        if path[dist] == 0:
            animateToTile(ram_location, 1, 0, oldx, oldy, oldx + 1, oldy, 0)
            oldx += 1
        elif path[dist] == 1:
            animateToTile(ram_location, -1, 0, oldx, oldy, oldx - 1, oldy, 2)
            oldx -= 1
        elif path[dist] == 2:
            animateToTile(ram_location, 0, 1, oldx, oldy, oldx, oldy + 1, 4)
            oldy += 1
        else:
            animateToTile(ram_location, 0, -1, oldx, oldy, oldx, oldy - 1, 6)
            oldy -= 1
        dist += 1
    return

def getPath(newx, newy, path):
    distance = gameMap.tiles[newx][newy].distance
    while gameMap.tiles[newx][newy].distance != 0:
        if newx > 0 and gameMap.tiles[newx][newy].distance > \
            gameMap.tiles[newx - 1][newy].distance:
            newx -= 1
            path[distance] = 0
        elif newx < MAP_SIZE - 1 and gameMap.tiles[newx][newy].distance > \
            gameMap.tiles[newx + 1][newy].distance:
            newx += 1
            path[distance] = 1
        elif newy > 0 and gameMap.tiles[newx][newy].distance > \
            gameMap.tiles[newx][newy - 1].distance:
            newy -= 1
            path[distance] = 2
        elif newy < MAP_SIZE - 1 and gameMap.tiles[newx][newy].distance > \
            gameMap.tiles[newx][newy + 1].distance:
            newy += 1
            path[distance] = 3
        distance -= 1
    return

def movePlayer(player_id, character_id, oldx, oldy, newx, newy):
    gameMap.tiles[oldx][oldy].occupiedBy = 0
    if newx == -1 or newy == -1 or newx == MAP_SIZE or newy == MAP_SIZE:
        return
    animate(players[player_id].characters[character_id].animationSprite, oldx, oldy, newx, newy)
    players[player_id].characters[character_id].position[0] = newx
    players[player_id].characters[character_id].position[1] = newy
    gameMap.tiles[newx][newy].occupiedBy = players[player_id].characters[character_id]
    drawSprite(newx << 4 + START_PIXEL_X, newy << 4 + START_PIXEL_Y,
        players[player_id].characters[character_id].standingSprite)
