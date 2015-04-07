from Map import MAP_SIZE
from Player import Turn
import operator

class ComputerPlayer:
    def __init__(self, gameMap, cpu, opponent):
        self.gameMap = gameMap
        self.cpu = cpu
        self.opponent = opponent
        self.currentPath = []
        self.currentPriority = []

    # Determine which opponents are a priority
    def planTurn(self, character):
        classPrio = {'ranger' : 0, 'mage' : 1, 'warrior' : 2}
        opponents = [self.opponent.characters[0]]
        self.priority = []
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
            nearby = 1 if opp.position.distance > threshold else i
            if opponents[opponents.index(opp) - 1].position.distance == \
                opp.position.distance:
                dist = opponents.index(opp) - 1
            else:
                dist = opponents.index(opp)
            prioVal = dist + \
                      classPrio[opp.characterClass.className] + nearby
            priority.append((opp, prioVal))
            self.currentPriority = priority
        print "priority", len(priority), priority
        self.findPath()
        for move in moves:
            move.distance = 1000
        print"calling make priority"
        self.priority.sort(key=operator.itemgetter(1), reverse=False)


        

    # Determine who to attack
    # Finds the highest priority target within attack range and attacks.
    # Returns enemy index if within attack range, otherwise returns -1 
    def findAttack(self, charRange):
        index = 0
        opponents = [self.opponent.characters[0]]
        for opp in self.opponent.characters[0:]:
            if opp.position.distance <= charRange:
                break;
            else: index += 1      
        if index < 3:          
            return index
        else : return -1

                
        pass             
    # Determine where to move
    def findPath(self):
        x = self.currentPriority[0][0].position.x
        y = self.currentPriority[0][0].position.y
        path = [0] * (self.currentPriority[0][0].position.distance + 1)
        self.gameMap.getPath(x, y, path)
        self.currentPath = path[1:]
        print "path", path
        pass

    def doTurn(self, cursorx, cursory):
        for character in self.cpu.characters:
            if character.move is not Turn.Done:
                break
        if cursorx is character.position.x and cursory is character.position.y:
            return ' '
        else:
            return 's'
