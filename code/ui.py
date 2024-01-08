import pygame
from config import *

class UI:
    def __init__(self):

        self.display_surface = pygame.display.get_surface()
        self.font = pygame.font.Font(UI_FONT, UI_FONT_SIZE)

        self.gadet_used = False

        self.health_bar_rect = pygame.Rect(10,10, HEALT_BAR_WIDTH, BAR_HEIGH)
        self.stamina_bar_rect = pygame.Rect(10,40, HEALT_BAR_WIDTH, BAR_HEIGH)
    
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
    def draw_text(self, text,text_col,font_size,x = None, y = None):
        font = pygame.font.Font('../assets/font\joystix.ttf', font_size)
        img = font.render(text, True, text_col)

        # Get the rect of the text surface
        text_rect = img.get_rect()
        # Calculate the center of the screen
        if x == None:
            x = (self.display_surface.get_width() - text_rect.width) // 2
        if y == None:
            y = (self.display_surface.get_height() - text_rect.height) // 2
        # Draw the text at the calculated position
        self.display_surface.blit(img, (x, y))

    def show_gadget(self, path):
        treasure_image = pygame.image.load(path).convert_alpha()
        treasure_image= pygame.transform.scale(treasure_image, (50,50))
        image_rect = treasure_image.get_rect()
        image_rect.topleft = (10, HEIGHT-80)
        self.display_surface.blit(treasure_image, image_rect)
        self.draw_text("z", (255,255,255),16, 30,HEIGHT-20)
    def display(self,player):
        self.show_bar(player.health, player.stats['health'], self.health_bar_rect, HEALTH_COLOR)
        self.show_bar(player.stamina, player.stats['stamina'], self.stamina_bar_rect, STAMINA_COLOR)
