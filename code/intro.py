import pygame
import sys
from retry_screen import Retry
# Initialize Pygame
pygame.init()

# Set up display
width, height = 800, 600
screen = pygame.display.set_mode((width, height))
pygame.display.set_caption("Pygame Button Example")

# Define colors
white = (255, 255, 255)
black = (0, 0, 0)
gray = (200, 200, 200)

# Define Button class
class Button:
    def __init__(self, x, y, width, height, color, text):
        self.rect = pygame.Rect(x, y, width, height)
        self.color = color
        self.text = text
        self.font = pygame.font.Font(None, 36)

    def draw(self):
        pygame.draw.rect(screen, self.color, self.rect)
        text_surface = self.font.render(self.text, True, black)
        text_rect = text_surface.get_rect(center=self.rect.center)
        screen.blit(text_surface, text_rect)

# Create a button
ss = Retry()

# Game loop
while True:

    # Clear the screen
    screen.fill(white)
    ss.show_retry_screen()
    # Update the display
    pygame.display.flip()

    # Cap the frame rate
    pygame.time.Clock().tick(60)
