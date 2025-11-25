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

#Classes

class Player:
    def __init__(self, x, y, img, l, h, score, lives):
        self.x = x
        self.y = y
        self.img = pygame.transform.scale(img, (l, h))
        self.l = l
        self.h = h
        self.score = score
        self.lives = lives
    
    def update(self):
        self.rect = pygame.Rect(self.x, self.y, self.l, self.h)
        
class Invader:
    def __init__(self, x, y, img, l, h, health, bullet_type):
        self.x = x
        self.y = y
        self.img = pygame.transform.scale(img, (l, h))
        self.rect = pygame.Rect(self.x, self.y, self.l, self.h)
        self.l = l
        self.h = h
        self.direction = -1  
        self.health = health
        self.bullet_type = bullet_type
        
    def update(self):
        self.rect = pygame.Rect(self.x, self.y, self.l, self.h)
        
class Bullet:
    def __init__(self):
        
        
        
        

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

