from Player import initializePlayers, initializeCharacterPositions, Turn
from Map import Map
from GameDrawer import drawCursor, drawSprite, animate, drawHealthbar
from Player import CHARS_PER_PLAYER
from enum import Enum

class Input(Enum):
    Up, Down, Left, Right, Esc, Next, Enter = range(7)

class Game:
    def __init__(self):
        # Draw map and initialize players here
        self.players = initializePlayers()
        self.gameMap = Map()
        initializeCharacterPositions(0, self.players[0].characters,
            self.gameMap.tiles)
        initializeCharacterPositions(1, self.players[1].characters,
            self.gameMap.tiles)

    def getPlayerInput(self):
        keypress = raw_input("")
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
            keypress = self.getPlayerInput()
            if keypress == Input.Up:
                drawCursor(oldX, oldY, oldX, oldY - 1)
                oldY -= 1
            elif keypress == Input.Down:
                drawCursor(oldX, oldY, oldX, oldY + 1)
                oldY += 1
            elif keypress == Input.Left:
                drawCursor(oldX, oldY, oldX - 1, oldY)
                oldX -= 1
            elif keypress == Input.Right:
                drawCursor(oldX, oldY, oldX + 1, oldY)
                oldX += 1
            elif keypress == Input.Enter and \
                    self.gameMap.tiles[oldX][oldY] in validMoves:
                return self.gameMap.tiles[oldX][oldY]
            elif keypress == Input.Esc:
                return False                

    def moveCharacter(self, character):
        print "moveChar"
        oldTile = character.position
        validMoves = self.gameMap.depthFirstSearch(character,
            character.characterClass.movement, False)
        for move in validMoves:
            print move.x, move.y
            drawSprite(move.x, move.y, 0) #highlight potential moves

        newTile = self.selectSpace(character, validMoves)
        if newTile is not False:
            character.position = newTile
            character.move = Turn.Attack
            oldTile.occupiedBy = 0
            newTile.occupiedBy = character
            animate(self.gameMap, 0, oldTile.x, oldTile.y, newTile.x, newTile.y)

        for move in validMoves:
            drawSprite(move.x, move.y, 0) # unhighlight moves

    def attackCharacter(self, team, character):
        print "attackChar"
        oldTile = character.position
        validMoves = self.gameMap.depthFirstSearch(character,
            character.characterClass.movement, True)
        for move in validMoves:
            print move.x, move.y
            drawSprite(move.x, move.y, 0) # highlight attacks

        newTile = self.selectSpace(character, validMoves)
        if newTile is not False:
            character.move = Turn.Done
            if newTile.occupiedBy is not character and \
                    newTile.occupiedBy is not 0:
                print "Successful hit"
                newTile.occupiedBy.currentHp -= character.characterClass.attack
                drawHealthbar(character)
                if newTile.occupiedBy.currentHp <= 0:
                    newTile.occupiedBy.currentHp = 0
                    drawSprite(newTile.x, newTile.y, Tile.Grass)
                    self.players[team].charactersRemaining -= 1

        for move in validMoves:
            drawSprite(move.x, move.y, 0) # unhighlight attacks
 
    def doPlayerTurn(self, team):
        print "doPlayerTurn"
        charId = 0
        drawCursor(0, 0, self.players[team].characters[charId].position.x,
            self.players[team].characters[charId].position.y)
        while True:
            keypress = self.getPlayerInput()
            if keypress == Input.Esc:
                # Draw exit screen
                return False
            elif keypress == Input.Next:
                move = self.players[team].currentMove()
                for character in self.players[team].characters:
                    if character.move == move and move != Turn.Done:
                        character.move += 1
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
                drawCursor(
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
                drawCursor(
                    self.players[team].characters[oldId].position.x,
                    self.players[team].characters[oldId].position.y,
                    self.players[team].characters[charId].position.x,
                    self.players[team].characters[charId].position.y)
 
    def playGame(self):
        print "playGame"
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

