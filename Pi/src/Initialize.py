from Player import CharacterClass
from Player import Character
from Player import Player 
from Map import Map

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

def initializeMap():
    return Map()
