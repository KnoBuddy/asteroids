import pygame

from circleshape import *
from constants import *

class PowerUp(CircleShape):

    _counter = 0

    def __init__(self, x, y, radius, direction):
        super().__init__(x, y, radius)
        PowerUp._counter += 1
        self.id = PowerUp._counter
        self.rotation = 0
        self.angle = direction
        self.timer = self.angle/100
        self.powerup_img_path = "./images/power_up.png"
        self.powerup_img = pygame.image.load(self.powerup_img_path)
        self.powerup_img = pygame.transform.smoothscale_by(self.powerup_img, 0.50)
        self.powerup_rect = self.powerup_img.get_rect()


    def draw(self, screen):
        self.powerup_rect = self.position
        rotated_powerup_img = pygame.transform.rotate(self.powerup_img, self.angle)
        new_powerup_rect = rotated_powerup_img.get_rect(center = self.powerup_img.get_rect(center = self.position).center)
        screen.blit(rotated_powerup_img, new_powerup_rect)

    def update(self, dt):
        self.position += self.velocity * dt
        if self.timer == 0:
            self.timer -= dt
            if self.timer >= 3.6:
                self.timer = 0
        else:
            self.timer += dt
            if self.timer <= 0.001:
                self.timer = 3.6
        self.timer %= 3.6

        self.rotate()

    def rotate(self):
        self.angle = self.timer * 100