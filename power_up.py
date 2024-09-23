import pygame

from circleshape import *

class PowerUp(CircleShape):

    def __init__(self, x, y, radius, powerup_type, direction):
        super().__init__(x, y, radius)
        self.rotation = 0
        self.angle = direction
        self.timer = 0
        self.powerup_img = "./images/powerup.png"


    def draw(self, screen):
        self.powerup_rect = self.position
        rotated_powerup_img = pygame.transform.rotate(self.powerup_img, self.angle)
        new_powerup_rect = rotated_powerup_img.get_rect(center = self.powerup_img.get_rect(center = self.position))
        screen.blit(rotated_powerup_img, new_powerup_rect)

    def update(self, dt):
        if self.timer == 0:
            self.timer -= dt
        self.rotate(dt)

    def rotate(self, dt):
        self.angle = self.timer * dt