from enum import Enum

CHARS_PER_PLAYER = 3

# CLASS STATS
WARRIOR_HP = 10
WARRIOR_ATK = 5
WARRIOR_DEF = 5
WARRIOR_RANGE = 1
WARRIOR_MVMNT = 2

MAGE_HP = 12
MAGE_ATK = 6
MAGE_DEF = 4
MAGE_RANGE = 3
MAGE_MVMNT = 2

RANGER_HP = 8
RANGER_ATK = 4
RANGER_DEF = 4
RANGER_RANGE = 2
RANGER_MVMNT = 3

class Turn(Enum):
    Move, Attack, Done = range(3)

class Input(Enum):
    Up, Down, Left, Right, Esc, Enter, Next = range(7)

class CharacterClass:
    def __init__(self, name, healthPoints, attack, defense, attackRange,
            movement):
        self.className = name
        self.maxHp = healthPoints
        self.attack = attack
        self.defense = defense
        self.attackRange = attackRange
        self.movement = movement

class Character:
    def __init__(self, characterClass, team, characterId):
        self.characterClass = characterClass
        self.currentHp = characterClass.maxHp
        self.team = team
        self.characterId = characterId
        self.position = [0, 0] # [x coord, y coord]
        self.move = Turn.Move

class Player:
    def __init__(self, characters):
        self.characters = characters
        self.charactersRemaining = CHARS_PER_PLAYER
        self.cursor = [0, 0]

    def isTurnDone(self):
        for character in self.characters:
            if character.move != Turn.Done and character.currentHp > 0:
                return False
        return True

    def resetTurn(self):
        for character in self.characters:
            character.move = Turn.Move

    def currentMove(self):
        move = Turn.Done
        for character in self.characters:
            if character.move < move:
                move = character.move
        return move

def initializeClasses():
    classes = []
    classes.append(CharacterClass("warrior", WARRIOR_HP, WARRIOR_ATK,
        WARRIOR_DEF, WARRIOR_RANGE, WARRIOR_MVMNT))
    classes.append(CharacterClass("mage", MAGE_HP, MAGE_ATK, MAGE_DEF,
        MAGE_RANGE, MAGE_MVMNT))
    classes.append(CharacterClass("ranger", RANGER_HP, RANGER_ATK, RANGER_DEF,
        RANGER_RANGE, RANGER_MVMNT))
    return classes    

def initializeCharacters(team):
    characters = []
    classes = initializeClasses()
    for characterClass, i in zip(classes, range(len(classes))):
        characters.append(Character(characterClass, team, i))
    return characters

def initializePlayers():
    players = []
    players.append(Player(initializeCharacters(0)))
    players.append(Player(initializeCharacters(1)))
    return players

