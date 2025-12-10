from game_assets import Invader, Defender, INVADER_TYPES, bg_img, invader_killed, player_img, player_loose_life, invader_shoot_sound #loads in ALL classes and methods from game_assets file and makes them accessible from main.py
import pygame
import sys
import time

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
        self.high_score = self.load_high_score()

#-----------------------The in game screens---------------------------------------
    
    def start_screen(self):

        font = pygame.font.Font(None, 30)
        header = pygame.font.Font(None, 50)
        text = header.render("Space Invaders", True, (255, 255, 255))
        start_text = font.render("Press SPACE to start", True, (255, 255, 255))
        high_score_text = font.render(f"HIGH SCORE: {self.high_score}", True, (255, 255, 255))
        running = True
        while running:
            for event in pygame.event.get():
                if event.type == pygame.QUIT:
                    pygame.quit()
                    sys.exit()
                if event.type == pygame.KEYDOWN and event.key == pygame.K_SPACE:
                    running = False
            self.screen.blit(bg_img, (0, 0))
            self.screen.blit(text, (130, 100))
            self.screen.blit(start_text, (150, 200))
            self.screen.blit(high_score_text, (170, 350))
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
        
        #Storing file data for high score on local device
    def save_high_score(self):

        try:
            with open("highscore.txt", "w") as file: #opens file in write mode
                file.write(str(self.high_score))#writes high score to file (only if called & score is higher than previous writing)
        except Exception as e:
            print(f"Error saving high score: {e}") #excpetion handling if file cannot be written to

    def load_high_score(self):

        try:
            with open("highscore.txt", "r") as f: #opens file in read mode
                return int(f.read()) # returns score as intiger to be displayed
        except:
            return 0  

    def end_screen(self): #onnly called when player looses all lives or invaders reach bottom
        
        font = pygame.font.Font(None, 48)
        text = font.render("Game Over", True, (255, 0, 0))
        score_text = font.render(f"Final Score: {self.score}", True, (255, 255, 255))

        if self.score > self.high_score:
            self.high_score = self.score
            self.save_high_score()

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

    def pause_menu(self): #small feature added, has no real need but adds to user experience

        font = pygame.font.Font(None, 72)
        small_font = pygame.font.Font(None, 36)
        pygame.event.clear()

        paused = True
        while paused:
            for event in pygame.event.get():
                if event.type == pygame.QUIT: #quites if windows closed
                    pygame.quit()
                    sys.exit()

                if event.type == pygame.KEYDOWN:
                    if event.key == pygame.K_p: #paused state toggled off if P pressed again
                        paused = False    

            self.screen.blit(bg_img, (0, 0))
            pause_text = font.render("PAUSED", True, (255, 255, 255))
            info_text = small_font.render("Press P to continue", True, (255, 255, 255))
            self.screen.blit(pause_text,  (140, 200))
            self.screen.blit(info_text,   (120, 300))
            pygame.display.flip() 
            pygame.time.delay(20)

    def draw_invaders(self): #main function for invader blitting and setting up invader array
        
        self.invaders.clear()
        config = self.get_level_config() #gets the level dictionary set as variable 'config'
        rows = config["rows"]
        #starting positions for invader array:
        COLS = 8
        START_X = 60
        SPACING_X = 45
        START_Y = 40
        SPACING_Y = 35
        max_row = 8

        for row in range(min(rows,max_row)): #iterates by row
            for col in range(COLS):
                x = START_X + col * SPACING_X # spaces out each invader by constants
                y = START_Y + row * SPACING_Y
                #setting invader types based on row number
                #stronger invaders ni higher rows push down
                strong_rows = min(1 + self.level // 3, 8)
                mid_rows = min(strong_rows + 2, 8)
                weak_rows = min(mid_rows + 2, 8)
# row selection for invader type
                if row < strong_rows:
                    inv_type = "invader"
                elif row < mid_rows:
                    inv_type = "squid"
                elif row < weak_rows:
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

    def get_level_config(self): # configures invader attributes based on level

        level = self.level 
        config = {}
        config["speed"] = 0.5 + (level * 0.00005)
        config["enemy_fire_rate"] = 0.001 + (level * 0.0003)   
        config["rows"] = min(5 + level // 2, 10)
        return config

    def draw(self): # draws the background and score/lives/level display

        self.screen.blit(bg_img, (0, 0))
        self.score_level_display(self.screen)
        
    def check_if_shot_invader(self): #checks if invader has been hit by bullet

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

    def load_next_level(self):# loading next level with all invaders destroyed

        if len(game.invaders) == 0:
            game.level += 1
            game.level_up_screen()
            game.draw_invaders()

    def check_invaders_reach_player(self):

        for inv in self.invaders:
            if inv.y + inv.h >= self.player.y: #if player y reached:
                self.end_screen()
                return True
        return False
    
    def invader_shooting_update(self): #invader shooting check
        for inv in game.invaders:
            bullet = inv.shoot()
            if bullet:
                #bullet is added to enemy bullet list and shot sound plays
                game.enemy_bullets.append(bullet) 
                invader_shoot_sound.play()

    def check_player_hit_by_bullet(self):

        for bullet in game.enemy_bullets:  
            if bullet.rect.colliderect(pygame.Rect(self.player.x, self.player.y, self.player.l, self.player.h)): 
                self.enemy_bullets.remove(bullet)
                self.player.lives -= 1
                player_loose_life.play()

                if self.player.lives <= 0:
                    self.end_screen()
                    running = False

#---------------------------the game loop-----------------------

game = Game() #create game instance
game.start_screen()
game.draw_invaders()

player_width = 40
player_height = 40
count = 20

game.player = Defender( #Create player object
    x=game.SCREEN_WIDTH // 2 - player_width // 2,
    y=game.SCREEN_HEIGHT - player_height - 20,
    img=player_img,
    l=player_width,
    h=player_height,
    cooldown=count - game.level //5) # decrease cooldown as level increases - making shooting faster and levels easier to pass

try:
    running = True
    while running:
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                running = False
                pygame.quit()
                sys.exit() 

            if event.type == pygame.KEYDOWN:
                if event.key == pygame.K_p:
                    game.pause_menu()

# mass code for main game loop calling all game methods
        game.player.movement(game.SCREEN_WIDTH, game.player_bullets)
        game.screen.blit(bg_img, (0, 0))   
        game.screen.blit(game.player.img, (game.player.x, game.player.y)) 
        game.invader_movement()  
        game.update_enemy_bullets()  
        game.update_bullets()    
        game.check_if_shot_invader() 
        game.load_next_level()
        game.score_level_display(game.screen)
        game.invader_shooting_update()
        if game.check_invaders_reach_player():
            running = False
        if game.check_player_hit_by_bullet():
            running = False

        pygame.display.flip()
        game.clock.tick(game.FPS)
        
#---------------------------end of main game loop------------------------

except Exception as e:
    print(f"An error occurred: {e}")