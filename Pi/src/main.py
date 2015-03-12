from initialize import initializePlayers
from initialize import initializeMap
from map import MapTile

def main():
    players = initializePlayers()
    gameMap = initializeMap()
    nodes = gameMap.depthFirstSearch(0, 0, 4, 4, 1, MapTile.tileIsMoveable)
    for node in nodes:
        print node.x, node.y

if __name__ == "__main__":
    main()
