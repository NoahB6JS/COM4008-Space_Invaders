import sys
import pygame
import random

import pygame
from Game import Game

if __name__ == "__main__":
    pygame.init()
    pygame.font.init()
    game = Game()
    game.run()

pygame.init()
pygame.mixer.init()

#--Image Files loaded in and set to variables

player_img = pygame.image.load("Media/player.png")
invader_img = pygame.image.load("Media/invader.png")
alien_img = pygame.image.load("Media/alien.png")
squid_img = pygame.image.load("Media/squid.png")
ufo_img = pygame.image.load("Media/ufo.png")
bg_img = pygame.image.load("Media/bg.jpg")

#Sound files path

def check_sound_path(path):
    try:
        return pygame.mixer.Sound(path)
    except Exception:
        return None


SHOOT_SOUND_PATH = check_sound_path("Media/sound/invaderkilled.wav")
SOUNDTRACK_PATH = check_sound_path("Media/sound/soundtrack.wav")

shoot_sound = check_sound_path(SHOOT_SOUND_PATH)
soundtrack_sound = check_sound_path(SOUNDTRACK_PATH)

try:
    pygame.mixer.music.load("Media/sound/soundtrack.wav")
    pygame.mixer.music.set_volume(0.3)
    pygame.mixer.music.play(-1)
except Exception:
    pass

#----Classes
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
        super().__init__(x, y, img, l, h, speed=0, direction=0)
        self.score = 0
        self.lives = 3
        self.bullet_type = "normal"
        self.cooldown = cooldown
        
    def update(self):
        self.rect = pygame.Rect(self.x, self.y, self.l, self.h)  
           
class Invader(Actor):
    def __init__(self, x, y, img, l, h, health, bullet_speed, point_value, fire_rate):
        super().__init__(x, y, img, l, h, speed=1, direction=1)
        self.point_value = point_value
        self.health = health 
        self.bullet_speed = bullet_speed
        self.fire_rate = fire_rate

    def update(self):
        self.rect = pygame.Rect(self.x, self.y, self.l, self.h)         

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
 

                
INVADER_TYPES = {
    "alien": {
        "img": alien_img,
        "health": 1,
        "bullet_speed": 3,
        "fire_rate": 0.002,
        "points": 10
    },
    "squid": {
        "img": squid_img,
        "health": 2,
        "bullet_speed": 4,
        "fire_rate": 0.004,
        "points": 20
    },
    "invader": {
        "img": invader_img,
        "health": 3,
        "bullet_speed": 5,
        "fire_rate": 0.006,
        "points": 50
    }
}

def get_level_config(level):
    config = {}
    config["speed"] = 0.5  + (level * 0.00005)
    config["enemy_fire_rate"] = 0.001 + (level * 0.0003)
    config["rows"] = min(5 + level // 2, 10)   
    config["cols"] = min(8 + level // 3, 12)   
    return config

def pick_invader_type(level):

    prob_invader = min(0.004 + level * 0.004, 0.008)     #Change the invader spawinng chances
    prob_squid = min(0.08 + level * 0.08, 0.4)   
    r = random.random()
    if r < prob_invader:
        return "invader"
    elif r < prob_invader + prob_squid:
        return "squid"
    else:
        return "alien" 
        

#Create game instance and start
game = Game.Game()
game.start_screen()
game.draw_invaders()


running = True
while running:
    
    
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            running = False
            pygame.quit()
            sys.exit()
                
    game.screen.blit(bg_img, (0,0))
    game.score_level_display(game.screen)
    game.invader_movement()
    game.invaders_shoot()
    game.score_level_display(game.screen)
    game.screen.blit(bg_img, (0,0))
    game.score_level_display(game.screen)
            
    for inv in game.invaders:
        game.screen.blit(inv.img, (inv.x, inv.y))
        inv.update()
        
    for inv in game.invaders:
        inv.x += inv.speed * inv.direction
        inv.update()   
        
    for inv in game.invaders:
        if inv.x <= 0 or inv.x + inv.l >= game.SCREEN_WIDTH:
            for i in game.invaders:
                i.direction *= -1
                i.y += 10
                             
            break
    
    for bullet in game.enemy_bullets[:]:
        bullet.update()
        pygame.draw.rect(game.screen, (0, 255, 0), bullet.rect) 

        if bullet.y > game.SCREEN_HEIGHT:
            game.enemy_bullets.remove(bullet)
                 
    pygame.display.flip()
    game.clock.tick(game.FPS)

