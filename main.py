from game_assets import Invader, Defender, INVADER_TYPES, bg_img, invader_killed, player_img, player_loose_life, invader_shoot_sound 
import pygame
import sys
import time

# initialise pygame modules
pygame.init()
#All game screen 
class ScreenManager:
    def __init__(self, game):

        self.game = game
        self.screen = game.screen
        self.high_score = game.high_score

    def start_screen(self):

        font = pygame.font.Font(None,30)
        header = pygame.font.Font(None,50)
        text = header.render("Space Invaders", True, (255,255,255))
        start_text = font.render("Press SPACE to start", True, (255,255,255))
        high_score_text = font.render(f"HIGH SCORE: {self.high_score}", True, (255,255,255))

        running = True
        while running:
            for event in pygame.event.get():
                if event.type == pygame.QUIT:#runs loop until key pressed
                    pygame.quit()
                    sys.exit()
                if event.type == pygame.KEYDOWN and event.key == pygame.K_SPACE:
                    running =False

            self.screen.blit(bg_img, (0,0))
            self.screen.blit(text, (130,100))
            self.screen.blit(start_text, (150,200))
            self.screen.blit(high_score_text, (170,350))
            pygame.display.flip()

    def level_up_screen(self):

        font = pygame.font.Font(None, 48)
        text = font.render(f"Level {self.game.level} Complete!", True, (255,255,255))
        score_text = font.render(f"score: {self.game.score}", True, (255,255,255))
        start_text = font.render("Press SPACE to start level", True, (255,255,255))

        running = True
        while running:           #runs loop until key pressed
            for event in pygame.event.get():
                if event.type == pygame.QUIT:
                    pygame.quit()
                    sys.exit()
                if event.type == pygame.KEYDOWN and event.key == pygame.K_SPACE:
                    running = False

            self.screen.blit(bg_img, (0, 0))
            self.screen.blit(text, (200,150))
            self.screen.blit(score_text, (180,250))
            self.screen.blit(start_text, (50,350))
            pygame.display.flip()

    def end_screen(self):  #onnly called when player looses all lives or invaders reach bottom

        font = pygame.font.Font(None,48)
        text = font.render("Game Over", True, (255, 0,0))
        score_text = font.render(f"Final Score: {self.game.score}", True, (255,255,255))

        if self.game.score > self.game.high_score:
            self.game.high_score = self.game.score
            self.game.save_high_score()

        running= True
        while running:
            for event in pygame.event.get():
                if event.type == pygame.QUIT:
                    pygame.quit()
                    sys.exit()
            self.screen.blit(bg_img, (0,0))
            self.screen.blit(text, (150,100))
            self.screen.blit(score_text, (130,200))
            pygame.display.flip()

    def pause_menu(self):#small feature added, has no real need but adds to user experience

        font = pygame.font.Font(None, 72)
        small_font = pygame.font.Font(None, 36)

        pygame.event.clear()
        paused = True

        while paused:
            for event in pygame.event.get():
                if event.type == pygame.QUIT: 
                    pygame.quit()
                    sys.exit()

                if event.type == pygame.KEYDOWN:
                    if event.key == pygame.K_p: #paused state toggled off if P pressed again
                        paused = False

            self.screen.blit(bg_img, (0,0))
            pause_text = font.render("PAUSED", True, (255,255,255))
            info_text = small_font.render("Press P to continue", True, (255,255, 255))
            self.screen.blit(pause_text,  (140,200))
            self.screen.blit(info_text,   (120,300))
            pygame.display.flip( )
            pygame.time.delay(20)

