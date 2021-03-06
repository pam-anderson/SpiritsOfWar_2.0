import pygame
import os

# -------------- IMPORTANT!! ----------------
# Run the following command first!
# sudo amixer cset numid=3 1
# -------------------------------------------

class Sounds:
    def __init__(self):
        self.sfx = []
        # Load main music
        pygame.mixer.init()
        pygame.mixer.music.load("mus.wav") # load main music
        pygame.mixer.music.play(-1) # -1 for infinite loop
        # can append more depending on # of SFX
        # Load sound effects
        if (os.path.isfile("rec_war.wav") == False):
            self.sfx.append(pygame.mixer.Sound("war.wav"))
        else: self.sfx.append(pygame.mixer.Sound("rec_war.wav"))
        if (os.path.isfile("rec_arch.wav") == False):
            self.sfx.append(pygame.mixer.Sound("arch.wav"))
        else: self.sfx.append(pygame.mixer.Sound("rec_arch.wav"))
        if (os.path.isfile("rec_mag.wav") == False):
            self.sfx.append(pygame.mixer.Sound("mag.wav"))
        else: self.sfx.append(pygame.mixer.Sound("rec_mag.wav")) 
        if (os.path.isfile("rec_mov.wav") == False):
            self.sfx.append(pygame.mixer.Sound("mov.wav"))
        else: self.sfx.append(pygame.mixer.Sound("rec_mov.wav"))
        if (os.path.isfile("rec_die.wav") == False):
            self.sfx.append(pygame.mixer.Sound("die.wav"))
        else: self.sfx.append(pygame.mixer.Sound("rec_die.wav"))

    def __del__(self):
        try: os.remove("rec_war.wav")
        except : pass
        try: os.remove("rec_mag.wav")
        except : pass
        try: os.remove("rec_arch.wav")
        except : pass
        try: os.remove("rec_mov.wav")
        except : pass
        try: os.remove("rec_die.wav")   
        except : pass

    def play_sfx(self, sfx_num):
        self.sfx[sfx_num].play(0) #0 for repeat once 
