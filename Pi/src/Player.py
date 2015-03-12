
# GLOBALS
CHARS_PER_PLAYER = 3

class CharacterClass:
    def __init__(self, name, healthPoints, attack, defense, attackRange,
            movement):
        self.className = name
        self.healthPoints = healthPoints
        self.attack = attack
        self.defense = defense
        self.attackRange = attackRange
        self.movement = movement

class Character:
    def __init__(self, characterClass, team, characterId):
        self.characterClass = characterClass
        self.team = team
        self.characterId = characterId
        self.position = [0, 0] # [x coord, y coord]

class Player:
    def __init__(self, characters):
        self.characters = characters
        self.charactersRemaining = CHARS_PER_PLAYER
