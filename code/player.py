import pygame
from config import *
from support import *
from entity import Entity
class Player(Entity):
    def __init__(self, pos, groups, obstacle_sprites, create_attack, destroy_attack):
        super().__init__(groups)
        self.image = pygame.image.load('../assets\player\down_idle\idle_down.png').convert_alpha()
        self.rect = self.image.get_rect(topleft = pos)
        self.hitbox = self.rect.inflate(0, -26)


        self.import_player_assets()
        self.status = 'down'

        self.speed = 5

        self.obstacle_sprites = obstacle_sprites

        self.create_attack = create_attack
        self.destroy_attack = destroy_attack

        self.attacking = False
        self.attack_cooldtime = 300
        self.attack_time = None
        self.stats = {'health': 1000, 'speed': 6, 'attack': 50, 'stamina': 100}
        self.health = self.stats['health']
        self.speed = self.stats['speed']
        self.stamina = self.stats['stamina']


        self.running = False


        self.vulnerable = True
        self.hurt_time = None
        self.invisibility_duction = 1000


        self.weapon_attack_sound = pygame.mixer.Sound('../audio\sword.wav')
        self.weapon_attack_sound.set_volume(0.2)


    def import_player_assets(self):
        path = '../assets\player/'
        self.animations = {'up': [], 'down': [], 'left': [], 'right': [],
                           'right_idle': [],'left_idle': [], 'up_idle': [], 'down_idle': [],
                           'right_attack': [], 'left_attack': [], 'up_attack': [], 'down_attack': []}
        
        for animation in self.animations.keys():
            full_path = path + animation
            self.animations[animation] = import_folder(full_path)

    def input(self):
        if not self.attacking:
            keys = pygame.key.get_pressed()

            if keys[pygame.K_w]:
                self.direction.y = -1
                self.status ='up'
            elif keys[pygame.K_s]:
                self.direction.y = 1
                self.status ='down'
            else:
                self.direction.y = 0

            if keys[pygame.K_a]:
                self.direction.x = -1
                self.status ='left'
            elif keys[pygame.K_d]:
                self.direction.x = 1
                self.status ='right'
            else:
                self.direction.x = 0

            mouse = pygame.mouse.get_pressed()
            if mouse[0] and not self.attacking:
                self.attacking = True
                self.attack_time = pygame.time.get_ticks()
                self.create_attack()
                self.weapon_attack_sound.play()
            elif mouse[2] and self.stamina >0 and not self.attacking:
                self.speed = self.stats['speed'] + 2
                self.stamina -= 0.5
                self.running = True
            elif not mouse[2]:
                self.speed = self.stats['speed']
                self.running = False
    
    def cooldown(self):
        current_time = pygame.time.get_ticks()
        if self.attacking:
            if current_time - self.attack_time >= self.attack_cooldtime:
                self.attacking = False
                self.destroy_attack()
        if not self.vulnerable:
            if current_time - self.hurt_time >= self.invisibility_duction:
                self.vulnerable = True
        if not self.running and not self.stamina > self.stats['stamina']:
            self.stamina += 0.5
            if self.stamina > self.stats['stamina']:
                self.stamina = self.stats['stamina']

    def get_status(self):
        if self.direction.x == 0 and self.direction.y == 0:
            if not 'idle' in self.status and not 'attack' in self.status:
                self.status = self.status + '_idle'
        if self.attacking:
            self.direction.x = 0
            self.direction.y = 0
            if not 'attack' in self.status:
                if 'idle' in self.status:
                    self.status = self.status.replace('_idle','_attack')
                else:
                    self.status = self.status + '_attack'
        else:
            if 'attack' in self.status:
                self.status = self.status.replace('_attack','')

        if self.stamina <= 0:
            self.speed = self.stats['speed']
            self.running = False
    def get_full_weapon_damage(self):
        return self.stats['attack']

    def animate(self):
        animation = self.animations[self.status]
        self.frame_index += self.animation_speed
        if self.frame_index >= len(animation):
            self.frame_index = 0
        self.image = animation[int(self.frame_index)]
        self.rect = self.image.get_rect(center = self.hitbox.center)

        if not self.vulnerable:
            #flicker
            alpha = self.wave_value()
            self.image.set_alpha(alpha)
        else:
            self.image.set_alpha(255)
    def check_death(self):
        if self.health <= 0:
            self.kill()
    def update(self):
        self.input()
        self.cooldown()
        self.animate()
        self.get_status()
        self.move(self.speed)
        self.check_death()
