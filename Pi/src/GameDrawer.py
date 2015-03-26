import RPi.GPIO as GPIO

START_PIXEL_X = 32
START_PIXEL_Y = 40
MAP_SIZE = 8

class Message:
    Healh, Screen, Cursor, AliveCharacters, PlayVideo, CalibrateVideo, \
        RecordVideo, Sprite, Exit, Turn = range(10)

class Drawer:
    def __init__(self, gameMap, players):
        self.gameMap = gameMap
        self.players = players
        self.readyPin = 3
        self.donePin = 5
        self.messagePins = [7, 8, 10, 11]
        self.dataPins = [12, 13, 15, 16, 18, 22, 29, 31, 32, 33, 35,
            36, 37, 38, 40]
        GPIO.setmode(GPIO.BOARD)
        for pin in self.messagePins:
            GPIO.setup(pin, GPIO.OUT)
        for pin in self.dataPins:
            GPIO.setup(pin, GPIO.OUT)
        GPIO.setup(self.readyPin, GPIO.OUT)
        GPIO.setup(self.donePin, GPIO.IN)

    def __del__(self):
        print "drawer cleanup"
        GPIO.cleanup()

    def drawMap(self):
        for y in range(MAP_SIZE):
            for x in range(MAP_SIZE):
                self.drawSprite((x << 4) + START_PIXEL_X, (y << 4) + START_PIXEL_Y,
                    self.gameMap.tiles[x][y].sprite.value)
        self.drawCharacters()
        return

    def setMessagePins(self, message):
        for pin in range(3):
            mask = 1 << pin
            out = 1 if mask & message > 0 else 0
            GPIO.output(self.messagePins[pin], out)

    def setDataPins(self, data, length):
        for pin in range(length):
            mask = 1 << pin
            out = 1 if mask & data > 0 else 0
            GPIO.output(self.dataPins[pin], out)
        GPIO.output(self.readyPin, 1)
        while not GPIO.input(self.donePin):
            pass
        GPIO.output(self.readyPin, 0)

    def boardIsReady(self):
        while GPIO.input(self.donePin):
            pass
        return

    #9bits for x, 8 bits for y, 6 bits for memory
    def drawSprite(self, x, y, memory):
        print x
        self.boardIsReady()
        out = x
        self.setMessagePins(Message.Sprite)
        self.setDataPins(out, 9)
        self.boardIsReady()
        out = (memory << 8) | y
        self.setMessagePins(Message.Sprite)
        self.setDataPins(out, 14)
        return
    
    def drawHealthbar(self, character):
        # Data = [team ID | char ID | current HP | max HP]
        #           MSB                             LSB
        self.boardIsReady()
        out = (character.team << 10) | (character.characterId << 8) | \
                (character.currentHp << 4) | character.characterClass.maxHp
        self.setMessagePins(Message.Health)
        self.setDataPins(out, 11)
        return
    
    def drawCursor(self,oldX, oldY, newX, newY):
        # Data = [oldX | oldY | newX | newY]
        #         MSB                   LSB
        self.boardIsReady()
        out = ((oldX << 3 | oldY) << 3 | newX) << 3 | newY
        self.setMessagePins(Message.Cursor)
        self.setDataPins(out, 12)
        return
    
    def drawCharacters(self):
        for p in self.players:
            for c in p.characters:
                self.drawSprite((c.position.x << 4) + START_PIXEL_X,
                    (c.position.y << 4) + START_PIXEL_Y, c.standingSprite)
        return
    
    def animateToTile(self,ram_location, dx, dy, oldx, oldy, newx, newy,
            sprite_type):
        for i in range(16):
            self.drawSprite((oldx << 4) + START_PIXEL_X, (oldy << 4) + START_PIXEL_Y,
                self.gameMap.tiles[oldx][oldy].sprite.value)
            self.drawSprite((newx << 4) + START_PIXEL_X, (newy << 4) + START_PIXEL_Y,
                self.gameMap.tiles[newx][newy].sprite.value)
            if i % 8 <= 3:
                self.drawSprite((oldx << 4) + i * dx + START_PIXEL_X,
                    (oldy << 4) + i * dy +
                    START_PIXEL_Y, ram_location + sprite_type)
            else:
                self.drawSprite((oldx << 4) + i * dx + START_PIXEL_X,
                    (oldy << 4) + i * dy + 
                    START_PIXEL_Y, ram_location + sprite_type + 1)
            #wait some time
        self.drawSprite((oldx << 4) + START_PIXEL_X, (oldy << 4) + START_PIXEL_Y,
            self.gameMap.tiles[oldx][oldy].sprite.value)
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
        self.drawSprite((newx << 4) + START_PIXEL_X, (newy << 4) + START_PIXEL_Y,
            character.standingSprite)
	
    def loadTurn(self, playerTurn):
        self.boardIsReady()
        out = playerTurn
        self.setMessagePins(Message.Turn)
        self.setDataPin(out, 1)
