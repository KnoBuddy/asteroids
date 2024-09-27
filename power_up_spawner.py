import pygame
import random

from power_up import *
from constants import *

class PowerUpSpawner(pygame.sprite.Sprite):
        edge = [
            [
                pygame.Vector2(1, 0),
                lambda y: pygame.Vector2(random.randint(POWER_UP_RADIUS*10, (SCREEN_WIDTH - POWER_UP_RADIUS*10)), y * random.randint(POWER_UP_RADIUS*10, (SCREEN_HEIGHT - POWER_UP_RADIUS*10))),
            ],
        ]

        def __init__(self):
            pygame.sprite.Sprite.__init__(self, self.containers)
            self.spawn_timer = 0.0
            self.id = 0

        def spawn(self, radius, position, direction):
            if self.id < 2:
                powerup = PowerUp(position.x, position.y, radius, direction)
                self.id += 1

        def update(self, dt):
            self.spawn_timer += dt
            if self.spawn_timer > POWER_UP_SPAWN_MAX:
                self.spawn_timer = 0

                # spawn a new powerup at a random point
                position = pygame.Vector2(random.randint(POWER_UP_RADIUS, (SCREEN_WIDTH - POWER_UP_RADIUS)), random.randint(POWER_UP_RADIUS, (SCREEN_HEIGHT - POWER_UP_RADIUS)))
                angle = random.randrange(0, 360, 1)
                new_angle = random.choice([-1, 1]) * angle
                self.spawn(POWER_UP_RADIUS, position, new_angle)
                