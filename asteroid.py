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
        self.collision_cooldown = 0
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

        # Dictionary mapping of asteroid radius to mass
        mass = {
            60: 500, 
            40: 300,
            20: 100
        }

        # Check if the asteroid_type is valid
        if asteroid_type in asteroid_images and radius in scale_factors and radius in mass:
            # Load the appropriate asteroid image
            self.asteroid_img = pygame.image.load(asteroid_images[asteroid_type])
            
            # Apply scaling if necessary
            if scale_factors[radius] != 1.0:
                self.asteroid_img = pygame.transform.smoothscale_by(self.asteroid_img, scale_factors[radius])
            
            # Get the rectangle for the asteroid image
            self.asteroid_rect = self.asteroid_img.get_rect()
            
            # Apply Mass
            self.mass = mass[radius]

    def draw(self, screen):
        self.asteroid_rect = self.position
        rotated_asteroid_img = pygame.transform.rotate(self.asteroid_img, self.angle)
        if self.position.x > 22147483647:
            self.position.x = 2147483647
        if self.position.x < -2147483647:
            self.position.x = -2147483647
        if self.position.y > 2147483647:
            self.position.y = 2147483647
        if self.position.y < -2147483647:
            self.position.y = -2147483647
            
        new_asteroid_rect = rotated_asteroid_img.get_rect(center = self.asteroid_img.get_rect(center = self.position).center)
        screen.blit(rotated_asteroid_img, new_asteroid_rect)
        
    def update(self, dt):
        if self.collision_cooldown > 0:
            self.collision_cooldown -= dt
        if self.collision_cooldown < 0:
            self.collision_cooldown = 0
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
    
    def collides_with_asteroid(self, other):
        return self.position.distance_to(other.position) <= self.radius + other.radius
    
    def elastic_collision(self, other, dt, bounciness, impulse_amp):
        # Resolve Overlapping Issues
        self.resolve_overlap(other)

        if self.collision_cooldown > 0 or other.collision_cooldown > 0:
            return

        # Calculate the displacement vector between A and B
        dX = other.position.x - self.position.x
        dY = other.position.y - self.position.y

        # Calculate the distance between the two objects
        distance = math.sqrt(dX**2 + dY**2)

        # Prevent division by zero
        if distance == 0:
            distance = 0.001
            delta = pygame.Vector2(1, 0)

        # Normalize the displacement vector
        nX = dX / distance
        nY = dY / distance

        # Calculate the relative velocity in the direction of the displacement
        vRelativeX = other.velocity.x - self.velocity.x
        vRelativeY = other.velocity.y - self.velocity.y

        # Calculate the velocity along the normal (collision axis)
        vRelDotN = vRelativeX * nX + vRelativeY * nY

        # Early exit if velocities are seperating (no collision)
        if vRelDotN > 0:
            return False # No collision as they are moving away from each other
        
        # Calculate impulse scalar with restitution (bounciness factor)
        impulse = (-(1 + bounciness)* vRelDotN) / (self.mass + other.mass)

        # Increase inpulse atrificially for more bounce
        impulse *= impulse_amp

        # Update velocities based on impule and the collision normal
        newselfvelocityX = self.velocity.x + impulse * other.mass * nX
        newselfvelocityY = self.velocity.y + impulse * other.mass * nY
        newothervelocityX = other.velocity.x + impulse * self.mass * nX
        newothervelocityY = other.velocity.y + impulse * self.mass * nY

        self.velocity.x = newselfvelocityX
        self.velocity.y = newselfvelocityY
        other.velocity.x = newothervelocityX
        other.velocity.y = newothervelocityY

        self.position += self.velocity * dt
        other.position += other.velocity * dt

        self.collision_cooldown = 1
        other.collision_cooldown = 1

    def resolve_overlap(self, other):
            # Calculate the displacement between the objects
        delta = other.position - self.position
        distance = delta.length()  # Calculate the actual distance
        
        if distance == 0:
            # Special case: objects are at the exact same position
            # Move them apart slightly
            distance = 0.001
            delta = pygame.Vector2(1, 0)  # Arbitrary unit vector
        
        # Calculate the overlap amount
        overlap = self.radius + other.radius - distance
        
        # Move each object half the overlap distance away from each other
        displacement = delta.normalize() * (overlap / 2)
        
        self.position -= displacement
        other.position += displacement