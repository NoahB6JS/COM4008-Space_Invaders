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

    def level_up_screen(self):
        font = pygame.font.Font(None, 48)
        text = font.render(f"Level {self.level} Complete!", True, (255, 255, 255))
        score_text = font.render(f"score: {self.score}", True, (255, 255, 255))
        start_text = font.render("Press SPACE to start level", True, (255, 255, 255))
        running = True
        while running:
            for event in pygame.event.get():
                if event.type == pygame.QUIT:
                    pygame.quit()
                    sys.exit()
                if event.type == pygame.KEYDOWN and event.key == pygame.K_SPACE:
                    running = False
                    
            self.screen.blit(bg_img, (0, 0))
            self.screen.blit(text, (200, 150))
            self.screen.blit(score_text, (180, 250))
            self.screen.blit(start_text, (50, 350))
            pygame.display.flip()
            time.sleep(2)
            running = False

    def end_screen(self):
        
        font = pygame.font.Font(None, 48)
        text = font.render("Game Over", True, (255, 0, 0))
        score_text = font.render(f"Final Score: {self.score}", True, (255, 255, 255))
        running = True
        while running:
            for event in pygame.event.get():
                if event.type == pygame.QUIT:
                    pygame.quit()
                    sys.exit()
            self.screen.blit(bg_img, (0, 0))
            self.screen.blit(text, (150, 100))
            self.screen.blit(score_text, (130, 200))
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
        max_row = 8

        for row in range(min(rows,max_row)):
            for col in range(COLS):
                x = START_X + col * SPACING_X
                y = START_Y + row * SPACING_Y
                if self.level >= 6:
                    if row == 0:
                        inv_type = "invader"  
                    elif row < 3:
                        inv_type = "squid"
                    else:
                        inv_type = "alien"

                elif self.level >= 3:
                    if row == 0:
                        inv_type = "squid"    
                    else:
                        inv_type = "alien"
                else:
                    inv_type = "alien"   

                 #scaling invader difficlty based on level.
                types = INVADER_TYPES[inv_type]
                inv = Invader(#instantiate invader object
                    x, y, #all attributes:
                    types["img"],
                    l=40, h=40,
                    health=types["health"],
                    bullet_speed=types["bullet_speed"] + self.level,
                    point_value=types["points"],
                    fire_rate=types["fire_rate"] + (self.level * 0.00002)
            )
                inv.speed = 1 + self.level * 0.01 #increase speed as invaders are shot
                self.invaders.append(inv) #appending the inv (invader) object and its attributes
            
    # --- Game helpers ---
    def score_level_display(self, screen):
        
        #blitting all the score, level and lives text onto the screen
        score_text = self.font.render(f"Score: {self.score}", True, (255, 255, 255))
        level_text = self.font.render(f"Level: {self.level}", True, (255, 255, 255))
        lives_text = self.font.render(f"Lives: {game.player.lives}", True, (255, 255, 255))
        screen.blit(score_text, (10, 10))
        screen.blit(level_text, (self.SCREEN_WIDTH - level_text.get_width() - 10, 10))
        screen.blit(lives_text, (self.SCREEN_WIDTH//2 - lives_text.get_width()//2, 10))


    def invader_movement(self):
        
        hit_wall = False #while invader hasnt hit the wall
        
        for inv in self.invaders:
            inv.move()
            self.screen.blit(inv.img, (inv.x, inv.y))
            next_x = inv.x + inv.speed * inv.direction # this is the next x position
            if next_x <= 0 or next_x + inv.l >= self.SCREEN_WIDTH: # checks if invaders are on either end of screen side
                hit_wall = True
        if hit_wall:
            for inv in self.invaders:
                inv.direction *= -1 # multiplies the direction by -1 to reverse direction
                inv.y += 10 # 10px down if wall is hit

    def update_enemy_bullets(self):
        for bullet in self.enemy_bullets[:]:
            bullet.update()
            pygame.draw.rect(self.screen, (0, 255, 0), bullet.rect) # draws enemy bullet in green
            if bullet.y > self.SCREEN_HEIGHT: # removes bullet if wall is hit
                self.enemy_bullets.remove(bullet)

    def get_level_config(self): 
        level = self.level 
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
                    
                    if inv.take_damage(): # only if invader health is 0
                        self.score += inv.point_value
                        invader_killed.play()
                        self.invaders.remove(inv) #adding point value for invader when hit and removing the invade
                        
                        for inv in self.invaders:#increase invader speed
                            inv.speed += 0.05

        
                
                    if bullet in self.player_bullets:
                        self.player_bullets.remove(bullet)
                
                        break             
                    
    def update_bullets(self):
        for bullet in game.player_bullets[:]:
            bullet.update()
            pygame.draw.rect(game.screen, (255,255,0), bullet.rect)
            if bullet.y < 0:
                game.player_bullets.remove(bullet)
            
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
    cooldown=20)


#. main game loop
try:
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

       
        game.invader_movement()  

       
        game.update_enemy_bullets()  
        game.update_bullets()
        
       
        game.check_if_shot_invader()  

        
        for inv in game.invaders:
            bullet = inv.shoot()
            if bullet:
                game.enemy_bullets.append(bullet)
                invader_shoot_sound.play()

       
        for bullet in game.enemy_bullets[:]:  # copy the list to avoid modification issues
            if bullet.rect.colliderect(pygame.Rect(game.player.x, game.player.y, game.player.l, game.player.h)): 
                game.enemy_bullets.remove(bullet)
                game.player.lives -= 1
                player_loose_life.play()
                if game.player.lives <= 0:
                    game.end_screen()
                    running = False

        
        for inv in game.invaders:
            if inv.y + inv.h >= game.player.y:
                running = False

       
        if len(game.invaders) == 0:
            game.level += 1
            game.level_up_screen()
            game.draw_invaders()

    
        game.score_level_display(game.screen)
        pygame.display.flip()
        game.clock.tick(game.FPS)

except Exception as e:
    print(f"An error occurred: {e}")