import sys
import time
import pygame
import random

pygame.init()
pygame.mixer.init()

# -------------------- IMAGE ASSETS --------------------
player_img = pygame.image.load("Media/player.png")
invader_img = pygame.image.load("Media/invader.png")
alien_img = pygame.image.load("Media/alien.png")
squid_img = pygame.image.load("Media/squid.png")
ufo_img = pygame.image.load("Media/ufo.png")
bg_img = pygame.image.load("Media/bg.jpg")

# ---- Barrier images ----
barrier_full_img = pygame.image.load("Media/barrier_full.png")
barrier_cracked_img = pygame.image.load("Media/barrier_cracked.png")
barrier_shattered_img = pygame.image.load("Media/barrier_shattered.png")

# ---------------------- SOUND CHECK ----------------------
def check_sound_path(path):
    try:
        return pygame.mixer.Sound(path)
    except Exception:
        return None

invader_killed = check_sound_path("Media/sound/invaderkilled.wav")
player_loose_life = check_sound_path("Media/sound/lose_life.wav")

# ---------------------- INVADER TYPES ----------------------
INVADER_TYPES = {
    "alien": {
        "img": alien_img,
        "health": 1,
        "bullet_speed": 3,
        "points": 10,
        "fire_rate": 0.001
    },
    "squid": {
        "img": squid_img,
        "health": 2,
        "bullet_speed": 4,
        "points": 20,
        "fire_rate": 0.0012
    },
    "invader": {
        "img": invader_img,
        "health": 3,
        "bullet_speed": 5,
        "points": 50,
        "fire_rate": 0.0015
    }
}

# ---------------------- CLASSES ----------------------

class Bullet:
    def __init__(self, x, y, speed, from_player=False):
        self.x = x
        self.y = y
        self.speed = speed
        self.from_player = from_player
        self.rect = pygame.Rect(self.x, self.y, 4, 12)

    def update(self):
        self.y += self.speed
        self.rect.topleft = (self.x, self.y)


