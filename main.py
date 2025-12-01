#Imported modules

import sys
import pygame
import random

pygame.init()
pygame.mixer.init()

#--Image Files loaded in and set to variables

player_img = pygame.image.load("Media/player.png")
invader_img = pygame.image.load("Media/invader.png")
alien_img = pygame.image.load("Media/alien.png")
squid_img = pygame.image.load("Media/squid.png")
ufo_img = pygame.image.load("Media/ufo.png")
bg_img = pygame.image.load("Media/bg.jpg")

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
        self.start_x = x
        self.start_y = y
        
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
 
class Game:
    def __init__(self):
        self.level = 1
        self.score = 0
        self.invaders = []
        self.invader_startrow = 10
        self.invader_endrow = 300
        self.invader_startcol = 100
        self.invader_endcol = 400 
        self.enemy_bullets = []
        self.enemy_bullet_speed = 5
        self.font = pygame.font.Font(None, 32)
        
    def draw_invaders(self):

        self.invaders.clear()
        config = get_level_config(self.level)
        ROWS = config["rows"]
        COLS = config["cols"]

        START_X = 60
        SPACING_X = 45
        START_Y = 40
        SPACING_Y = 35

        for r in range(ROWS):
            for c in range(COLS):

                inv_type = pick_invader_type(self.level)
                t = INVADER_TYPES[inv_type]
                x = START_X + c * SPACING_X
                y = START_Y + r * SPACING_Y
                inv = Invader(x,y,t["img"],40, 40,t["health"],t["bullet_speed"],t["points"],t["fire_rate"])
                inv.speed = config["speed"]
                self.invaders.append(inv)
          
    def start_screen(self):
        font = pygame.font.Font(None, 48)
        text = font.render("Space Invaders", True, (255,255,255))
        start_text = font.render("Press SPACE to start", True, (255,255,255))

        running = True
        while running:
            for event in pygame.event.get():
                if event.type == pygame.QUIT:
                    pygame.quit()
                    sys.exit()
                if event.type == pygame.KEYDOWN and event.key == pygame.K_SPACE:
                    running = False
            screen.blit(bg_img, (0,0))
            screen.blit(start_text, (100,200))
            screen.blit(text, (120,100))  
            pygame.display.flip()
            
    def game_over_screen(self):
        font = pygame.font.Font(None, 48)
        game_over_text= font.render("GAME OVER", True, (255,255,255))
        game_over_text2 = font.render("press SPACE to restart", True, (255,255,255))
        
        running = True
        while running:
            for event in pygame.event.get():
                if event.type == pygame.QUIT:
                    pygame.quit()
                    sys.exit()
                if event.type == pygame.KEYDOWN and event.key == pygame.K_SPACE:
                    running = False
            screen.blit(bg_img, (0,0))
            screen.blit(game_over_text, (150,200))
            screen.blit(game_over_text2, (85,300))
            pygame.display.flip()
            
    def next_level_screen(self):
        font = pygame.font.Font(None, 48)
        game_over_text= font.render(f"Level: {self.level} complete", True, (255,255,255))
        game_over_text2 = font.render("press SPACE to continue", True, (255,255,255))
        
        running = True
        while running:
            for event in pygame.event.get():
                if event.type == pygame.QUIT:
                    pygame.quit()
                    sys.exit()
                if event.type == pygame.KEYDOWN and event.key == pygame.K_SPACE:
                    running = False
            screen.blit(bg_img, (0,0))
            screen.blit(game_over_text, (150,200))
            screen.blit(game_over_text2, (85,300))
            pygame.display.flip()


    def score_level_display(self, screen):
        score_text = self.font.render(f"Score: {self.score}", True, (255, 255, 255))
        level_text = self.font.render(f"Level: {self.level}", True, (255, 255, 255))
        screen.blit(score_text, (10, 10))
        screen.blit(level_text, (SCREEN_WIDTH - level_text.get_width() - 10, 10))

    def invaders_shoot(self):
        for inv in self.invaders:
        
            if random.random() < inv.fire_rate:
                self.enemy_bullets.append(
                    Bullet(
                        inv.x + inv.l//2,
                        inv.y + inv.h,
                        4, 10,
                        speed=inv.bullet_speed,
                        owner="enemy"
                )
            )
                
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
    config["speed"] = 1 + (level * 0.15)
    config["enemy_fire_rate"] = 0.001 + (level * 0.0003)
    config["rows"] = min(5 + level // 2, 10)   
    config["cols"] = min(8 + level // 3, 12)   
    return config

def pick_invader_type(level):

    prob_invader = min(0.4 + level * 0.4, 0.8)     #Change the invader spawinng chances
    prob_squid = min(0.08 + level * 0.08, 0.4)   
    r = random.random()
    if r < prob_invader:
        return "invader"
    elif r < prob_invader + prob_squid:
        return "squid"
    else:
        return "alien" 
        


FPS = 60
clock = pygame.time.Clock()
SCREEN_HEIGHT = 500
SCREEN_WIDTH = 500
screen = pygame.display.set_mode([SCREEN_WIDTH, SCREEN_HEIGHT])


game = Game()
game.start_screen()
game.draw_invaders()


running = True
while running:
    game.invaders_shoot()
    
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            running = False
            pygame.quit()
            sys.exit()
                

    screen.blit(bg_img, (0,0))
    game.score_level_display(screen)
            
    for inv in game.invaders:
        screen.blit(inv.img, (inv.x, inv.y))
        inv.update()
        
    
    for inv in game.invaders:
        inv.x += inv.speed * inv.direction
        inv.update()   
        
    for inv in game.invaders:
        if inv.x <= 0 or inv.x + inv.l >= SCREEN_WIDTH:
            for i in game.invaders:
                i.direction *= -1
                i.y += 10
                             
            break
    
    for bullet in game.enemy_bullets[:]:
        bullet.update()
        pygame.draw.rect(screen, (0, 255, 0), bullet.rect) 

        if bullet.y > SCREEN_HEIGHT:
            game.enemy_bullets.remove(bullet)
                 
    pygame.display.flip()
    clock.tick(FPS)

