import pygame
import sys

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
        self.FPS = 60
        self.clock = pygame.time.Clock()
        self.SCREEN_HEIGHT = 500
        self.SCREEN_WIDTH = 500        
        self.screen = pygame.display.set_mode([self.SCREEN_WIDTH, self.SCREEN_HEIGHT])
        
    def draw_invaders(self):
        self.invaders.clear()
        config = self.get_level_config(self.level)
        ROWS = config["rows"]
        COLS = config["cols"]
        START_X = 60
        SPACING_X = 45
        START_Y = 40
        SPACING_Y = 35

        for r in range(ROWS):
            for c in range(COLS):
                
                x = START_X + c * SPACING_X
                y = START_Y + r * SPACING_Y
                inv_type = pick_invader_type(self.level)
                types = INVADER_TYPES[inv_type]
                inv = Invader(x,y,types["img"],40, 40,types["health"],types["bullet_speed"],types["points"],types["fire_rate"])
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
            self.screen.blit(bg_img, (0,0))
            self.screen.blit(start_text, (100,200))
            self.screen.blit(text, (120,100))  
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
            self.screen.blit(bg_img, (0,0))
            self.screen.blit(game_over_text, (150,200))
            self.screen.blit(game_over_text2, (85,300))
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
            self.screen.blit(bg_img, (0,0))
            self.screen.blit(game_over_text, (150,200))
            self.screen.blit(game_over_text2, (85,300))
            pygame.display.flip()

    def score_level_display(self, screen):
        score_text = self.font.render(f"Score: {self.score}", True, (255, 255, 255))
        level_text = self.font.render(f"Level: {self.level}", True, (255, 255, 255))
        screen.blit(score_text, (10, 10))
        screen.blit(level_text, (self.SCREEN_WIDTH - level_text.get_width() - 10, 10))

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
                shoot_sound.play()
                
    def invader_movement(self):
        hit_wall = False

        for inv in self.invaders:
            self.screen.blit(inv.img, (inv.x, inv.y))
            inv.update()

        for inv in self.invaders:
            next_x = inv.x + inv.speed * inv.direction

            if next_x <= 0 or next_x + inv.l >= self.SCREEN_WIDTH:
                hit_wall = True
                break

        if hit_wall:
            for inv in self.invaders:
                inv.direction *= -1
                inv.y += 10

        for inv in self.invaders:
            inv.x += inv.speed * inv.direction
            inv.update()
 