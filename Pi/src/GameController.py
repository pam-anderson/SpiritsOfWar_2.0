from Player import initializePlayers, initializeCharacterPositions, Turn
from Map import Map, Sprite
from GameDrawer import Drawer, START_PIXEL_X, START_PIXEL_Y
from Player import CHARS_PER_PLAYER
from enum import Enum
from Sounds import Sound
from getch import getch
from Gui import guiVideoRec
from Gui import guiSoundRec

class Input(Enum):
    Up, Down, Left, Right, Esc, Next, Enter = range(7)
class Sound(Enum):
    War, Mage, Arch, Move, Die = range(5)
    

class Game:
    def __init__(self):
        # Draw map and initialize players here
        self.players = initializePlayers()
        self.gameMap = Map()
        self.draw = Drawer(self.gameMap, self.players)
        self.cpu = 0
        #self.sound = Sound()
        self.vidGui = guiVideoRec()
        self.sndGui = guiSoundRec()
        initializeCharacterPositions(0, self.players[0].characters,
            self.gameMap.tiles)
        initializeCharacterPositions(1, self.players[1].characters,
            self.gameMap.tiles)

    def getPlayerInput(self, team):
        if self.players[team].mode is 0:
            keypress = getch()
            if keypress == 'a' or keypress == 'A':
                return Input.Left
            elif keypress == 'd' or keypress == 'D':
                return Input.Right
            elif keypress == 's' or keypress == 'S':
                return Input.Down
            elif keypress == 'w' or keypress == 'W':
                return Input.Up
            elif keypress == 'n' or keypress == 'N':
                return Input.Next
            elif keypress == ' ':
                return Input.Enter
            elif keypress == 'x' or keypress == 'X':
                return Input.Esc

    def selectSpace(self, character, validMoves):
        oldX = character.position.x
        oldY = character.position.y 
        while(True):
            keypress = self.getPlayerInput(character.team)
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
#        self.sound.play_sfx(Sound.Move)
        oldTile = character.position
        validMoves = self.gameMap.depthFirstSearch(character.position.x,
            character.position.y, character.team,
            character.characterClass.movement, False)
        self.highlightTiles(validMoves, 1)
        newTile = self.selectSpace(character, validMoves)
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
#       self.sound.play_sfx(character.characterId)
        oldTile = character.position
        validMoves = self.gameMap.depthFirstSearch(character.position.x,
            character.position.y, character.team,
            character.characterClass.movement, True)
        self.highlightTiles(validMoves, 2)
        newTile = self.selectSpace(character, validMoves)
        if newTile is not False:
            character.move = Turn.Done
            if newTile.occupiedBy is not character and \
                    newTile.occupiedBy is not 0:
                newTile.occupiedBy.currentHp = max(0,
                    newTile.occupiedBy.currentHp - \
                    character.characterClass.attack)
                self.draw.drawHealthbar(newTile.occupiedBy)
                if newTile.occupiedBy.currentHp <= 0:
#                    self.sound.play_sfx(Sound.Die)
                    newTile.occupiedBy.currentHp = 0
                    newTile.occupiedBy = 0
                    self.draw.drawSprite(newTile.x, newTile.y,
                        Sprite.Grass.value)
                    self.players[team].charactersRemaining -= 1
        self.highlightTiles(validMoves, 0)
        for move in validMoves:
            move.distance = 1000
 
    def doPlayerTurn(self, team):
        print "doPlayerTurn"
        charId = 0
        self.draw.drawCursor(0, 0,
            self.players[team].characters[charId].position.x,
            self.players[team].characters[charId].position.y)
        while True:
            keypress = self.getPlayerInput(team)
            if keypress == Input.Esc:
                # Draw exit screen
                if self.exitMenu():
                    return False
            elif keypress == Input.Next:
                move = self.players[team].currentMove()
                for character in self.players[team].characters:
                    if character.move == move and move != Turn.Done:
                        character.move += 1
                    self.draw.drawCursor( character.position.x,
                        character.position.y, -1, -1)
                return True
            elif keypress == Input.Enter:
                if self.players[team].characters[charId].move == Turn.Move:
                    self.moveCharacter(self.players[team].characters[charId])
                    return True
                elif self.players[team].characters[charId].move == Turn.Attack:
                    self.attackCharacter(team,
                        self.players[team].characters[charId])
                    return True
            elif keypress == Input.Left:
                oldId = charId
                while True:
                    if charId > 0:
                        charId -= 1
                    else:
                        charId = CHARS_PER_PLAYER - 1
                    if self.players[team].characters[charId].currentHp > 0:
                        break
                self.draw.drawCursor(
                    self.players[team].characters[oldId].position.x,
                    self.players[team].characters[oldId].position.y,
                    self.players[team].characters[charId].position.x,
                    self.players[team].characters[charId].position.y)
            elif keypress == Input.Right:
                oldId = charId
                while True:
                    if charId < CHARS_PER_PLAYER - 1:
                        charId += 1
                    else:
                        charId = 0
                    if self.players[team].characters[charId].currentHp > 0:
                        break
                self.draw.drawCursor(
                    self.players[team].characters[oldId].position.x,
                    self.players[team].characters[oldId].position.y,
                    self.players[team].characters[charId].position.x,
                    self.players[team].characters[charId].position.y)
 
    def drawMenu(self):
        # Draw Main Menu
        print "drawMenu"
        opts = {'1P' : 0, '2P' : 1, 'Inst' : 2, 'AV' : 3}
        cursor = 0
        while True:
            keypress = self.getPlayerInput(0)
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
                    self.players[1].mode = 1
                if cursor is 3:
                    self.vidGui.createButton()
                    self.sndGui.createButton()                    
                return

    def exitMenu(self):
        print "exitMenu"
        self.draw.exitMenu(0)
        while True:
            keypress = self.getPlayerInput(0)
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
                if self.players[currPlayer].charactersRemaining == 0:
                    print "Game over"
                    return
                if not self.doPlayerTurn(currPlayer):
                    print "Exited game"
                    return
            self.players[currPlayer].resetTurn()
            currPlayer = not currPlayer
            self.draw.loadTurn(currPlayer)



