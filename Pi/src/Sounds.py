import pygame

#sudo amixer cset numid=3 1

def init_music():
    pygame.mixer.init()  # initialize pygame
    pygame.mixer.music.load("Gumi.wav") # load main music
    pygame.mixer.music.play(-1) # -1 for infinite loop

def init_sfx():
    global sfx # initialize global
    sfx = [] # create an array of objects
    sfx.append(pygame.mixer.Sound("Gumi.wav")) # can append more depending on # of SFX
	
def play_sfx(sfx_num):
    sfx[sfx_num].play(0) #0 for repeat once 
	
