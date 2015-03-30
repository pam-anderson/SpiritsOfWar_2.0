import pygame

# -------------- IMPORTANT!! ----------------
# Run the following command first!
# sudo amixer cset numid=3 1
# -------------------------------------------

class Sound:
    def __init__(self):
        self.sfx = []
        # Load main music
        pygame.mixer.init()
        pygame.mixer.music.load("mus.wav") # load main music
        pygame.mixer.music.play(-1) # -1 for infinite loop
        # can append more depending on # of SFX
        self.sfx.append(pygame.mixer.Sound("war.wav")) 
        # Load sound effects
        self.sfx.append(pygame.mixer.Sound("arch.wav"))
        self.sfx.append(pygame.mixer.Sound("mag.wav"))
        self.sfx.append(pygame.mixer.Sound("mov.wav"))
        self.sfx.append(pygame.mixer.Sound("die.wav"))

    def play_sfx(self, sfx_num):
        self.sfx[sfx_num].play(0) #0 for repeat once 
