import pygame
from config import *

class UI:
    def __init__(self):

        self.display_surface = pygame.display.get_surface()
        self.font = pygame.font.Font(UI_FONT, UI_FONT_SIZE)

        self.health_bar_rect = pygame.Rect(WIDTH/2-(HEALT_BAR_WIDTH/2),HEIGHT-80, HEALT_BAR_WIDTH, BAR_HEIGH)
        self.stamina_bar_rect = pygame.Rect(WIDTH/2 - (HEALT_BAR_WIDTH/2), HEIGHT-50, HEALT_BAR_WIDTH, BAR_HEIGH)
    
    def show_bar(self, current, max_amount, bg_rect, color):
        pygame.draw.rect(self.display_surface, UI_COLOR, bg_rect)

        ratio = current / max_amount
        current_width = bg_rect.width * ratio

        current_rect = bg_rect.copy()

        current_rect.width = current_width
        if(current > max_amount*0.2):
            pygame.draw.rect(self.display_surface, color,current_rect)
        else:
            pygame.draw.rect(self.display_surface, 'red',current_rect)
        pygame.draw.rect(self.display_surface, UI_COLOR, bg_rect, 3)


    def display(self,player):
        self.show_bar(player.health, player.stats['health'], self.health_bar_rect, HEALTH_COLOR)
        self.show_bar(player.stamina, player.stats['stamina'], self.stamina_bar_rect, STAMINA_COLOR)
