import pygame

# Run the following command first!
# sudo amixer cset numid=3 1

class Sound:
    def __init__(self):
        self.sfx = []
        pygame.mixer.init()
        pygame.mixer.music.load("mus.wav") # load main music
        pygame.mixer.music.play(-1) # -1 for infinite loop
        self.sfx.append(pygame.mixer.Sound("war.wav")) # can append more depending on # of SFX
        self.sfx.append(pygame.mixer.Sound("arch.wav"))
        self.sfx.append(pygame.mixer.Sound("mag.wav"))
        self.sfx.append(pygame.mixer.Sound("mov.wav"))
        self.sfx.append(pygame.mixer.Sound("die.wav"))

    def play_sfx(self, sfx_num):
        sfx[sfx_num].play(0) #0 for repeat once 
	
