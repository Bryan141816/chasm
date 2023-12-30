import pygame
import sys
from config import *
from level import Level

class Game:
    def __init__(self, reopen_launcher):
        pygame.init()
        self.screen = pygame.display.set_mode((WIDTH, HEIGHT))
        self.clock = pygame.time.Clock()

        pygame.display.set_caption("Game")

        self.level = Level(self.change_bgm)
        self.bgm_playing = False
        self.boss = False
        self.bg_count = 0

        self.intro_screen_time = pygame.time.get_ticks()
        self.intro_screen_cooldown = 2500
        # Load the background image
        self.bg_path = ["../assets/Intro/intro1.jpg", "../assets/Intro/intro2.jpg", "../assets/Intro/intro3.jpg", "../assets/Intro/intro4.jpg", "../assets/control/CONTROL_SPLASH.png"]
        self.background_image = pygame.image.load(self.bg_path[self.bg_count]).convert()

        # Scale the background image to fit the screen
        self.background_image = pygame.transform.scale(self.background_image, (WIDTH, HEIGHT))

        self.show_background = True  # Flag to determine whether to show the background
        self.fade_in_duration = 1000  # Duration of the fade-in effect in milliseconds
        self.fade_alpha = 0  # Initial alpha value for fade-in
        
        self.reopen_launcher = reopen_launcher

        self.win = False

        self.bgm_volume = 0
    def run(self):
        state = True
        while state:
            self.clock.tick(FPS)  # Move the clock tick outside the conditions

            for event in pygame.event.get():
                if event.type == pygame.QUIT:
                    state = False
                elif event.type == pygame.MOUSEBUTTONDOWN and event.button == 1:
                    if self.win:
                        state = False
                    if self.bg_count == 4:
                        self.show_background = False
                        if not self.bgm_playing and not self.boss and not self.win:
                            self.main_sound = pygame.mixer.Sound('../audio/bryan-main_theme.wav')
                            self.main_sound.play(loops=-1)
                            self.main_sound.set_volume(self.bgm_volume)
                            self.bgm_playing = True
            if ((self.bgm_playing or self.boss) and not self.bgm_volume >=1):
                self.bgm_volume += 0.03
                self.main_sound.set_volume(self.bgm_volume)

            if self.win:
                self.background_image = pygame.image.load('launcher\endscreen-01.png').convert()
                self.background_image = pygame.transform.scale(self.background_image, (WIDTH, HEIGHT))
                self.screen.blit(self.background_image, (0, 0))


            if self.bg_count != 4:
                currenttime = pygame.time.get_ticks()
                if currenttime - self.intro_screen_time >= self.intro_screen_cooldown:
                    self.intro_screen_time = currenttime  # Update to current time
                    self.bg_count += 1
                    self.background_image = pygame.image.load(self.bg_path[self.bg_count]).convert()
                    # Scale the background image to fit the screen
                    self.background_image = pygame.transform.scale(self.background_image, (WIDTH, HEIGHT))
                    self.fade_alpha = 0  # Reset alpha value for the new background

            if self.show_background:
                # Draw the scaled background image with fade-in effect
                if self.fade_alpha < 255 and self.clock.get_time() > 0:  # Avoid division by zero
                    self.fade_alpha += 255 / (self.fade_in_duration / self.clock.get_time())
                    self.background_image.set_alpha(int(self.fade_alpha))
                

                self.screen.blit(self.background_image, (0, 0))
                
            elif not self.win:
                
                # Don't draw the background, instead, run the level
                self.screen.fill('#1c292d')
                self.level.run()

            pygame.display.update()
        self.reopen_launcher()
        pygame.quit()


    def change_bgm(self, type):
        if self.bgm_playing or self.boss:
            self.main_sound.stop()
            self.bgm_playing = not self.bgm_playing
            self.boss = not self.boss
        if type == 'start':
            self.boss = True
            self.bgm_volume = 0.5
            self.main_sound = pygame.mixer.Sound('../audio/bryan-slime_boss.wav')
            self.main_sound.play(loops=-1)
            self.main_sound.set_volume(self.bgm_volume)
        elif type == 'win':
            self.win = True
            self.bgm_playing = True
            self.bgm_volume = 0.5
            self.main_sound = pygame.mixer.Sound('../audio/bryan-goodbye.wav')
            self.main_sound.play(loops=-1)
            self.main_sound.set_volume(self.bgm_volume)


