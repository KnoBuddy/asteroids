import pygame

from constants import *
from score import *

class Menu():
    def __init__(self, screen):
        self.start = True
        self.screen = screen

    def start_screen(self, screen):
        pygame.font.init()

        self.button((SCREEN_WIDTH // 2)-30, (SCREEN_HEIGHT // 4)-20, 60, 40, "Start")

        h_score = Score().check_h_score()
        font = pygame.font.Font(None, 72)
        text = font.render(f"High Score: {h_score}", True, (SCORE_COLOR))
        text_rect =  text.get_rect(center=(SCREEN_WIDTH // 2, SCREEN_HEIGHT // 2))
        screen.blit(text, text_rect)

    def button(self, x,y,w,h, text):
        pos = pygame.mouse.get_pos()
        click = pygame.mouse.get_pressed()

        if pos[0] > x and pos[0] < x + w and pos[1] > y and pos[1] < y + h:
            if click[0] == 1:
                self.start = False
        pygame.draw.rect(self.screen, BUTTON_COLOR, (x,y,w,h))
        font = pygame.font.Font(None, 36)
        text = font.render("Start", True, (TEXT_COLOR))
        text_rect = text.get_rect(center=(SCREEN_WIDTH // 2, SCREEN_HEIGHT // 4))
        self.screen.blit(text, text_rect)

    def start_game(self):
        self.start = False