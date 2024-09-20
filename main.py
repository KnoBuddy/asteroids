# Current Game:
# Player moves with WASD --- Done
# Asteroids spawn and move randomly --- Done
# Player can shoot asteroids --- Done
# Bigger asteroids split when shot, and small ones are destroyed --- Done

# Additions wanted in priority from top to bottom:
# Player rotation follow mouse instead of WASD CHECK --- DONE!
# Crosshair follows mouse --- DONE!
# Add sprites instead of basic shapes --- Player and Crosshair DONE!
# Fix movement so that sideways movement is more user friendly
# Collisions between asteroids and semi accurate physics bounce
# Fix bullets to spawn at tip of ship, not from center --- Half DONE!
# Implement multiple lives and respawning
# Add score, menu screen, game loop -- DONE
# Add power ups that change gun type or increase rate of fire
# Levels with different speeds and types of asteroids
# Color different types of asteroids.

import pygame
import sys
import os

from startup import *
from menu import *
from game_over import *
from score import *
from circleshape import *
from constants import *
from player import *
from asteroid import *
from asteroidfield import *
from shot import *

cwd = "/home/kyle/workspace/github.com/knobuddy/asteroids/"
os.chdir(cwd)

print("Starting asteroids!")
print(f"Screen width: {SCREEN_WIDTH}")
print(f"Screen height: {SCREEN_HEIGHT}")

pygame.init()

screen = pygame.display.set_mode((SCREEN_WIDTH, SCREEN_HEIGHT))



def run_game():
    running = True
    menu = Menu(screen)
    startup = Startup()
    score = Score()
    new_score = 0
    while running == True:
        startup.dt = (startup.time.tick(60))/1000
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                return
        if menu.start == True:
            screen.fill("black")
            menu.start_screen(screen)
            pygame.display.flip()
        else:
            for object in startup.updateable:
                object.update(startup.dt)
            
            screen.fill("black")
            score.display_score(screen, new_score)
                
            for object in startup.drawable:
                object.draw(screen)

            for asteroid in startup.asteroids:
                if asteroid.collides_with(startup.player):
                    print("Game Over")
                    game_over = GameOver()
                    while game_over.game_state == True:
                        for event in pygame.event.get():
                            if event.type == pygame.QUIT:
                                pygame.quit()
                                return
                            elif event.type == pygame.KEYDOWN or event.type == pygame.MOUSEBUTTONDOWN:
                                game_over.game_state = False
                                menu.start = True
                                new_score = 0
                                del startup
                                startup = Startup()
                            else:
                                h_score = score.check_h_score()
                                if new_score > h_score:
                                    score.write_score(new_score)
                                game_over.display(screen, new_score, h_score)
                        pygame.display.flip()
                for shot in startup.shots:
                    if asteroid.collides_with(shot):
                        asteroid.split()
                        shot.kill()
                        new_score += 1
                        print(new_score)
            
            startup.crosshair_rect.center = pygame.mouse.get_pos()
            screen.blit(startup.crosshair_img, startup.crosshair_rect)

            pygame.display.flip()

def main():
    run_game()

if __name__ == "__main__":
    main()