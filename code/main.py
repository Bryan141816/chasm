import pygame
import sys
from config import *
from level import Level



class Game:
    def __init__(self):
        pygame.init()
        self.screen = pygame.display.set_mode((WIDTH, HEIGHT))
        self.clock = pygame.time.Clock()

        pygame.display.set_caption("Game")

        self.level = Level()
        self.bgm_playing = False
        self.bg_count = 0
        # Load the background image
        self.bg_path = ["../assets\Intro\intro1.jpg","../assets\Intro\intro2.jpg","../assets\Intro\intro3.jpg","../assets\Intro\intro4.jpg","../assets/control/CONTROL_SPLASH.png"]
        self.background_image = pygame.image.load(self.bg_path[self.bg_count]).convert()


        # Scale the background image to fit the screen
        self.background_image = pygame.transform.scale(self.background_image, (WIDTH, HEIGHT))

        self.show_background = True  # Flag to determine whether to show the background

    def run(self):
        while True:
            for event in pygame.event.get():
                if event.type == pygame.QUIT:
                    pygame.quit()
                    sys.exit()
                elif event.type == pygame.MOUSEBUTTONDOWN and event.button == 1:

                    if self.bg_count == 4:
                        self.show_background = False
                        if not self.bgm_playing:

                            main_sound = pygame.mixer.Sound('../audio/bryan-cave.wav')
                            main_sound.play(loops=-1)
                            self.bgm_playing = True
                    else:
                    
                        # Left mouse click
                        self.bg_count += 1
                        self.background_image = pygame.image.load(self.bg_path[self.bg_count]).convert()
                        # Scale the background image to fit the screen
                        self.background_image = pygame.transform.scale(self.background_image, (WIDTH, HEIGHT))
            


            if self.show_background:
                # Draw the scaled background image
                self.screen.blit(self.background_image, (0, 0))
            else:
                # Don't draw the background, instead, run the level
                self.screen.fill('#1c292d')
                self.level.run()

            pygame.display.update()
            self.clock.tick(FPS)

