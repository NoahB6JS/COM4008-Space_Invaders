import pygame
from Game import Game

pygame.init()
pygame.mixer.init()

screen = pygame.display.set_mode((500, 500))

images = {
    "player": pygame.image.load("Media/player.png"),
    "invader": pygame.image.load("Media/invader.png"),
    "alien": pygame.image.load("Media/alien.png"),
    "squid": pygame.image.load("Media/squid.png"),
    "ufo": pygame.image.load("Media/ufo.png"),
}

bg_img = pygame.image.load("Media/bg.jpg")

sounds = {
    "shoot": pygame.mixer.Sound("Media/sound/invaderkilled.wav"),
    "soundtrack": pygame.mixer.Sound("Media/sound/soundtrack.wav")
}
pygame.mixer.music.load("Media/sound/soundtrack.wav")
pygame.mixer.music.set_volume(0.3)
pygame.mixer.music.play(-1)

game = Game(screen, images, sounds, bg_img)
game.run()

