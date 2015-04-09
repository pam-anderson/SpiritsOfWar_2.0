import RPi.GPIO as GPIO
from time import sleep
from Map import Direction
import numpy as np
import time
import cv2
import subprocess

START_PIXEL_X = 32
START_PIXEL_Y = 40
MAP_SIZE = 8
NUM_FRAMES = 50

class Message:
    Health, Screen, Cursor, AliveCharacters, PlayVideo, SendVideo, \
        RecordVideo, Sprite, Exit, Turn, Menu = range(11)

class Drawer:
    def __init__(self, gameMap, players):
        self.gameMap = gameMap
        self.players = players
        self.readyPin = 3
        self.donePin = 5
        self.messagePins = [7, 8, 10, 11]
        self.dataPins = [12, 13, 15, 16, 18, 19, 21, 22, 23, 24, 26, 29, 31, 32,
            33, 35, 36, 37, 38, 40]
        self.setGpios()

    def __del__(self):
        print "drawer cleanup"
        for pin in self.messagePins:
            GPIO.output(pin, 0)
            pass
        for pin in self.dataPins:
            pass
            GPIO.output(pin, 0)
        GPIO.cleanup()

    def setGpios(self):
        GPIO.setmode(GPIO.BOARD)
        for pin in self.messagePins:
            GPIO.setup(pin, GPIO.OUT)
            pass
        for pin in self.dataPins:
            GPIO.setup(pin, GPIO.OUT)
            pass
        GPIO.setup(self.readyPin, GPIO.OUT)
        GPIO.setup(self.donePin, GPIO.IN)

    def drawMap(self):
        for y in range(MAP_SIZE):
            for x in range(MAP_SIZE):
                self.drawSprite(x, y, self.gameMap.tiles[x][y].sprite)
        self.drawCharacters()
        return

    def setMessagePins(self, message):
        for pin in range(len(self.messagePins)):
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

    def navigateMenu(self, sel):
        self.boardIsReady()
        self.setMessagePins(Message.Menu)
        self.setDataPins(sel, 3)
        # Pi is now a reader until the DE2 passes the changeWriter message

    def exitMenu(self, sel):
        self.boardIsReady()
        self.setMessagePins(Message.Exit)
        self.setDataPins(sel, 1)

    def drawSprite(self, x, y, memory, tileCoords = 1):
        # If tileCoords == 0, x and y args are in pixel coords
        # 1st Set of Data = [x pixel]
        # 2nd Set of Data = [Memory | y pixel]
        #                     MSB       LSB
        self.boardIsReady()
        if tileCoords is 1:
            out = (x << 4) + START_PIXEL_X
        else:
            out = x
        self.setMessagePins(Message.Sprite)
        self.setDataPins(out, 9)
        self.boardIsReady()
        if tileCoords is 1:
            out = (memory << 8) | ((y << 4) + START_PIXEL_Y)
        else:
            out = (memory << 8) | y
        self.setMessagePins(Message.Sprite)
        self.setDataPins(out, 18)
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
        oldTile = self.gameMap.tiles[oldX][oldY]
        self.drawSprite(oldX, oldY, oldTile.sprite)
        if self.gameMap.tiles[oldX][oldY].occupiedBy != 0:
            self.drawSprite(oldX, oldY, oldTile.occupiedBy.standingSprite)
        # Data = [oldX | oldY | newX | newY]
        #         MSB                   LSB
        if newX < 0 or newY < 0:
            return
        self.boardIsReady()
        out = (newX << 3) | newY
        self.setMessagePins(Message.Cursor)
        self.setDataPins(out, 12)
        return
    
    def drawCharacters(self):
        for p in self.players:
            for c in p.characters:
                self.drawSprite(c.position.x, c.position.y, c.standingSprite)
        return
    
    def animateToTile(self,ram_location, dx, dy, oldx, oldy, newx, newy,
            sprite_type):
        newTile = self.gameMap.tiles[newx][newy]
        oldTile = self.gameMap.tiles[oldx][oldy]
        oldx = (oldx << 4) + START_PIXEL_X
        oldy = (oldy << 4) + START_PIXEL_Y
        newx = (newx << 4) + START_PIXEL_X
        newy = (newy << 4) + START_PIXEL_Y
        print oldx, oldy, newx, newy
        for i in range(16):
            self.drawSprite(oldx, oldy, oldTile.sprite, 0)
            self.drawSprite(newx, newy, newTile.sprite, 0)
            if i % 8 <= 3:
                self.drawSprite(oldx + i * dx, oldy + i * dy,
                    ram_location + sprite_type, 0)
            else:
                self.drawSprite(oldx + i * dx, oldy + i * dy,
                    ram_location + sprite_type + 1, 0)
            sleep(0.03)
        self.drawSprite(oldx, oldy, oldTile.sprite, 0)
        return
    
    def animate(self, ram_location, oldx, oldy, newx, newy):
        dist = 1
        #movement music
        path = [0] * (self.gameMap.tiles[newx][newy].distance + 1)
        self.gameMap.getPath(newx, newy, path)
        while dist <= self.gameMap.tiles[newx][newy].distance:
            if path[dist] == Direction.Left:
                self.animateToTile(ram_location, 1, 0, oldx, oldy,
                    oldx + 1, oldy, 2)
                oldx += 1
            elif path[dist] == Direction.Right:
                self.animateToTile(ram_location, -1, 0, oldx, oldy,
                    oldx - 1, oldy, 6)
                oldx -= 1
            elif path[dist] == Direction.Up:
                self.animateToTile(ram_location, 0, 1, oldx, oldy,
                    oldx, oldy + 1, 4)
                oldy += 1
            else: # Direction.Down
                self.animateToTile(ram_location, 0, -1, oldx, oldy,
                    oldx, oldy - 1, 0)
                oldy -= 1
            dist += 1
        return
    
    def movePlayer(self, character, oldx, oldy, newx, newy):
        if newx == -1 or newy == -1 or newx == MAP_SIZE or newy == MAP_SIZE:
            return
        self.animate(character.animationSprite, oldx, oldy, newx,
            newy)
        self.drawSprite(newx, newy, character.standingSprite)
	
    def loadTurn(self, playerTurn):
        self.boardIsReady()
        out = playerTurn
        self.setMessagePins(Message.Turn)
        self.setDataPins(out, 1)

    def sendVideo(self, name):
        cap = cv2.VideoCapture(name)
        i = 0
        self.boardIsReady();
        self.setMessagePins(5);
        self.setDataPins(0);
        subprocess.call(['sudo','./pins', name])

    def Video(self, team, character):
        if team == 0 and character.characterId == 0:
            self.sendVideo('p0c0')
        elif team == 0 and character.characterId == 1:
            self.sendVideo('p0c1')
        elif team == 0 and character.characterId == 2:
            self.sendVideo('p0c2')
        elif team == 1 and character.characterId == 0:
            self.sendVideo('p1c0')
        elif team == 1 and character.characterId == 1:
            self.sendVideo('p1c1')
        elif team == 1 and character.characterId == 2:
            self.sendVideo('p1c2')