class Invader:
    def __init__(self, x, y, img, l, h, health, bullet_speed, point_value, fire_rate):
        self.x = x
        self.y = y
        self.img = img
        self.l = l
        self.h = h
        self.health = health
        self.bullet_speed = bullet_speed
        self.point_value = point_value
        self.fire_rate = fire_rate
        self.direction = 1
        self.speed = 1

    def move(self):
        self.x += self.speed * self.direction

    def take_damage(self):
        self.health -= 1
        return self.health <= 0

    def shoot(self):
        if random.random() < self.fire_rate:
            return Bullet(self.x + self.l // 2, self.y + self.h, self.bullet_speed)
        return None

    def update(self, screen, width):
        screen.blit(self.img, (self.x, self.y))
        if self.x <= 0 or self.x + self.l >= width:
            return True
        return False


class Defender:
    def __init__(self, x, y, img, l, h, cooldown):
        self.x = x
        self.y = y
        self.img = img
        self.l = l
        self.h = h
        self.cooldown = cooldown
        self.cooldown_timer = 0
        self.lives = 3

    def movement(self, screen_width, bullets):
        keys = pygame.key.get_pressed()

        if keys[pygame.K_LEFT] and self.x > 0:
            self.x -= 5

        if keys[pygame.K_RIGHT] and self.x + self.l < screen_width:
            self.x += 5

        if keys[pygame.K_SPACE] and self.cooldown_timer == 0:
            bullets.append(Bullet(self.x + self.l//2, self.y, -7, True))
            self.cooldown_timer = self.cooldown

        if self.cooldown_timer > 0:
            self.cooldown_timer -= 1


# --------------------------------------------------------
#                ⭐ BARRIER CLASS
# --------------------------------------------------------

class Barrier:
    def __init__(self, x, y):
        self.x = x
        self.y = y
        self.stage = 0  # 0=full, 1=cracked, 2=shattered

        self.images = [
            barrier_full_img,
            barrier_cracked_img,
            barrier_shattered_img
        ]

        self.rect = self.images[self.stage].get_rect(topleft=(x, y))

    def take_damage(self):
        self.stage += 1
        if self.stage >= 3:
            return True
        self.rect = self.images[self.stage].get_rect(topleft=(self.x, self.y))
        return False

    def draw(self, screen):
        screen.blit(self.images[self.stage], (self.x, self.y))


# ---------------------- GAME CLASS ----------------------

class Game:
    def __init__(self):
        self.level = 1
        self.score = 0
        self.invaders = []
        self.enemy_bullets = []
        self.player_bullets = []
        self.barriers = []

        self.font = pygame.font.Font(None, 32)
        self.FPS = 60
        self.clock = pygame.time.Clock()

        self.SCREEN_WIDTH = 500
        self.SCREEN_HEIGHT = 500
        self.screen = pygame.display.set_mode([self.SCREEN_WIDTH, self.SCREEN_HEIGHT])

    # ------------------ BARRIERS ------------------
    def create_barriers(self):
        barrier_y = self.SCREEN_HEIGHT - 150
        spacing = self.SCREEN_WIDTH // 4
        positions = [spacing - 40, spacing*2 - 40, spacing*3 - 40]
        self.barriers = [Barrier(x, barrier_y) for x in positions]

    # ------------------ SCREENS ------------------
    def start_screen(self):
        font = pygame.font.Font(None, 48)
        title = font.render("SPACE INVADERS", True, (255,255,255))
        start = font.render("Press SPACE to Start", True, (255,255,255))

        while True:
            for event in pygame.event.get():
                if event.type == pygame.QUIT:
                    pygame.quit()
                    sys.exit()
                if event.type == pygame.KEYDOWN and event.key == pygame.K_SPACE:
                    return

            self.screen.blit(bg_img, (0, 0))
            self.screen.blit(title, (100, 120))
            self.screen.blit(start, (80, 250))
            pygame.display.flip()

    def level_up_screen(self):
        font = pygame.font.Font(None, 48)
        text = font.render(f"Level {self.level} Complete!", True, (255,255,255))
        score_text = font.render(f"Score: {self.score}", True, (255,255,255))

        self.screen.blit(bg_img, (0,0))
        self.screen.blit(text, (100, 150))
        self.screen.blit(score_text, (140, 250))
        pygame.display.flip()
        time.sleep(2)

    def end_screen(self):
        font = pygame.font.Font(None, 48)
        text = font.render("GAME OVER", True, (255,0,0))
        score_text = font.render(f"Final Score: {self.score}", True, (255,255,255))

        while True:
            for event in pygame.event.get():
                if event.type == pygame.QUIT:
                    pygame.quit()
                    sys.exit()

            self.screen.blit(bg_img, (0,0))
            self.screen.blit(text, (130, 150))
            self.screen.blit(score_text, (150, 230))
            pygame.display.flip()

    # ------------------ INVADERS ------------------
    def draw_invaders(self):
        self.invaders.clear()
        config = self.get_level_config()

        rows = config["rows"]
        COLS = 8
        START_X = 60
        SPACING_X = 45
        START_Y = 40
        SPACING_Y = 35
        max_row = 8

        for row in range(min(rows, max_row)):
            for col in range(COLS):
                x = START_X + col*SPACING_X
                y = START_Y + row*SPACING_Y

                if self.level >= 6:
                    inv_type = "invader" if row == 0 else "squid" if row < 3 else "alien"
                elif self.level >= 3:
                    inv_type = "squid" if row == 0 else "alien"
                else:
                    inv_type = "alien"

                stats = INVADER_TYPES[inv_type]

                inv = Invader(
                    x, y,
                    stats["img"],
                    l=40, h=40,
                    health=stats["health"],
                    bullet_speed=stats["bullet_speed"] + self.level,
                    point_value=stats["points"],
                    fire_rate=stats["fire_rate"] + (self.level * 0.00002)
                )

                inv.speed = 1 + self.level * 0.01
                self.invaders.append(inv)

    # ------------------ DISPLAY ------------------
    def score_level_display(self):
        score_text = self.font.render(f"Score: {self.score}", True, (255,255,255))
        level_text = self.font.render(f"Level: {self.level}", True, (255,255,255))
        lives_text = self.font.render(f"Lives: {self.player.lives}", True, (255,255,255))

        self.screen.blit(score_text, (10, 10))
        self.screen.blit(level_text, (400, 10))
        self.screen.blit(lives_text, (215, 10))

    # ------------------ BULLET + COLLISIONS ------------------

    def handle_player_bullets(self):
        for bullet in self.player_bullets[:]:
            bullet.update()
            pygame.draw.rect(self.screen, (255,255,0), bullet.rect)

            # Hit barrier?
            for barrier in self.barriers[:]:
                if bullet.rect.colliderect(barrier.rect):
                    self.player_bullets.remove(bullet)
                    if barrier.take_damage():
                        self.barriers.remove(barrier)
                    break

            # Hit invader?
            for inv in self.invaders[:]:
                if bullet.rect.colliderect(pygame.Rect(inv.x, inv.y, inv.l, inv.h)):
                    self.player_bullets.remove(bullet)

                    if inv.take_damage():
                        self.score += inv.point_value
                        if invader_killed:
                            invader_killed.play()
                        self.invaders.remove(inv)

                        # Speed up remaining invaders
                        for x in self.invaders:
                            x.speed += 0.05
                    break

            if bullet.y < 0:
                self.player_bullets.remove(bullet)

    def handle_enemy_bullets(self):
        for bullet in self.enemy_bullets[:]:
            bullet.update()
            pygame.draw.rect(self.screen, (0,255,0), bullet.rect)

            # Hit barrier?
            for barrier in self.barriers[:]:
                if bullet.rect.colliderect(barrier.rect):
                    self.enemy_bullets.remove(bullet)
                    if barrier.take_damage():
                        self.barriers.remove(barrier)
                    break

            # Hit player?
            if bullet.rect.colliderect(pygame.Rect(self.player.x, self.player.y, self.player.l, self.player.h)):
                self.enemy_bullets.remove(bullet)
                self.player.lives -= 1
                if player_loose_life:
                    player_loose_life.play()
                if self.player.lives <= 0:
                    self.end_screen()

            if bullet.y > self.SCREEN_HEIGHT:
                self.enemy_bullets.remove(bullet)

    # ------------------ LEVEL CONFIG ------------------
    def get_level_config(self):
        return {
            "speed": 0.5 + (self.level * 0.00005),
            "enemy_fire_rate": 0.001 + (self.level * 0.0003),
            "rows": min(5 + self.level // 2, 10)
        }

    # ------------------ DRAW ------------------
    def draw(self):
        self.screen.blit(bg_img, (0, 0))
        self.score_level_display()

        for barrier in self.barriers:
            barrier.draw(self.screen)


# --------------------------------------------------------
#                ⭐ GAME LOOP
# --------------------------------------------------------

game = Game()
game.start_screen()
game.draw_invaders()

player_width = 40
player_height = 40

game.player = Defender(
    x=game.SCREEN_WIDTH//2 - player_width//2,
    y=game.SCREEN_HEIGHT - player_height - 20,
    img=player_img,
    l=player_width,
    h=player_height,
    cooldown=20
)

game.create_barriers()

# ---------------- MAIN GAME LOOP ----------------
running = True

while running:
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            running = False
            pygame.quit()
            sys.exit()

    game.player.movement(game.SCREEN_WIDTH, game.player_bullets)

    game.screen.blit(bg_img, (0, 0))
    game.screen.blit(game.player.img, (game.player.x, game.player.y))

    # Move invaders
    hit_wall = False
    for inv in game.invaders:
        if inv.update(game.screen, game.SCREEN_WIDTH):
            hit_wall = True

    if hit_wall:
        for inv in game.invaders:
            inv.direction *= -1
            inv.y += 10

    # Invader shooting
    for inv in game.invaders:
        bullet = inv.shoot()
        if bullet:
            game.enemy_bullets.append(bullet)

    # Update bullets
    game.handle_player_bullets()
    game.handle_enemy_bullets()

    # Draw barriers
    for barrier in game.barriers:
        barrier.draw(game.screen)

    # Check win condition
    if len(game.invaders) == 0:
        game.level += 1
        game.level_up_screen()
        game.draw_invaders()
        game.create_barriers()

    game.score_level_display()
    pygame.display.flip()
    game.clock.tick(game.FPS)
