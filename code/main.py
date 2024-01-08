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

        self.level = Level(self.change_bgm, self.close_game)
        self.bgm_playing = False
        self.boss = False

        self.show_background = True  # Flag to determine whether to show the background
        self.fade_in_duration = 1000  # Duration of the fade-in effect in milliseconds
        self.fade_alpha = 0  # Initial alpha value for fade-in
        
        self.reopen_launcher = reopen_launcher

        self.win = False

        self.bgm_volume = 0
        self.state = True
    def run(self):
        while self.state:
            self.clock.tick(FPS)  # Move the clock tick outside the conditions

            for event in pygame.event.get():
                if event.type == pygame.QUIT:
                    self.state = False
            if ((self.bgm_playing or self.boss) and not self.bgm_volume >=0.5):
                self.bgm_volume += 0.03
                self.main_sound.set_volume(self.bgm_volume)
            else:
                
                # Don't draw the background, instead, run the level
                self.screen.fill('#000000')
                self.level.run()

            pygame.display.update()
        self.reopen_launcher()
        pygame.quit()
    
    def close_game(self):
        self.state = False

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
            self.bgm_playing = True
            self.bgm_volume = 0.5
            self.main_sound = pygame.mixer.Sound('../audio/bryan-goodbye.wav')
            self.main_sound.play(loops=-1)
            self.main_sound.set_volume(self.bgm_volume)


