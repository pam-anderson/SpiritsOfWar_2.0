from Player import initializePlayers
from Map import Map

class Game:
    def __init__(self):
        self.currPlayer = 0
        # Draw map and initialize players here
        self.players = initializePlayers()
        self.gameMap = Map()
 
    def doPlayerTurn(self, team):
        # cycle thru chars, exit menu, skip turn, or select char
        # GET PLAYER INPUT
        keypress = 0
        charId = 0
        while True:
            if keypress == Input.Esc:
                # Draw exit screen
                return False
            elif keypress == Input.Next:
                # moveable->atk or atk->done
                move = players[team].currentMove()
                for character in players[team].characters:
                    if character.move == move and move != Turn.Done:
                        character.move += 1
                return True
            elif keypress == Input.Enter and \
                    gameMap.tiles[x][y].occupiedBy != 0:
                # do mvmnt or atk
                pass
            elif keypress == Input.Left:
                while True:
                    if charId > 0:
                        charId -= 1
                    else:
                        charId = CHARS_PER_PLAYER - 1
                    if players[team].characters[charId].currentHp > 0:
                        break
            elif keypress == Input.Right:
                while True:
                    if charId < CHAR_PER_PLAYER - 1:
                        charId += 1
                    else:
                        charId = 0
                    if players[team].characters[charId].currentHp > 0:
                        break
                #cycle right thru characters
                pass
            
    def playGame():
        while True:
            while not players[currPlayer].isTurnDone:
                if players[currPlayer].charactersRemaining == 0:
                    print "Game over"
                    return
                doPlayerTurn(currPlayer)
            players[currPlayer].resetTurn()
            currPlayer = not currPlayer

