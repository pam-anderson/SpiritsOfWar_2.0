from enum import Enum
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
    
    def depthFirstSearch(self, character, levels, attackable):
        x = character.position.x
        y = character.position.y
        teamId = character.team
        queue = [self.tiles[x][y]]
        neighbours = []
        validMoves = [self.tiles[x][y]]
        self.tiles[x][y].distance = 0
        for level in range(levels):
            for node in queue:
                for direction in Direction:
                    if direction == Direction.Left and x > 0 and \
                          self.tiles[node.x - 1][node.y].tileIsValid(teamId, attackable):
                        self.tiles[node.x - 1][node.y].explored = True
                        neighbours.append(self.tiles[node.x - 1][node.y])
                        validMoves.append(self.tiles[node.x - 1][node.y])                        
                        self.tiles[node.x - 1][node.y].distance = level + 1
                    elif direction == Direction.Right and x < MAP_SIZE - 1 and \
                          self.tiles[node.x + 1][node.y].tileIsValid(teamId, attackable):
                        self.tiles[node.x + 1][node.y].explored = True
                        neighbours.append(self.tiles[node.x + 1][node.y])
                        validMoves.append(self.tiles[node.x + 1][node.y])
                        self.tiles[node.x + 1][node.y].distance = level + 1
                    elif direction == Direction.Up and y > 0 and \
                          self.tiles[node.x][node.y - 1].tileIsValid(teamId, attackable):
                        self.tiles[node.x][node.y - 1].explored = True
                        neighbours.append(self.tiles[node.x][node.y - 1])
                        validMoves.append(self.tiles[node.x][node.y - 1])
                        self.tiles[node.x][node.y - 1].distance = level + 1
                    elif direction == Direction.Down and y < MAP_SIZE - 1:
                        if self.tiles[node.x][node.y + 1].tileIsValid(teamId, attackable):
                            self.tiles[node.x][node.y + 1].explored = True
                            neighbours.append(self.tiles[node.x][node.y + 1])
                            validMoves.append(self.tiles[node.x][node.y + 1])
                            self.tiles[node.x][node.y + 1].distance = level + 1
                        queue.remove(node) 
            queue = list(neighbours)
            neighbours = []
        for node in validMoves:
            node.explored = False
        return validMoves
