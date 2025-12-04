from game_assets import * #loads in ALL classes and methods from game_assets file and makes them accessible from main.py

class Game:
    def __init__(self):
        self.level = 1
        self.score = 0
        self.invaders = []
        self.enemy_bullets = []
        self.player_bullets = []
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
        rows = config["rows"]
        COLS = 8
        START_X = 60
        SPACING_X = 45
        START_Y = 40
        SPACING_Y = 35

        for row in range(rows):
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
                self.invaders.append(inv) #appending the inv (invader) object and its attributes
            
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


    def get_level_config(self): #level calc for invader sequqnce
        level = self.level #attribute of game starts at 1
        config = {}
        config["speed"] = 0.5 + (level * 0.00005)
        config["enemy_fire_rate"] = 0.001 + (level * 0.0003)
        config["rows"] = min(5 + level // 2, 10)
        return config

    def draw(self):
        self.screen.blit(bg_img, (0, 0))
        self.score_level_display(self.screen)
        
    def check_if_shot_invader(self):
        for bullet in self.player_bullets:
            for inv in self.invaders:
                
                if bullet.rect.colliderect(pygame.Rect(inv.x, inv.y, inv.l, inv.h)):
                    
                 inv.speed += 1
                 inv.health -= 1
                 
                 if inv.health <= 0:
                    self.score += inv.point_value
                    self.invaders.remove(inv)
                 break
            
            
#---------------------------The game loop---------------------------

game = Game() #create game instance
game.start_screen()
game.draw_invaders()

player_width = 40
player_height = 40

game.player = Defender(
    x=game.SCREEN_WIDTH // 2 - player_width // 2,
    y=game.SCREEN_HEIGHT - player_height - 20,
    img=player_img,
    l=player_width,
    h=player_height,
    cooldown=400
    
)

running = True
while running:
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            running = False
            pygame.quit()
            sys.exit()
               
    keys = pygame.key.get_pressed()
    if keys[pygame.K_LEFT] and game.player.x>0:
        game.player.x -=game.player.speed
    elif keys[pygame.K_RIGHT] and game.player.x + game.player.l < game.SCREEN_WIDTH:
             game.player.x += game.player.speed
     #all game methods        
    game.screen.blit(bg_img, (0, 0))   
    game.screen.blit(game.player.img, (game.player.x, game.player.y)) 
    game.invader_movement()  
    game.update_enemy_bullets()  
    game.check_if_shot_invader()  
    game.score_level_display(game.screen)  
    pygame.display.flip()
    game.clock.tick(game.FPS)

    for inv in game.invaders:
        bullet = inv.chance_of_shot()
        if bullet:
            game.enemy_bullets.append(bullet)
            shoot_sound.play()
            
    pygame.display.flip()
    clock.tick(FPS)
    if keys[pygame.K_LEFT] and player.x>0:
        player.X -=player.speed
        if keys[pygame.K_RIGHT] and player.x + player.l < SCREEN_WIDTH:
             player.x += player.speed
    game.clock.tick(game.FPS)
     # Player firing
if keys[pygame.K_SPACE] and player.cooldown_counter == 0:
    game.player_bullets.append(Bullet(player.x + 18, player.y, 4, 10, -7, "player"))
    player.cooldown_counter = player.cooldown
     # Player bullet movement
for bullet in game.player_bullets[:]:
    bullet.update()
    pygame.draw.rect(screen, (255,255,0), bullet.rect)
    if bullet.y < 0:
        game.player_bullets.remove(bullet)

# Hit invaders
for inv in game.invaders[:]:
    if bullet.rect.colliderect(inv.rect):
        inv.health -= 1
        game.player_bullets.remove(bullet)
        if inv.health <= 0:
            game.score += inv.point_value
game.invaders.remove(inv)
break
if player.cooldown_counter > 0:
     player.cooldown_counter -= 1



