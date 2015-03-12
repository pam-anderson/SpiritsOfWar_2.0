from enum import Enum

# GLOBALS
CHARS_PER_PLAYER = 3

class Turn(Enum):
    Move, Attack, Done = range(3)

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
        self.standingSprite = team * 3 + 3 + characterId
        self.animationSprite = characterId * 8 + 9

class Player:
    def __init__(self, characters):
        self.characters = characters
        self.charactersRemaining = CHARS_PER_PLAYER

    def isTurnDone(self):
        for character in self.characters:
            if character.move != Turn.Done and character.currentHp > 0:
                return False
        return True

    def resetTurn(self):
        for character in characters:
            character.move = Turn.Move
