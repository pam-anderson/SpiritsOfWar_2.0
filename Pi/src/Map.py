from enum import Enum
from random import randint
# If getting error about not having module enum, do:
# sudo pip install enum34

MAP_SIZE = 8

class Direction(Enum):
    Left, Right, Up, Down = range(4)

class Sprite(Enum):
    Grass, Water, Rock = range(3)

class MapTile:
    def __init__(self, x, y, sprite):
        self.x = x
        self.y = y
        self.sprite = sprite.value
        self.distance = 1000
        self.explored = False
        self.occupiedBy = 0 

    def tileIsValid(self, teamId, attackable):
        if not self.explored and self.occupiedBy == 0 and \
            self.sprite == Sprite.Grass.value:
            return True
        if attackable and not self.explored and self.occupiedBy != 0 and \
            self.occupiedBy.team != teamId:
            return True
        else:
            return False

class Map:
    def __init__(self):
        self.tiles = [[0 for x in range(MAP_SIZE)] for x in range(MAP_SIZE)]
        for x in range(MAP_SIZE):
            for y in range(MAP_SIZE):
                self.tiles[x][y] = MapTile(x, y, Sprite.Grass)
        self.randomizeMap()

    def randomizeMap(self):
        # Generate random body of water
        size = randint(1, 2)
        lakeX = randint(2, MAP_SIZE - 3)
        lakeY = randint(2, MAP_SIZE - 3)
        lakeTiles = self.depthFirstSearch(lakeX, lakeY, 0, size, 0)
        for tile in lakeTiles:
            tile.sprite = Sprite.Water.value
            tile.distance = 1000
        # Generate random rocks on map
        rocks = randint(5, 10)
        for rock in range(rocks):
            x = randint(2, MAP_SIZE - 3)
            y = randint(0, MAP_SIZE - 1)
            self.tiles[x][y].sprite = Sprite.Rock.value
    
    def depthFirstSearch(self, x, y, teamId, levels, attackable):
        queue = [self.tiles[x][y]]
        neighbours = []
        validMoves = [self.tiles[x][y]]
        self.tiles[x][y].distance = 0
        for level in range(levels):
            for node in queue:
                for direction in Direction:
                    if direction == Direction.Left and node.x > 0 and \
                          self.tiles[node.x - 1][node.y].tileIsValid(teamId, attackable):
                        print node.x - 1, node.y
                        self.tiles[node.x - 1][node.y].explored = True
                        neighbours.append(self.tiles[node.x - 1][node.y])
                        validMoves.append(self.tiles[node.x - 1][node.y]) 
                        self.tiles[node.x - 1][node.y].distance = level + 1
                    elif direction == Direction.Right and node.x < MAP_SIZE - 1 and \
                          self.tiles[node.x + 1][node.y].tileIsValid(teamId, attackable):
                        print node.x + 1, node.y
                        self.tiles[node.x + 1][node.y].explored = True
                        neighbours.append(self.tiles[node.x + 1][node.y])
                        validMoves.append(self.tiles[node.x + 1][node.y])
                        self.tiles[node.x + 1][node.y].distance = level + 1
                    elif direction == Direction.Up and node.y > 0 and \
                          self.tiles[node.x][node.y - 1].tileIsValid(teamId, attackable):
                        print node.x, node.y - 1
                        self.tiles[node.x][node.y - 1].explored = True
                        neighbours.append(self.tiles[node.x][node.y - 1])
                        validMoves.append(self.tiles[node.x][node.y - 1])
                        self.tiles[node.x][node.y - 1].distance = level + 1
                    elif direction == Direction.Down and node.y < MAP_SIZE - 1:
                        if self.tiles[node.x][node.y + 1].tileIsValid(teamId, attackable):
                            print node.x, node.y + 1
                            self.tiles[node.x][node.y + 1].explored = True
                            neighbours.append(self.tiles[node.x][node.y + 1])
                            validMoves.append(self.tiles[node.x][node.y + 1])
                            self.tiles[node.x][node.y + 1].distance = level + 1
            queue = list(neighbours)
            neighbours = []
        for node in validMoves:
            node.explored = False
        return validMoves
