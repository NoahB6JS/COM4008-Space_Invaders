import sys
import pygame
import random

#---------------------------The game assets---------------------------

pygame.init()
pygame.mixer.init()
player_img = pygame.image.load("Media/player.png")
invader_img = pygame.image.load("Media/invader.png")
alien_img = pygame.image.load("Media/alien.png")
squid_img = pygame.image.load("Media/squid.png")
ufo_img = pygame.image.load("Media/ufo.png")
bg_img = pygame.image.load("Media/bg.jpg")

INVADER_TYPES = {
    "alien": {"img": alien_img, "health": 1, "bullet_speed": 3, "fire_rate": 0.002, "points": 10},
    "squid": {"img": squid_img, "health": 2, "bullet_speed": 4, "fire_rate": 0.004, "points": 20},
    "invader": {"img": invader_img, "health": 3, "bullet_speed": 5, "fire_rate": 0.006, "points": 50},
}

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

class Game:
    def __init__(self):
        self.level = 1
        self.score = 0
        self.invaders = []
        self.enemy_bullets = []
        self.font = pygame.font.Font(None, 32)
        self.FPS = 60
        self.clock = pygame.time.Clock()
        self.SCREEN_HEIGHT = 500
        self.SCREEN_WIDTH = 500
        self.screen = pygame.display.set_mode([self.SCREEN_WIDTH, self.SCREEN_HEIGHT])

#-----------------------The in game screens---------------------------------------
    def start_screen(self):
        font = pygame.font.Font(None, 48)
        text = font.render("Space Invaders", True, (255, 255, 255))
        start_text = font.render("Press SPACE to start", True, (255, 255, 255))
        running = True
        while running:
            for event in pygame.event.get():
                if event.type == pygame.QUIT:
                    pygame.quit()
                    sys.exit()
                if event.type == pygame.KEYDOWN and event.key == pygame.K_SPACE:
                    running = False
            self.screen.blit(bg_img, (0, 0))
            self.screen.blit(start_text, (100, 200))
            self.screen.blit(text, (120, 100))
            pygame.display.flip()

    def draw_invaders(self):
        self.invaders.clear()
        config = self.get_level_config()
        ROWS = config["rows"]
        COLS = config["cols"]
        START_X = 60
        SPACING_X = 45
        START_Y = 40
        SPACING_Y = 35

        for row in range(ROWS):
            for col in range(COLS):
                x = START_X + col * SPACING_X
                y = START_Y + row * SPACING_Y
                
                
            
                if self.level >= 3:
                    if row < 1:
                        inv_type = "invader"  
                elif row < 3:
                    inv_type = "squid"
                else:
                  inv_type = "alien"
                
                types = INVADER_TYPES[inv_type]
            
                inv = Invader(
                    x, y,
                    types["img"],
                    l=40, h=40,
                    health=types["health"],
                    bullet_speed=types["bullet_speed"],
                    point_value=types["points"],
                    fire_rate=types["fire_rate"]
            )
            
                inv.speed = 1 + self.level * 0.01  
                self.invaders.append(inv)
            
            
    # --- Game helpers ---
    def score_level_display(self, screen):
        score_text = self.font.render(f"Score: {self.score}", True, (255, 255, 255))
        level_text = self.font.render(f"Level: {self.level}", True, (255, 255, 255))
        screen.blit(score_text, (10, 10))
        screen.blit(level_text, (self.SCREEN_WIDTH - level_text.get_width() - 10, 10))

    def invader_movement(self):
        hit_wall = False
        for inv in self.invaders:
            inv.move()
            self.screen.blit(inv.img, (inv.x, inv.y))
            next_x = inv.x + inv.speed * inv.direction
            if next_x <= 0 or next_x + inv.l >= self.SCREEN_WIDTH:
                hit_wall = True
        if hit_wall:
            for inv in self.invaders:
                inv.direction *= -1
                inv.y += 10

    def update_enemy_bullets(self):
        for bullet in self.enemy_bullets[:]:
            bullet.update()
            pygame.draw.rect(self.screen, (0, 255, 0), bullet.rect)
            if bullet.y > self.SCREEN_HEIGHT:
                self.enemy_bullets.remove(bullet)

    def pick_invader_type(self):
        level = self.level
        prob_invader = min(0.004 + level * 0.004, 0.008)
        prob_squid = min(0.08 + level * 0.08, 0.4)
        r = random.random()
        if r < prob_invader:
            return "invader"
        elif r < prob_invader + prob_squid:
            return "squid"
        else:
            return "alien"

    def get_level_config(self):
        level = self.level
        config = {}
        config["speed"] = 0.5 + (level * 0.00005)
        config["enemy_fire_rate"] = 0.001 + (level * 0.0003)
        config["rows"] = min(5 + level // 2, 10)
        config["cols"] = min(8 + level // 3, 12)
        return config

    def draw(self):
        self.screen.blit(bg_img, (0, 0))
        self.score_level_display(self.screen)

#---------------------------The game loop---------------------------

game = Game()
game.start_screen()
game.draw_invaders()

running = True
while running:
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            running = False
            pygame.quit()
            sys.exit()

    game.draw()
    game.invader_movement()
    game.update_enemy_bullets()

    for inv in game.invaders:
        bullet = inv.chance_of_shot()
        if bullet:
            game.enemy_bullets.append(bullet)
            shoot_sound.play()
            
    pygame.display.flip()
    game.clock.tick(game.FPS)