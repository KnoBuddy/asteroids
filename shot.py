import pygame
from circleshape import *
from constants import *
from player import *

class Shot(CircleShape):
    def __init__(self, x, y):
        super().__init__(x, y, radius=SHOT_RADIUS)
        self.shot_img = pygame.image.load("./images/shot.png")

    def draw(self, screen):
        self.shot_rect = self.shot_img.get_rect(center=self.position)
        screen.blit(self.shot_img, self.shot_rect)
    
    def update(self, dt):
        self.position += self.velocity * dt

    def fix_pos(self):
        self.position 
        