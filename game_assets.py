import sys
import pygame
import random
import os

#mixing sound files before loop (dont delete)
pygame.init()
pygame.mixer.init()

#Media checkerr
check_files = ["Media/player.png", "Media/invader.png", "Media/alien.png",
               "Media/squid.png", "Media/ufo.png", "Media/bg.png",
                "Media/sound/soundtrack.wav","Media/sound/laser.wav"]

#EXCEPTION HANDLING FOR THE MEDIA FILE BEFORE GAME STARTS.

for file in check_files:
    try:
        if file[-3:] == "png": #CHecks files extension
            file = pygame.image.load(file)
        else:
            file = pygame.mixer.Sound(file)
    except Exception as e:
        print(f"ERROR LOADING MEDIA: {file}: {e}") #error message if file not found
        pygame.quite()
        sys.exit()
 
#---------------------------The game assets---------------------------

player_img = pygame.image.load("Media/player.png")
invader_img = pygame.image.load("Media/invader.png")
alien_img = pygame.image.load("Media/alien.png")
squid_img = pygame.image.load("Media/squid.png")
ufo_img = pygame.image.load("Media/ufo.png")
bg_img = pygame.image.load("Media/bg.png")
soundtrack_sound = pygame.mixer.Sound("Media/sound/soundtrack.wav")
shoot_sound = pygame.mixer.Sound("Media/sound/laser.wav")

try: #Tries to tune background sound
    pygame.mixer.music.load("Media/sound/soundtrack.wav")
    pygame.mixer.music.set_volume(0.3)
    pygame.mixer.music.play(-1)
except Exception:
    pass

#INVADER TYPES DICTIONARY

INVADER_TYPES = {
    "alien": {"img": alien_img, "health": 1, "bullet_speed": 3, "fire_rate": 0.002, "points": 10},
    "squid": {"img": squid_img, "health": 2, "bullet_speed": 4, "fire_rate": 0.004, "points": 20},
    "invader": {"img": invader_img, "health": 3, "bullet_speed": 5, "fire_rate": 0.006, "points": 30},
}

#---------------------------my classes---------------------------
class Actor:
    def __init__(self, x, y, img, l, h, speed, direction):
        self.x = x
        self.y = y
        self.img = pygame.transform.scale(img, (l, h))
        self.l = l
        self.h = h
        self.rect = pygame.Rect(self.x, self.y, self.l, self.h)
        self.speed = speed
        self.direction = direction

    def update(self):
        self.rect = pygame.Rect(self.x, self.y, self.l, self.h)
class Defender(Actor):
    def __init__(self, x, y, img, l, h, cooldown):
        super().__init__(x, y, img, l, h, speed=0, direction=0) #inheriting the actor class attributes
        self.score = 0
        self.lives = 3
        self.bullet_type = "normal"
        self.cooldown = cooldown

    def update(self):
        self.rect = pygame.Rect(self.x, self.y, self.l, self.h) # updates the users boundaries
class Invader(Actor):
    def __init__(self, x, y, img, l, h, health, bullet_speed, point_value, fire_rate):
        super().__init__(x, y, img, l, h, speed=1, direction=1)
        self.point_value = point_value
        self.health = health
        self.bullet_speed = bullet_speed
        self.fire_rate = fire_rate

    def update(self):
        self.rect = pygame.Rect(self.x, self.y, self.l, self.h) #inheriting the actor class attributes

    def move(self):
        self.x += self.speed * self.direction
        self.update()

    def chance_of_shot(self):
        if random.random() < self.fire_rate:
            return Bullet(self.x + self.l//2, self.y + self.h, 4, 10, self.bullet_speed, "enemy")
        return None
class Bullet:
    def __init__(self, x, y, w, h, speed, owner):
        self.x = x
        self.y = y
        self.width = w
        self.height = h
        self.speed = speed
        self.owner = owner
        self.rect = pygame.Rect(self.x, self.y, w, h)

    def update(self):
        self.y += self.speed
        self.rect.topleft = (self.x, self.y)