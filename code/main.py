import pygame, sys
from config import *
from level import Level

class Game:
    def __init__(self):
        pygame.init()
        self.screen = pygame.display.set_mode((WIDTH, HEIGHT))
        self.clock = pygame.time.Clock()

        self.level = Level()

        main_sound = pygame.mixer.Sound('../audio/bryan-cave.wav')
        main_sound.play(loops= -1)
    def run(self):
        while True:
            for event in pygame.event.get():
                if event.type == pygame.QUIT:
                    pygame.quit()
                    sys.exit()
            
            self.screen.fill('#1c292d')
            self.level.run()
            pygame.display.update()
            self.clock.tick(FPS)

if __name__ == '__main__':
    game = Game()
    game.run()