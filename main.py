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


#----Classes
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
        self.l = l
        self.h = h
        self.health = health
        self.rect = pygame.Rect(self.x, self.y, self.l, self.h)
        self.speed = 0.75
        self.direction = -1  
        self.bullet_type = bullet_type
        
    def update(self):
        self.rect = pygame.Rect(self.x, self.y, self.l, self.h)
        
class Bullet:
    def __init__(self, x, y, w, h, s):
        self.x = x
        self.y = y
        self.speed = s
        self.width = w
        self.height = h
        self.rect = pygame.Rect(self.x, self.y, self.width, self.height)
        
    def update(self):
        self.rect = pygame.Rect(self.x, self.y, self.width, self.height)
        
class EnemyBullet:
    def __init__(self, x, y):
        self.x = x
        self.y = y
        self.w = 4
        self.h = 10
        self.speed = 5
        self.rect = pygame.Rect(self.x, self.y, self.w, self.h)

    def update(self):
        self.y += self.speed
        self.rect.topleft = (self.x, self.y)
    

#--Main Game variables

FPS = 60
clock = pygame.time.Clock()

SCREEN_HEIGHT = 500
SCREEN_WIDTH = 500
screen = pygame.display.set_mode([SCREEN_WIDTH, SCREEN_HEIGHT])

score = 0
level = 0

#Invader starting positions in matrix

invaders = []
invader_startrow = 10
invader_endrow = 300
invader_startcol = 100
invader_endcol = 400 

#Draw invaders function

def draw_invaders():
    START_X = 100
    SPACING_X = 45
    START_Y = 30
    SPACING_Y = 35
    ROWS = 5
    COLS = 8
    
    for r in range(ROWS):
        for c in range(COLS):
            x = START_X + c * SPACING_X
            y = START_Y + r * SPACING_Y
            
            health = 1
            bullet_type = "easy"
            
            invaders.append(Invader(x,y,defender_img,40,40,health,bullet_type))
            
draw_invaders()          
            

#--Contains the main game loop

running = True
while running:
    
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            running = False
            pygame.quit()
            sys.exit()
            
            
            
    #background load
    screen.blit(bg_img, (0,0))
            
    #display invaders on screen
    for inv in invaders:
        screen.blit(inv.img, (inv.x, inv.y))
        inv.update()
        
    #Invader movement
    for inv in invaders:
        inv.x += inv.speed * inv.direction
        inv.update()   
        
    for inv in invaders:
        if inv.x <= 0 or inv.x + inv.l >= SCREEN_WIDTH:
            for i in invaders:
                i.direction *= -1
                i.y += 10
                
                    
            break
        
    #Runs screen           
    pygame.display.flip()
    clock.tick(FPS)

