import pygame
from support import *
class Weapon(pygame.sprite.Sprite):
    def __init__(self, player, groups):
        super().__init__(groups)

        self.direction = player.status.split('_')[0]

        self.image = None
        self.player = player

        self.import_player_assets()
        self.frame_index = 0
        self.animation_speed = 0.40

        if self.direction == 'right':
            self.animate()
            self.rect = self.image.get_rect(midleft = player.rect.midright + pygame.math.Vector2(-25,0))
        elif self.direction == 'left':
            self.animate()
            self.rect = self.image.get_rect(midright = player.rect.midleft + pygame.math.Vector2(25,0))
        elif self.direction == 'down':
            self.animate()
            self.rect = self.image.get_rect(midtop = player.rect.midbottom + pygame.math.Vector2(0,-25))
        else:
            self.animate()
            self.rect = self.image.get_rect(midbottom = player.rect.midtop + pygame.math.Vector2(0,25))
    def import_player_assets(self):
        path = '../assets\Weapon/'
        self.animations = {'up': [], 'down': [], 'left': [], 'right': []}
        
        for animation in self.animations.keys():
            full_path = path + animation
            self.animations[animation] = import_folder(full_path)
    def animate(self):
        animation = self.animations[self.direction]
        self.frame_index += self.animation_speed
        if not self.frame_index >= len(animation):
            self.image = animation[int(self.frame_index)]
        if self.frame_index > len(animation):
            self.kill()
    def update(self):
        self.animate()