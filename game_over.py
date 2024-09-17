import pygame

from constants import *

class GameOver():
    def __init__(self):
        self.game_state = True
    
    def display(self, screen, new_score, h_score):
        screen.fill("black")
        if new_score > h_score:
            font = pygame.font.Font(None, 72)
            text = font.render(f"New High Score: {h_score}", True, (SCORE_COLOR))
            text_rect =  text.get_rect(center=(SCREEN_WIDTH // 2, SCREEN_HEIGHT // 2))
            screen.blit(text, text_rect)
        else:
            font = pygame.font.Font(None, 72)
            text = font.render(f"High Score: {h_score}", True, (SCORE_COLOR))
            text_rect =  text.get_rect(center=(SCREEN_WIDTH // 2, SCREEN_HEIGHT // 2))
            screen.blit(text, text_rect)
            font = pygame.font.Font(None, 36)
            text = font.render(f"Your Score: {new_score}", True, (SCORE_COLOR))
            text_rect =  text.get_rect(center=(SCREEN_WIDTH // 2, SCREEN_HEIGHT // 3))
            screen.blit(text, text_rect)
        font = pygame.font.Font(None, 24)
        text = font.render("Press any key to return to tile screen.", True, (SCORE_COLOR))
        text_rect =  text.get_rect(center=(SCREEN_WIDTH // 2, SCREEN_HEIGHT // 1.5))
        screen.blit(text, text_rect)