from game_assets import Invader
import pygame
import os

image_path = os.path.join("Media", "invader.png") #load image path
invader_img = pygame.image.load(image_path)

class TestInvader:
    def test_take_damage(self): #test function
# tests if invader will die after loosing 3 lives
        invader = Invader(0, 0, invader_img, 50, 50, health=3, bullet_speed=5, point_value=100, fire_rate=0.1)
        assert invader.take_damage() == False  
        assert invader.health == 2
        assert invader.take_damage() == False  
        assert invader.health == 1
        assert invader.take_damage() == True   
        assert invader.health == 0
