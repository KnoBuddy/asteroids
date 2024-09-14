# Current Game:
# Player moves with WASD
# Asteroids spawn and move randomly
# Player can shoot asteroids
# Bigger asteroids split when shot, and small ones are destroyed

# Additions wanted in priority from top to bottom:
# Player rotation follow mouse instead of WASD
# Crosshair follows mouse
# Collisions between asteroids and semi accurate physics bounce
# Fix bullets to spawn at tip of ship, not from center
# Add score, menu screen, game loop
# Add power ups that change gun type or increase rate of fire
# Levels with different speeds and types of asteroids
# Color different types of asteroids.

import pygame
import sys
import os
from circleshape import *
from constants import *
from player import *
from asteroid import *
from asteroidfield import *
from shot import *

cwd = "/home/kyle/workspace/github.com/knobuddy/asteroids/"
os.chdir(cwd)

def main():
    print("Starting asteroids!")
    print(f"Screen width: {SCREEN_WIDTH}")
    print(f"Screen height: {SCREEN_HEIGHT}")

    pygame.init()
    screen = pygame.display.set_mode((SCREEN_WIDTH, SCREEN_HEIGHT))
    time = pygame.time.Clock()
    dt = 0

    updateable = pygame.sprite.Group()
    drawable = pygame.sprite.Group()
    asteroids = pygame.sprite.Group()
    shots = pygame.sprite.Group()

    Asteroid.containers = (asteroids, updateable, drawable)
    AsteroidField.containers = (updateable)
    asteroidfield = AsteroidField()

    Player.containers = (updateable, drawable)
    player = Player(SCREEN_WIDTH/2, SCREEN_HEIGHT/2)

    Shot.containers = (shots, updateable, drawable)

    pygame.mouse.set_visible(False)
    crosshair_img = pygame.image.load("crosshair.png")
    crosshair_rect = crosshair_img.get_rect()

    while True:
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                return
            
        for object in updateable:
            object.update(dt)
        
        screen.fill("black")
            
        for object in drawable:
            object.draw(screen)

        for asteroid in asteroids:
            if asteroid.collides_with(player):
                print("Game Over")
                sys.exit()
            for shot in shots:
                if asteroid.collides_with(shot):
                    asteroid.split()
                    shot.kill()
        
        crosshair_rect.center = pygame.mouse.get_pos()
        screen.blit(crosshair_img, crosshair_rect)

        pygame.display.flip()

        dt = (time.tick(60))/1000

if __name__ == "__main__":
    main()