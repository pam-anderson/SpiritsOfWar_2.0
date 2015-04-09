from Map import MAP_SIZE, Direction
from Player import Turn
from operator import itemgetter

sel = { Direction.Up    : 's',
        Direction.Down  : 'w',
        Direction.Left  : 'd',
        Direction.Right : 'a'}

class ComputerPlayer:
    def __init__(self, gameMap, cpu, opponent):
        self.gameMap = gameMap
        self.cpu = cpu
        self.opponent = opponent
        self.currentCharacter = 0
        self.movePath = []
        self.attackPath = []
        self.currentPriority = []

    # Determine which opponents are a priority
    def planTurn(self, character):
        classPrio = {'ranger' : 0, 'mage' : 1, 'warrior' : 2}
        opponents = [self.opponent.characters[0]]
        priority = []
        # Set distance values to determine closeness of opponents
        moves = self.gameMap.depthFirstSearch(character.position.x,
            character.position.y, character.team, MAP_SIZE * 2, 1)
        for opp in self.opponent.characters[1:]:
            for i in range(len(opponents)):
                if opp.position.distance > opponents[i].position.distance:
                    pass
                else:
                    break
            opponents.insert(i, opp)
        threshold = character.characterClass.movement + \
                    character.characterClass.attackRange
        for opp in opponents:
#            print opp.characterClass.className, opp.position.distance
            # Prioritize opponents by distance from character
            nearby = 3 if opp.position.distance > threshold else 0
            if opponents[opponents.index(opp) - 1].position.distance == \
                opp.position.distance:
                dist = opponents.index(opp) - 1
            else:
                dist = opponents.index(opp)
            prioVal = dist + \
                      classPrio[opp.characterClass.className] + nearby
            priority.append((opp, prioVal))
            priority.sort(key=itemgetter(1))
            self.currentPriority = priority
        print "prio", priority
        # Get movement path
        self.findPath(moves)
        #for move in moves:
        #    move.distance = 1000
        # Get attack path
        #moves = self.gameMap.depthFirstSearch(character.position.x,
        #    character.position.y, character.team, character.characterClass.attackRange, 1)
        moves = self.gameMap.depthFirstSearch(character.position.x,
            character.position.y, character.team, character.characterClass.attackRange, 1)
        self.findAttack(character.characterClass.attackRange)
        for move in moves:
            move.distance = 1000

    # Determine who to attack
    # Finds the highest priority target within attack range and attacks.
    # Returns enemy index if within attack range, otherwise returns false
    def findAttack(self, charRange):
        character = None
        for opp in self.currentPriority:
            print "The distance to target priority #", opp, "is", \
                    opp[0].position.distance
            if opp[0].position.distance <= charRange:
                character = opp[0]
                break
        if character is not None:
            x = character.position.x
            y = character.position.y
            path = [0] * (character.position.distance + 1)
            self.gameMap.getPath(character.position.x, character.position.y, path)
            rng = character.characterClass.attackRange
            self.attackPath = path[1:rng]
            print "atk", self.attackPath
        else:   
            self.attackPath = []

    # Determine where to move
    # charIndex select which char to move towards
    def findPath(self, moves):
        character = self.currentPriority[0][0]
        x = character.position.x
        y = character.position.y
        if self.currentCharacter.characterClass.attackRange >= character.position.distance:
            movePath = []
            return
        for move in moves:
            move.distance = 1000
        moves = self.gameMap.depthFirstSearch(self.currentCharacter.position.x,
            self.currentCharacter.position.y, self.currentCharacter.team, 2 * MAP_SIZE, 0)
        start = self.gameMap.findStartingPoint(character)
        while start is False:
            for char in self.currentPriority:
                start = self.gameMap.findStartingPoint(char[0])
                if start is not False:
                    break
        print "start", start.x, start.y
        path = [0] * (start.distance + 1)
        self.gameMap.getPath(start.x, start.y, path)
        rng = character.characterClass.movement
        self.movePath = path[1:rng]
        for move in moves:
            move.distance = 1000
        print "move", self.movePath
        print "path", path

    def doAttack(self):
        if len(self.attackPath) is 0:
            return ' '
        else:
            move = self.attackPath.pop(0)
            return sel[move]

    def doMove(self):
        if len(self.movePath) is 0 or self.movePath[0] is 0:
            return ' '
        else:
            move = self.movePath.pop(0)
            return sel[move]

    def doTurn(self, cursorx, cursory):
        if self.currentCharacter is not 0 and \
                self.currentCharacter.move is not Turn.Done:
            character = self.currentCharacter
            print cursorx, cursory, character.position.x, character.position.y
            if cursorx is character.position.x and cursory is character.position.y:
                return ' '
            else:
                return 'd'
        else:
            for character in self.cpu.characters:
                if character.move is not Turn.Done:
                    break
            if cursorx is character.position.x and cursory is character.position.y:
                self.currentCharacter = character
                self.planTurn(character)
                return ' '
            else:
                return 'd'
