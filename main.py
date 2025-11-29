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
    def __init__(self,health, bullet_type,point_value, invader_type):
        self.point_value = point_value
        self.invader_type = invader_type
        self.health = health 
        self.bullet_type = bullet_type
        
    def update(self):
        self.rect = pygame.Rect(self.x, self.y, self.l, self.h) 
        
class Bullet(Actor):
    def __init__(self, w, h,):
        
        self.width = w
        self.height = h

    def update(self):
        self.rect = pygame.Rect(self.x, self.y, self.width, self.height)
        
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
        
      
    def draw_invaders(self):
        self.invaders.clear()
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
            
                self.invaders.append(Invader(x,y,defender_img,40,40,health,bullet_type))
    
    #Start screen           
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
            
    def next_level(self):
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

    def invaders_shoot(self):
        for inv in self.invaders:
            if random.random() < 0.002:  
                self.enemy_bullets.append(
                    EnemyBullet(inv.x + inv.l//2, inv.y + inv.h, self.enemy_bullet_speed)
            )


        
        
        
        
#--Main Game variables

FPS = 60
clock = pygame.time.Clock()
SCREEN_HEIGHT = 500
SCREEN_WIDTH = 500
screen = pygame.display.set_mode([SCREEN_WIDTH, SCREEN_HEIGHT])
        

#--Contains the main game loop

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
                
    #background load
    screen.blit(bg_img, (0,0))
            
    #display invaders on screen
    for inv in game.invaders:
        screen.blit(inv.img, (inv.x, inv.y))
        inv.update()
        
    #Invader movement
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
        
    #Runs screen           
    pygame.display.flip()
    clock.tick(FPS)

