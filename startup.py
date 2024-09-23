import pygame

from player import *
from shot import *
from asteroid import *
from asteroidfield import *
from power_up import *
from menu import *

class Startup():
    def __init__(self):
        self.time = pygame.time.Clock()
        self.dt = 0

        self.updateable = pygame.sprite.Group()
        self.drawable = pygame.sprite.Group()
        self.asteroids = pygame.sprite.Group()
        self.shots = pygame.sprite.Group()
        self.powerup = pygame.sprite.Group()

        Asteroid.containers = (self.asteroids, self.updateable, self.drawable)
        AsteroidField.containers = (self.updateable)
        self.asteroidfield = AsteroidField()

        Player.containers = (self.updateable, self.drawable)
        self.player = Player(SCREEN_WIDTH/2, SCREEN_HEIGHT/2)

        Shot.containers = (self.shots, self.updateable, self.drawable)
        PowerUp.containers = (self.powerup, self.updateable, self.drawable)

        pygame.mouse.set_visible(False)
        self.crosshair_img = pygame.image.load("./images/crosshair2.png")
        self.crosshair_rect = self.crosshair_img.get_rect()
            