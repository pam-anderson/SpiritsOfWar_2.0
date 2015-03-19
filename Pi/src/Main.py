from GameController import Game
from Sounds import Sound

def main():
    game = Game()
    sound = Sound()
    sound.init_music() # comment in for music. 
    sound.init_sfx()   # use command "sudo amixer cset numid=3 1"
    game.playGame()

if __name__ == "__main__":
    main()
