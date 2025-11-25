#Imported modules

import sys
import pygame
import random

pygame.init()
pygame.mixer.init()

#--Image Files loaded in and set to variables

player_img = pygame.image.load("Media/player.png")
defender_img = pygame.image.load("Media/defender.png")
alien_img = pygame.image.load("Media/alien.png")
squid_img = pygame.image.load("Media/squid.png")
ufo_img = pygame.image.load("Media/ufo.png")
bg_img = pygame.image.load("Media/bg.jpg")

#--Main Game variables

FPS = 60
clock = pygame.time.Clock()

SCREEN_HEIGHT = 500
SCREEN_WIDTH = 500
screen = pygame.display.set_mode([SCREEN_HEIGHT, SCREEN_WIDTH])

score = 0
level = 0

#--Contains the main game loop

running = True
while running:
    
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            running = False
            pygame.quit()
            sys.exit()
            
   
#Runs screen           
pygame.display.flip()
clock.tick(FPS)