class InvaderManager:
    def __init__(self, game):
        self.game = game
        self.invaders = game.invaders  #  uses same list so nothing breaks

    def draw_invaders(self):#main function for invader blitting and setting up invader array

        self.invaders.clear()
        config = self.game.get_level_config() #gets the level dictionary set as variable 'config'
        rows = config["rows"]

        #starting positions for invader array:
        COLS=8
        START_X=60
        SPACING_X=45
        START_Y=40
        SPACING_Y=35
        max_row=8

        for row in range(min(rows,max_row)): #iterates by row
            for col in range(COLS):

                x = START_X + col * SPACING_X # spaces out each invader by constants
                y = START_Y + row * SPACING_Y #

            # invader type determination based on row and level
                strong_rows = min(1 + self.game.level // 3, 8)
                mid_rows = min(strong_rows + 2, 8)
                weak_rows = min(mid_rows + 2, 8)

                 # row selection for invader type
                if row < strong_rows:
                    inv_type = "invader"
                elif row < mid_rows:
                    inv_type = "squid"
                else:
                    inv_type = "alien"

                types = INVADER_TYPES[inv_type]

                inv = Invader(
                    x, y,
                    types["img"],
                    l=40, h=40,
                    health=types["health"],
                    bullet_speed=types["bullet_speed"] + self.game.level,
                    point_value=types["points"],
                    fire_rate=types["fire_rate"] + (self.game.level * 0.00002)
                )

                inv.speed = 1 + self.game.level * 0.01
                self.invaders.append(inv)

    def move_invaders(self):

        hit_wall = False #while invader hasnt hit the wall

        for inv in self.invaders:
            inv.move()
            self.game.screen.blit(inv.img, (inv.x, inv.y))

            next_x = inv.x + inv.speed * inv.direction # this is the next x position

            if next_x <= 0 or next_x + inv.l >= self.game.SCREEN_WIDTH: # checks if invaders are on either end of screen side
                hit_wall = True

        if hit_wall:
            for inv in self.invaders:
                inv.direction *= -1 # multiplies the direction by -1 to reverse direction
                inv.y += 10 # 10px down if wall is hit

    def invader_shooting_update(self): #invader shooting check

        for inv in self.invaders:
            bullet = inv.shoot()
            if bullet:
                self.game.enemy_bullets.append(bullet)
                invader_shoot_sound.play()

    def check_if_shot_invader(self):  #checks if invader has been hit by bullet

        for bullet in self.game.player_bullets:
            for inv in self.invaders:
                if bullet.rect.colliderect(pygame.Rect(inv.x, inv.y, inv.l, inv.h)):

                    if inv.take_damage(): # only if invader health is 0
                        self.game.score += inv.point_value
                        invader_killed.play()
                        self.invaders.remove(inv)

                        for inv in self.invaders:#increase invader speed
                            inv.speed+=0.05

                    if bullet in self.game.player_bullets:
                        self.game.player_bullets.remove(bullet)
                        break

    def check_invaders_reach_player(self):

        for inv in self.invaders:
            if inv.y + inv.h >= self.game.player.y: #if player y reached:
                self.game.screens.end_screen()
                return True
        return False
#Game class for main game attributes and methods
class Game:
    def __init__(self):

        # all game attributes
        self.level=1
        self.score=0
        self.invaders = [] # main invader lists
        self.enemy_bullets = []
        self.player_bullets = []
        self.font = pygame.font.Font(None,32)
        self.FPS=60
        self.clock = pygame.time.Clock()
        self.SCREEN_HEIGHT=500
        self.SCREEN_WIDTH=500
        self.screen = pygame.display.set_mode([self.SCREEN_WIDTH, self.SCREEN_HEIGHT])
        self.high_score = self.load_high_score()
        self.player_width=40
        self.player_height=40

        # instantiating defender object in game class
        self.player = Defender(
            x=self.SCREEN_WIDTH // 2 - self.player_width // 2,
            y=self.SCREEN_HEIGHT - self.player_height - 20,
            img=player_img,
            l=self.player_width,
            h=self.player_height,
            cooldown=20 - self.level //5
        )

        self.screens = ScreenManager(self)
        self.invader_manager = InvaderManager(self)
        
    def save_high_score(self):
        try:
            with open("highscore.txt", "w") as file: #opens file in write mode
                file.write(str(self.high_score))#writes high score to file (only if called & score is higher than previous writing)
        except Exception as e:
            print(f"Error saving high score: {e}") #excpetion handling if file cannot be written to

    def load_high_score(self):

        try:
            with open("highscore.txt", "r") as f: #opens  file in read mode
                return int(f.read()) # returns score as intiger to be displayed
        except:
            return 0

    
    def get_level_config(self): # configures invader attributes based on level

        level = self.level
        config = {}
        config["speed"] = 0.5 + (level * 0.00005) #speed increase
        config["enemy_fire_rate"] = 0.001 + (level * 0.0003)
        config["rows"] = min(5 + level // 2, 10)
        return config

    def score_level_display(self, screen):

          #blitting all the score, level and lives text onto the screen
        score_text = self.font.render(f"Score: {self.score}", True, (255,255,255))
        level_text = self.font.render(f"Level: {self.level}", True, (255,255,255))
        lives_text = self.font.render(f"Lives: {self.player.lives}", True, (255,255,255))

        screen.blit(score_text, (10, 10))
        screen.blit(level_text, (self.SCREEN_WIDTH -level_text.get_width() - 10,10))
        screen.blit(lives_text, (self.SCREEN_WIDTH//2 - lives_text.get_width()//2, 10))

    def update_enemy_bullets(self):

        for bullet in self.enemy_bullets[:]:
            bullet.update()
            pygame.draw.rect(self.screen, (0, 255, 0), bullet.rect) # draws enemy bullet in green
            if bullet.y > self.SCREEN_HEIGHT: # removes bullet if wall is hit
                self.enemy_bullets.remove(bullet)

    def update_bullets(self):

        for bullet in self.player_bullets[:]:
            bullet.update()
            pygame.draw.rect(self.screen, (255,255,0), bullet.rect)
            if bullet.y < 0:
                self.player_bullets.remove(bullet)

    def load_next_level(self):# loading next level with all invaders destroyed

        if len(self.invaders) == 0:
            self.level += 1
            self.screens.level_up_screen()
            self.invader_manager.draw_invaders()

    def check_player_hit_by_bullet(self):

        for bullet in self.enemy_bullets:
            if bullet.rect.colliderect(pygame.Rect(self.player.x, self.player.y, self.player.l, self.player.h)):
                self.enemy_bullets.remove(bullet)
                self.player.lives -= 1
                player_loose_life.play()

                if self.player.lives <= 0:
                    self.screens.end_screen()
                    return True

        return False

game = Game() #create game object
game.screens.start_screen()
game.invader_manager.draw_invaders()

try:
    running=True
    while running:
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                running=False
                pygame.quit()
                sys.exit()

            if event.type == pygame.KEYDOWN:
                if event.key == pygame.K_p:
                    game.screens.pause_menu()

        game.player.movement(game.SCREEN_WIDTH, game.player_bullets)
        game.screen.blit(bg_img, (0,0))    
        game.screen.blit(game.player.img, (game.player.x,game.player.y))
        game.invader_manager.move_invaders()
        game.update_enemy_bullets()
        game.update_bullets()
        game.invader_manager.check_if_shot_invader()
        game.load_next_level()
        game.score_level_display(game.screen)
        game.invader_manager.invader_shooting_update()
        if game.invader_manager.check_invaders_reach_player():
            running=False
        if game.check_player_hit_by_bullet():
            running=False

        pygame.display.flip()
        game.clock.tick(game.FPS)

except Exception as e: #error if problem with game code
    print(f"An error occurred: {e}")
