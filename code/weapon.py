import pygame
from support import *
class Weapon(pygame.sprite.Sprite):
    def __init__(self, player, groups, state):
        super().__init__(groups)

        self.direction = player.status.split('_')[0]

        self.image = None
        self.player = player
        self.state = state
        if not self.state:
            self.direction = self.direction + '2'

        self.import_player_assets()
        self.frame_index = 0
        self.animation_speed = 0.40

        if self.direction == 'right' or self.direction == 'right2':
            self.animate()
            self.rect = self.image.get_rect(midleft = player.rect.midright + pygame.math.Vector2(-25,0))
        elif self.direction == 'left' or self.direction == 'left2':
            self.animate()
            self.rect = self.image.get_rect(midright = player.rect.midleft + pygame.math.Vector2(25,0))
        elif self.direction == 'down' or self.direction == 'down2':
            self.animate()
            self.rect = self.image.get_rect(midtop = player.rect.midbottom + pygame.math.Vector2(0,-25))
        else:
            self.animate()
            self.rect = self.image.get_rect(midbottom = player.rect.midtop + pygame.math.Vector2(0,25))
    def import_player_assets(self):
        path = '../assets\Weapon/'
        self.animations = None
        if self.state:
            self.animations = {'up': [], 'down': [], 'left': [], 'right': []}
        else:
            self.animations = {'up2': [], 'down2': [], 'left2': [], 'right2': []}
        
        for animation in self.animations.keys():
            full_path = path + animation
            self.animations[animation] = import_folder(full_path)
    def animate(self):
        animation = self.animations[self.direction]
        self.frame_index += self.animation_speed
        if not self.frame_index >= len(animation):
            self.image = animation[int(self.frame_index)].convert_alpha()
        if self.frame_index > len(animation):
            self.kill()
    def update(self):
        self.animate()