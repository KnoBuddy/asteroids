import pygame
import os

from constants import *

class Score():
    def __init__(self):
        self.hs_path = "./high_score.txt"
        if os.path.exists(self.hs_path) == False:
            out = open(self.hs_path, "w")
            out.write("0")
            out.close()
        file = open(self.hs_path, "r")     
        score = file.readline()
        file.close()
        score = int(score)

    def display_score(self, screen, score):
        font = pygame.font.Font(None, 36)
        text = font.render(f"Score: {score}", True, (SCORE_COLOR))
        text_rect =  text.get_rect(center=(SCREEN_WIDTH // 20, SCREEN_HEIGHT // 20))
        screen.blit(text, text_rect)

    def check_h_score(self):
        file = open(self.hs_path, "r")
        h_score = int(file.readline())
        file.close()
        return h_score

    def write_score(self, score):
        file = open(self.hs_path, "w")
        file.write(str(score))
        file.close()