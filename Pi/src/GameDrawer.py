import RPi.GPIO as GPIO

START_PIXEL_X = 0
START_PIXEL_Y = 0
MAP_SIZE = 8

# Write message type to: [7, 11, 12] (BOARD)
# Ready flag at [13] 
# Pins available for data (13): [15, 16, 18, 22, 29, 31, 32, 33, 35,
# 36, 37, 38, 40]

class Drawer:
    def __init__(self, gameMap, players):
        self.gameMap = gameMap
        self.players = players
        self.dataPins = [15, 16, 18, 22, 29, 31, 32, 33, 35, 36, 37, 38, 40]
        GPIO.setmode(GPIO.BOARD)

    def drawMap(self):
        for y in range(MAP_SIZE):
            for x in range(MAP_SIZE):
                self.drawSprite(x << 4 + START_PIXEL_X, y << 4 + START_PIXEL_Y,
                    self.gameMap.tiles[x][y].sprite)
        self.drawCharacters()
        return

    def setDataPins(self, data, length):
        for pin in range(length):
            mask = 1 << pin
            out = 1 if mask & data > 0 else 0
            GPIO.output(self.dataPins[pin], out)

    def boardIsReady(self):
        while GPIO.input(13):
            pass
        return
            
    
    def drawSprite(self, x, y, memory):
        self.boardIsReady()
    	#IOWR_32DIRECT(DRAWER_BASE, 0, x);
    	#IOWR_32DIRECT(DRAWER_BASE, 4, y);
    	#IOWR_32DIRECT(DRAWER_BASE, 8, memory);
    	#IOWR_32DIRECT(DRAWER_BASE, 12, 1); //Start
    	#while(IORD_32DIRECT(DRAWER_BASE, 24) == 0) {}
        return
    
    def drawHealthbar(self, character):
        self.boardIsReady()
        GPIO.output(7, GPIO.LOW)
        GPIO.output(11, GPIO.LOW)
        GPIO.output(12, GPIO.LOW)
        # PUT HEALTHBAR INFO IN GPIO HERE
        out = character.currentHp << 4 | character.characterClass.maxHp
        self.setDataPins(out, 8)
        return
    
    def drawCursor(self,oldX, oldY, newX, newY):
        #clear old cursor position, draw new position     
        self.boardIsReady()
        return
    
    def drawCharacters(self):
        for p in self.players:
            for c in self.players.characters:
                self.drawSprite(c.position[0] << 4 + START_PIXEL_X,
                    c.position[1] << 4 + START_PIXEL_Y, c.standingSprite)
        return
    
    def animateToTile(self,ram_location, dx, dy, oldx, oldy, newx, newy,
            sprite_type):
        for i in range(16):
            self.drawSprite(oldx << 4 + START_PIXEL_X, oldy << 4 + START_PIXEL_Y,
                self.gameMap.tiles[oldx][oldy].sprite)
            self.drawSprite(newx << 4 + START_PIXEL_X, newy << 4 + START_PIXEL_Y,
                self.gameMap.tiles[newx][newy].sprite)
            if i % 8 <= 3:
                self.drawSprite(oldx << 4 + i * dx + START_PIXEL_X,
                    oldy << 4 + i * dy +
                    START_PIXEL_Y, ram_location + sprite_type)
            else:
                self.drawSprite(oldx << 4 + i * dx + START_PIXEL_X,
                    oldy << 4 + i * dy + 
                    START_PIXEL_Y, ram_location + sprite_type + 1)
            #wait some time
        self.drawSprite(oldx << 4 + START_PIXEL_X, oldy << 4 + START_PIXEL_Y,
            self.gameMap.tiles[oldx][oldy].sprite)
        return
    
    def animate(self, ram_location, oldx, oldy, newx, newy):
        dist = 1
        #movement music
        path = [0] * (self.gameMap.tiles[newx][newy].distance + 1)
        self.getPath(newx, newy, path)
        while dist <= self.gameMap.tiles[newx][newy].distance:
            if path[dist] == 0:
                self.animateToTile(ram_location, 1, 0, oldx, oldy,
                    oldx + 1, oldy, 0)
                oldx += 1
            elif path[dist] == 1:
                self.animateToTile(ram_location, -1, 0, oldx, oldy,
                    oldx - 1, oldy, 2)
                oldx -= 1
            elif path[dist] == 2:
                self.animateToTile(ram_location, 0, 1, oldx, oldy,
                    oldx, oldy + 1, 4)
                oldy += 1
            else:
                self.animateToTile(ram_location, 0, -1, oldx, oldy,
                    oldx, oldy - 1, 6)
                oldy -= 1
            dist += 1
        return
    
    def getPath(self, newx, newy, path):
        distance = self.gameMap.tiles[newx][newy].distance
        while self.gameMap.tiles[newx][newy].distance != 0:
            if newx > 0 and self.gameMap.tiles[newx][newy].distance > \
                    self.gameMap.tiles[newx - 1][newy].distance:
                newx -= 1
                path[distance] = 0
            elif newx < MAP_SIZE - 1 and self.gameMap.tiles[newx][newy].distance > \
                    self.gameMap.tiles[newx + 1][newy].distance:
                newx += 1
                path[distance] = 1
            elif newy > 0 and self.gameMap.tiles[newx][newy].distance > \
                    self.gameMap.tiles[newx][newy - 1].distance:
                newy -= 1
                path[distance] = 2
            elif newy < MAP_SIZE - 1 and self.gameMap.tiles[newx][newy].distance > \
                    self.gameMap.tiles[newx][newy + 1].distance:
                newy += 1
                path[distance] = 3
            distance -= 1
        return
    
    def movePlayer(self, character, oldx, oldy, newx, newy):
        self.gameMap.tiles[oldx][oldy].occupiedBy = 0
        if newx == -1 or newy == -1 or newx == MAP_SIZE or newy == MAP_SIZE:
            return
        self.animate(character.animationSprite, oldx, oldy, newx,
            newy)
        character.position = self.gameMap.tiles[newx][newy]
        self.gameMap.tiles[newx][newy].occupiedBy = character
        self.drawSprite(newx << 4 + START_PIXEL_X, newy << 4 + START_PIXEL_Y,
            character.standingSprite)
