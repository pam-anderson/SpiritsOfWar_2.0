MAP_SIZE = 8

class MapTile:
    def __init__(self, x, y, sprite):
        self.x = x
        self.y = y
        self.sprite = sprite
        self.distance = 0
        self.explored = False
        self.occupiedBy = 0

class Map:
    def __init__(self):
        self.gameMap = [[0 for x in range(MAP_SIZE)] for x in range(MAP_SIZE)]
        for x in range(MAP_SIZE):
            for y in range(MAP_SIZE):
                self.gameMap[x][y] = MapTile(x, y, "grass")

