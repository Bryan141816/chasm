import pygame
from config import *
class Retry:
    def __init__(self, reset_level):

        self.display_surface = pygame.display.get_surface()
        self.font = pygame.font.Font(UI_FONT, UI_FONT_SIZE)
        self.health_bar_rect = pygame.Rect(10,10, HEALT_BAR_WIDTH, BAR_HEIGH)
        self.stamina_bar_rect = pygame.Rect(10,40, HEALT_BAR_WIDTH, BAR_HEIGH)
        self.button = None
        self.reset_level = reset_level

        self.content_container = pygame.Rect((WIDTH/2)-200,(HEIGHT/2)-200, 400,400)
        self.button = Button((WIDTH/2)-75,(HEIGHT/2)+100,150,50,(0,255,0),"Retry", self.display_surface)
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
    
    def create_screen_retry(self):
        pygame.draw.rect(self.display_surface, (73,77,82), self.content_container, border_radius= 20)
        self.image = pygame.image.load('../assets\popup\dead.png').convert_alpha()
        self.image= pygame.transform.scale(self.image, (100,100))
        self.image_rect = self.image.get_rect()
        self.image_rect.topleft = (self.content_container.left+150, self.content_container.top +50)
        self.display_surface.blit(self.image, self.image_rect)
        self.draw_text("You died.",(255, 255, 255), 20, None, (HEIGHT/2)-60)
        self.button.draw()
        mouse = pygame.mouse.get_pressed()
        if mouse[0]:
            if self.button.rect.collidepoint(pygame.mouse.get_pos()):
                self.reset_level()


    def show_retry_screen(self):
        self.create_screen_retry()
class Button:
    def __init__(self, x, y, width, height, color, text, surface):
        self.rect = pygame.Rect(x, y, width, height)
        self.color = color
        self.text = text
        self.font = pygame.font.Font(None, 30)
        self.display_surface = surface
    def draw(self):
        pygame.draw.rect(self.display_surface, self.color, self.rect, border_radius= 10)
        text_surface = self.font.render(self.text, True, (255,255,255))
        text_rect = text_surface.get_rect(center=self.rect.center)
        self.display_surface.blit(text_surface, text_rect)
