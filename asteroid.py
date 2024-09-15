import pygame
import random
from circleshape import *
from constants import *

class Asteroid(CircleShape):
    def __init__(self, x, y, radius, asteroid_type, direction):
        super().__init__(x, y, radius)
        self.rotation = 0
        self.angle = direction
        self.timer = self.angle/100
        if radius == 60:
            if asteroid_type == 1:
                self.asteroid_img = pygame.image.load("./images/asteroid1.png")
                self.asteroid_rect = self.asteroid_img.get_rect()
            elif asteroid_type == 2:
                self.asteroid_img = pygame.image.load("./images/asteroid2.png")
                self.asteroid_rect = self.asteroid_img.get_rect()
            else:
                self.asteroid_img = pygame.image.load("./images/asteroid3.png")
                self.asteroid_rect = self.asteroid_img.get_rect()
        if radius == 40:
            if asteroid_type == 1:
                self.asteroid_img = pygame.image.load("./images/asteroid1.png")
                self.asteroid_img = pygame.transform.smoothscale_by(self.asteroid_img, 0.66)
                self.asteroid_rect = self.asteroid_img.get_rect()
            elif asteroid_type == 2:
                self.asteroid_img = pygame.image.load("./images/asteroid2.png")
                self.asteroid_img = pygame.transform.smoothscale_by(self.asteroid_img, 0.66)
                self.asteroid_rect = self.asteroid_img.get_rect()
            else:
                self.asteroid_img = pygame.image.load("./images/asteroid3.png")
                self.asteroid_img = pygame.transform.smoothscale_by(self.asteroid_img, 0.66) 
                self.asteroid_rect = self.asteroid_img.get_rect()
        if radius == 20:
            if asteroid_type == 1:
                self.asteroid_img = pygame.image.load("./images/asteroid1.png")
                self.asteroid_img = pygame.transform.smoothscale_by(self.asteroid_img, 0.33) 
                self.asteroid_rect = self.asteroid_img.get_rect()
            elif asteroid_type == 2:
                self.asteroid_img = pygame.image.load("./images/asteroid2.png")
                self.asteroid_img = pygame.transform.smoothscale_by(self.asteroid_img, 0.33)
                self.asteroid_rect = self.asteroid_img.get_rect()
            else:
                self.asteroid_img = pygame.image.load("./images/asteroid3.png")
                self.asteroid_img = pygame.transform.smoothscale_by(self.asteroid_img, 0.33)
                self.asteroid_rect = self.asteroid_img.get_rect()


    def draw(self, screen):
        self.asteroid_rect = self.position
        rotated_asteroid_img = pygame.transform.rotate(self.asteroid_img, self.angle)
        new_asteroid_rect = rotated_asteroid_img.get_rect(center = self.asteroid_img.get_rect(center = self.position).center)
        screen.blit(rotated_asteroid_img, new_asteroid_rect)
        
    
    def update(self, dt):
        self.position += self.velocity * dt
        if self.timer > 0:
            self.timer -= dt
            if self.timer >= 3.6:
                self.timer = 0.001
        else:
            self.timer += dt
            if self.timer <= 0:
                self.timer = 3.6

        self.rotate()

    def rotate(self):
        self.angle = self.timer * 100
    
    def split(self):
        self.kill()
        if self.radius <= ASTEROID_MIN_RADIUS:
            return
        angle = random.uniform(20, 50)
        v1 = self.velocity.rotate(angle)
        v2 = self.velocity.rotate(-angle)
        new_radius = self.radius - ASTEROID_MIN_RADIUS
        angle = random.randrange(0, 360, 1)
        new_angle = random.choice([-1, 1]) * angle
        asteroid_type = random.randrange(1, 3, 1)
        asteroid1 = Asteroid(self.position.x, self.position.y, new_radius, asteroid_type, new_angle)
        asteroid2 = Asteroid(self.position.x, self.position.y, new_radius, asteroid_type, new_angle)
        asteroid1.velocity = v1 * 1.2
        asteroid2.velocity = -v2 * 1.2
        