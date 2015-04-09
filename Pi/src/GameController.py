from Player import initializePlayers, initializeCharacterPositions, Turn
from Map import Map, Sprite
from GameDrawer import Drawer, START_PIXEL_X, START_PIXEL_Y
from Player import CHARS_PER_PLAYER
from enum import Enum
from Sounds import Sounds
from getch import getch
import sys
from ComputerPlayer import ComputerPlayer
from Gui import guiVideoRec
from Gui import guiSoundRec
from itertools import cycle

class Input(Enum):
    Up, Down, Left, Right, Esc, Next, Enter = range(7)

class Sound(Enum):
    War, Mage, Arch, Move, Die = range(5) 

keys = {'a' : Input.Left,  'A' : Input.Left,
        'd' : Input.Right, 'D' : Input.Right,
        's' : Input.Down,  'S' : Input.Down,
        'w' : Input.Up,    'W' : Input.Up,
        'n' : Input.Next,  'N' : Input.Next,
        'x' : Input.Esc,   'X' : Input.Esc,
        ' ' : Input.Enter }

fncs = {'select' : 0,
        'move'   : 1,
        'attack' : 2}

soundSel = { 'Move' : 3, 'Die' : 4 }


class Game:
    def __init__(self):
        # Draw map and initialize players here
        self.players = initializePlayers()
        self.gameMap = Map()
        self.draw = Drawer(self.gameMap, self.players)
        self.cpu = [0,0]
        self.sound = Sounds()
        self.vidGui = guiVideoRec()
        self.sndGui = guiSoundRec()
        initializeCharacterPositions(0, self.players[0].characters,
            self.gameMap.tiles)
        initializeCharacterPositions(1, self.players[1].characters,
            self.gameMap.tiles)

    def getPlayerInput(self, team, function, cursorx = 0, cursory = 0):
        if self.players[team].mode is 0:
            #keypress = sys.stdin.read(1)
            keypress = getch()
        else:
            # Look at fncs dictionary
            if function is fncs['select']:
                keypress = self.cpu[team].doTurn(cursorx, cursory)
            elif function is fncs['move']:
                keypress = self.cpu[team].doMove()
            elif function is fncs['attack']:
                keypress = self.cpu[team].doAttack()
        try:
        #    print keypress
            return keys[keypress]
        except KeyError as exception:
            return

    def selectSpace(self, character, validMoves, function):
        oldX = character.position.x
        oldY = character.position.y 
        while(True):
            keypress = self.getPlayerInput(character.team, function)
            if keypress == Input.Up:
                self.draw.drawCursor(oldX, oldY, oldX, oldY - 1)
                oldY -= 1
            elif keypress == Input.Down:
                self.draw.drawCursor(oldX, oldY, oldX, oldY + 1)
                oldY += 1
            elif keypress == Input.Left:
                self.draw.drawCursor(oldX, oldY, oldX - 1, oldY)
                oldX -= 1
            elif keypress == Input.Right:
                self.draw.drawCursor(oldX, oldY, oldX + 1, oldY)
                oldX += 1
            elif keypress == Input.Enter and \
                    self.gameMap.tiles[oldX][oldY] in validMoves:
                return self.gameMap.tiles[oldX][oldY]
            elif keypress == Input.Esc:
                return False                

    def highlightTiles(self, tiles, highlight):
        for move in tiles:
            # Highlight potential moves
            if not highlight:
                move.sprite = move.sprite & 0xFF
            else:
                move.sprite = move.sprite | (highlight << 8)
            self.draw.drawSprite(move.x, move.y, move.sprite)
            if move.occupiedBy:
                self.draw.drawSprite(move.x, move.y,
                    move.occupiedBy.standingSprite)

    def moveCharacter(self, character):
        print "moveChar"
        oldTile = character.position
        validMoves = self.gameMap.depthFirstSearch(character.position.x,
            character.position.y, character.team,
            character.characterClass.movement, False)
        self.highlightTiles(validMoves, 1)
        newTile = self.selectSpace(character, validMoves, fncs['move'])
        if newTile is not oldTile:
            self.sound.play_sfx(soundSel['Move'])
        if newTile is not False:
            self.draw.movePlayer(character, oldTile.x, oldTile.y, newTile.x, newTile.y)
            character.position = newTile
            character.move = Turn.Attack
            oldTile.occupiedBy = 0
            newTile.occupiedBy = character
        self.highlightTiles(validMoves, 0)
        for move in validMoves:
            move.distance = 1000

    def attackCharacter(self, team, character):
        print "attackChar"
        oldTile = character.position
        validMoves = self.gameMap.depthFirstSearch(character.position.x,
            character.position.y, character.team,
            character.characterClass.attackRange, True)
        self.highlightTiles(validMoves, 2)
        newTile = self.selectSpace(character, validMoves, fncs['attack'])
        if newTile is not False:
            character.move = Turn.Done
            if newTile.occupiedBy is not character and \
                    newTile.occupiedBy is not 0:
                self.sound.play_sfx(character.characterId)
                newTile.occupiedBy.currentHp = max(0,
                    newTile.occupiedBy.currentHp - \
                    character.characterClass.attack)
                self.draw.Video(team, character)
                self.draw.drawHealthbar(newTile.occupiedBy)
                if newTile.occupiedBy.currentHp <= 0:
                    self.sound.play_sfx(soundSel['Die'])
                    newTile.occupiedBy.currentHp = 0
                    self.players[not team].characters.remove(newTile.occupiedBy)
                    newTile.occupiedBy = 0
                    self.draw.drawSprite(newTile.x, newTile.y,
                        Sprite.Grass.value)
        self.highlightTiles(validMoves, 0)
        for move in validMoves:
            move.distance = 1000
 
    def doPlayerTurn(self, team):
        print "doPlayerTurn"
        characters = cycle(self.players[team].characters)
        character = characters.next()
        self.draw.drawCursor(0, 0, character.position.x, character.position.y)
        while True:
            keypress = self.getPlayerInput(team, fncs['select'],
                character.position.x, character.position.y)
            if keypress == Input.Esc:
                # Draw exit screen
                if self.exitMenu():
                    return False
            elif keypress == Input.Next:
                move = self.players[team].currentMove()
                for char in self.players[team].characters:
                    if char.move == move and move != Turn.Done:
                        char.move += 1
                    self.draw.drawCursor( char.position.x,
                        char.position.y, -1, -1)
                return True
            elif keypress == Input.Enter:
                if character.move == Turn.Move:
                    self.moveCharacter(character)
                    return True
                elif character.move == Turn.Attack:
                    self.attackCharacter(team, character)
                    return True
            elif keypress == Input.Left or keypress == Input.Right:
                oldChar = character
                character = characters.next()
                self.draw.drawCursor(oldChar.position.x, oldChar.position.y,
                    character.position.x, character.position.y)
 
    def drawMenu(self):
        # Draw Main Menu
        print "drawMenu"
        opts = {'1P' : 0, '2P' : 1, 'Demo' : 2, 'AV' : 3}
        cursor = 0
        while True:
            keypress = self.getPlayerInput(0, 0)
            if keypress == Input.Left or keypress == Input.Up:
                if cursor > 0:
                    cursor -= 1
                    print cursor
                self.draw.navigateMenu(cursor)
            elif keypress == Input.Right or keypress == Input.Down:
                if cursor+1 < len(opts):
                    cursor += 1
                    print cursor
                self.draw.navigateMenu(cursor)
            elif keypress == Input.Enter:
                self.draw.navigateMenu(4)
                if cursor is 0:
                    self.cpu[1] = ComputerPlayer(self.gameMap, self.players[1],
                        self.players[0])
                    self.players[1].mode = 1
                if cursor is 2:
                    self.players[0].mode = 1
                    self.players[1].mode = 1
                    self.cpu[0] = ComputerPlayer(self.gameMap, self.players[0],
                        self.players[1])
                    self.cpu[1] = ComputerPlayer(self.gameMap, self.players[1],
                        self.players[0])
                if cursor is 3:
                    self.vidGui.createButton()
                    self.sndGui.createButton()                    
                return

    def exitMenu(self):
        print "exitMenu"
        self.draw.exitMenu(0)
        while True:
            keypress = self.getPlayerInput(0, 0)
            if keypress == Input.Left:
                # Exit
                self.draw.exitMenu(0)
                return True
            elif keypress == Input.Right:
                # Don't exit
                self.draw.exitMenu(1)
                return False

    def playGame(self):
        print "playGame"
        self.drawMenu();
        self.draw.drawMap()
        self.draw.drawCharacters()
        currPlayer = 0
        while True:
            while not self.players[currPlayer].isTurnDone():
                if len(self.players[currPlayer].characters) is 0:
                    print "Game over"
                    return
                if not self.doPlayerTurn(currPlayer):
                    print "Exited game"
                    return
            self.players[currPlayer].resetTurn()
            currPlayer = not currPlayer
            self.draw.loadTurn(currPlayer)



