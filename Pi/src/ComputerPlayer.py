#from GameController import Input
from Map import MAP_SIZE

class ComputerPlayer:
    def __init__(self, gameMap, cpu, opponent):
        self.gameMap = gameMap
        self.cpu = cpu
        self.opponent = opponent

    # Determine which opponents are a priority
    def planTurn(self, character):
        classPrio = {'ranger' : 0, 'mage' : 1, 'warrior' : 2}
        opponents = [self.opponent.characters[0]]
        priority = []
        # Set distance values to determine closeness of opponents
        self.gameMap.depthFirstSearch(character.position.x,
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
            nearby = 1 if opp.position.distance > threshold else 0
            prioVal = opponents.index(opp) + \
                      classPrio[opp.characterClass.className] + nearby
            priority.append((opp, prioVal))
        #    print priority[opponents.index(opp)]

    # Determine who to attack
    def findAttack(self):
        pass

    # Determine where to move
    def findPath(self):
        pass
