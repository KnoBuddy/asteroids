import pygame
import random

from circleshape import *
from constants import *
from asteroidfield import *
from power_up import *

class PowerUpSpawn(AsteroidField):
        edges = [
            [
                pygame.Vector2(1, 0),
                lambda y: pygame.Vector2(random.randint(POWER_UP_RADIUS, (SCREEN_HEIGHT - POWER_UP_RADIUS)), y * (random.randint(SCREEN_HEIGHT - POWER_UP_RADIUS), POWER_UP_RADIUS)),
            ],
            [
                pygame.Vector2(0, 1),
                lambda x: pygame.Vector2(x * random.randint((SCREEN_WIDTH - POWER_UP_RADIUS), POWER_UP_RADIUS), random.randint(POWER_UP_RADIUS, (SCREEN_WIDTH - POWER_UP_RADIUS))),
            ],
        ]

        def __init__(self):
            pygame.sprite.Sprite.__init__(self, self.containers)
            self.spawn_timer = 0.0

        def spawn(self, radius, position, velocity, powerup_type, direction):
            powerup = PowerUp(position.x, position.y, radius, direction)
            powerup.velocity = 0 #velocity

        def update(self, dt):
            self.spawn_timer += dt
            if self.spawn_timer > POWER_UP_SPAWN_MAX:
                self.spawn_timer = 0

                # spawn a new powerup at a random edge
                edge = random.choice(self.edges)
                speed = random.randint(40, 100)
                velocity = edge[0] * speed
                velocity = velocity.rotate(random.randint(-30, 30))
                position = edge[1](random.uniform(0, 1))
                angle = random.randrange(0, 360, 1)
                new_angle = random.choice([-1, 1]) * angle
                powerup_type = random.randrange(1, 3, 1)
                self.spawn(POWER_UP_RADIUS, position, velocity, powerup_type, new_angle)
                