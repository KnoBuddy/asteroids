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
        # Dictionary mapping asteroid types to image file paths
        asteroid_images = {
            1: "./images/asteroid1.png",
            2: "./images/asteroid2.png",
            3: "./images/asteroid3.png"
        }

        # Dictionary mapping radius to the scaling factor
        scale_factors = {
            60: 1.0,   # No scaling for radius 60
            40: 0.66,  # Scaling by 0.66 for radius 40
            20: 0.33   # Scaling by 0.33 for radius 20
        }

        # Check if the asteroid_type is valid
        if asteroid_type in asteroid_images and radius in scale_factors:
            # Load the appropriate asteroid image
            self.asteroid_img = pygame.image.load(asteroid_images[asteroid_type])
            
            # Apply scaling if necessary
            if scale_factors[radius] != 1.0:
                self.asteroid_img = pygame.transform.smoothscale_by(self.asteroid_img, scale_factors[radius])
            
            # Get the rectangle for the asteroid image
            self.asteroid_rect = self.asteroid_img.get_rect()


    def draw(self, screen):
        self.asteroid_rect = self.position
        rotated_asteroid_img = pygame.transform.rotate(self.asteroid_img, self.angle)
        new_asteroid_rect = rotated_asteroid_img.get_rect(center = self.asteroid_img.get_rect(center = self.position).center)
        screen.blit(rotated_asteroid_img, new_asteroid_rect)
        
    
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
        