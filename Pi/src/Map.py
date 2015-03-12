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
        self.sprite = sprite
        self.distance = 0
        self.explored = False
        self.occupiedBy = 0 

    def tileIsMoveable(self, teamId):
    # Even though we don't use teamId, we want the same arguments as
    # tileIsAttackable since these will be passed to the DFS
        if not self.explored and self.occupiedBy == 0 and \
            self.sprite == Sprite.Grass:
            return True
        else:
            return False

    def tileIsAttackable(self, teamId):
        if not self.explored and self.occupiedBy != 0 and \
            self.occupiedBy.team != teamId:
            return True
        elif not self.explored and self.occupiedBy == 0 and \
            self.sprite == Sprite.Grass:
            return True
        else:
            return False

class Map:
    def __init__(self):
        self.tiles = [[0 for x in range(MAP_SIZE)] for x in range(MAP_SIZE)]
        for x in range(MAP_SIZE):
            for y in range(MAP_SIZE):
                self.tiles[x][y] = MapTile(x, y, Sprite.Grass)
    
    def depthFirstSearch(self, teamId, charId, x, y, levels, valid):
        queue = [self.tiles[x][y]]
        neighbours = []
        validMoves = [self.tiles[x][y]]
        for level in range(levels):
            for node in queue:
                for direction in Direction:
                    if direction == Direction.Left and \
                            valid(self.tiles[x - 1][y], teamId):
                        self.tiles[x - 1][y].explored = True
                        neighbours.append(self.tiles[x - 1][y])
                        validMoves.append(self.tiles[x - 1][y])
                    elif direction == Direction.Right and \
                            valid(self.tiles[x + 1][y], teamId):
                        self.tiles[x + 1][y].explored = True
                        neighbours.append(self.tiles[x + 1][y])
                        validMoves.append(self.tiles[x + 1][y])
                    elif direction == Direction.Up and \
                            valid(self.tiles[x][y - 1], teamId):
                        self.tiles[x][y - 1].explored = True
                        neighbours.append(self.tiles[x][y - 1])
                        validMoves.append(self.tiles[x][y - 1])
                    elif direction == Direction.Down:
                        if valid(self.tiles[x][y + 1], teamId):
                            self.tiles[x][y + 1].explored = True
                            neighbours.append(self.tiles[x][y + 1])
                            validMoves.append(self.tiles[x][y + 1])
                        queue.remove(node) 
            queue = list(neighbours)
            neighbours = []
        for node in validMoves:
            node.explored = False
        return validMoves
