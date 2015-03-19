import pygame

# Run the following command first!
# sudo amixer cset numid=3 1

class Sound:
    sfx = []
    def init_music(self):
        pygame.mixer.init()  # initialize pygame
        pygame.mixer.music.load("mus.wav") # load main music
        pygame.mixer.music.play(-1) # -1 for infinite loop

    def init_sfx(self):
        sfx.append(pygame.mixer.Sound("war.wav")) # can append more depending on # of SFX
        sfx.append(pygame.mixer.Sound("arch.wav"))
        sfx.append(pygame.mixer.Sound("mag.wav"))
        sfx.append(pygame.mixer.Sound("mov.wav"))
        sfx.append(pygame.mixer.Sound("die.wav"))
	
    def play_sfx(self, sfx_num):
        sfx[sfx_num].play(0) #0 for repeat once 
	
