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
# Collisions between asteroids and walls; semi accurate physics bounce --- Mostly Done (Could use exageratted bounce to make it look and feel better)
# Fix bullets to spawn at tip of ship, not from center --- Half DONE!
# Implement multiple lives and respawning
# Add score, menu screen, game loop -- DONE
# Add power ups that change gun type or increase rate of fire --- DONE!
# Levels with different speeds and types of asteroids
# Color different types of asteroids.

import pygame
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
    collision = 0
    while running == True:
        startup.dt = (startup.time.tick(60))/1000
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                return
        if menu.start == True:
            screen.fill("black")
            menu.start_screen(screen)
            pygame.display.flip()
            gun_timer = 0
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
                for asteroids in startup.asteroids:
                    if asteroid.collides_with(asteroids):
                            asteroid.elastic_collision(asteroids, startup.dt, 5000000, 5000000)
                for powerup in startup.powerup:
                    if powerup.collides_with(startup.player):
                        powerup.kill()
                        if startup.player.has_guns == False:
                            if startup.player.has_left_gun == True and startup.player.has_right_gun == False:
                                startup.player.has_right_gun = True
                            if startup.player.has_left_gun == False:
                                startup.player.has_left_gun = True
                if startup.player.has_guns == True:
                    if gun_timer > 10:
                        startup.player.has_left_gun = False
                        startup.player.has_right_gun = False
                        startup.player.has_guns = False
                        gun_timer = 0
                        startup.powerup_spawner.id = 0
            
            startup.crosshair_rect.center = pygame.mouse.get_pos()
            screen.blit(startup.crosshair_img, startup.crosshair_rect)
            if startup.player.has_guns == True:
                gun_timer += startup.dt
                print(gun_timer)

            pygame.display.flip()

def main():
    run_game()

if __name__ == "__main__":
    main()