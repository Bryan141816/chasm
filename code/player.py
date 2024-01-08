import pygame
from config import *
from support import *
from entity import Entity
class Player(Entity):
    def __init__(self, pos, groups, obstacle_sprites, create_attack, destroy_attack, use_gadget, show_retry_screen):
        super().__init__(groups)
        self.image = pygame.image.load('../assets\player\down_idle\idle_down.png').convert_alpha()
        self.rect = self.image.get_rect(topleft = pos)
        self.hitbox = self.rect.inflate(0, 0)


        self.import_player_assets()
        self.status = 'down'

        self.use_gadget = use_gadget
        self.show_retry_screen = show_retry_screen
        self.tutorial_state = False


        self.obstacle_sprites = obstacle_sprites

        self.create_attack = create_attack
        self.destroy_attack = destroy_attack
        
        self.focused= False
        self.tutorial_move = False
        self.tutorial_attack = False
        self.moved = False
        self.attacked = False

        self.attacking = False
        self.can_move = True
        self.move_cooldown = 100
        self.attack_cooldtime = 300
        self.attack_time = None
        self.stats = {'health': 100, 'speed': 6, 'attack': 5, 'stamina': 100}
        self.health = self.stats['health']
        self.speed = self.stats['speed']
        self.stamina = self.stats['stamina']

        self.gadget_effect = False
        self.gadget_on_cooldown = False
        self.running = False


        self.status_effect = False



        self.vulnerable = True
        self.hurt_time = None
        self.invisibility_duction = 1000


        self.weapon_attack_sound = pygame.mixer.Sound('../audio\sword.wav')
        self.weapon_attack_sound.set_volume(1)


    def import_player_assets(self):
        path = '../assets\player/'
        self.animations = {'up': [], 'down': [], 'left': [], 'right': [],
                           'right_idle': [],'left_idle': [], 'up_idle': [], 'down_idle': [],
                           'right_attack': [], 'left_attack': [], 'up_attack': [], 'down_attack': []}
        
        for animation in self.animations.keys():
            full_path = path + animation
            self.animations[animation] = import_folder(full_path)

    def input(self):
        if self.focused:
            if self.can_move:
                keys = pygame.key.get_pressed()
                if self.tutorial_move:
                    if keys[pygame.K_w]:
                        self.direction.y = -1
                        self.status ='up'
                        self.moved = True
                    elif keys[pygame.K_s]:
                        self.direction.y = 1
                        self.status ='down'
                        self.moved = True
                    else:
                        self.direction.y = 0
                    if keys[pygame.K_z]:
                        if not self.gadget_effect:
                            self.use_gadget()
                            self.gadget_effect = True
                    if keys[pygame.K_a]:
                        self.direction.x = -1
                        self.status ='left'
                        self.moved = True
                    elif keys[pygame.K_d]:
                        self.direction.x = 1
                        self.status ='right'
                        self.moved = True
                    else:
                        self.direction.x = 0
                
                mouse = pygame.mouse.get_pressed()
                if self.tutorial_attack:
                    if mouse[0] and not self.attacking:
                        self.attacked = True
                        self.attacking = True
                        self.can_move = False
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
        if not self.can_move:
            if current_time - self.attack_time >= self.move_cooldown:
                self.can_move = True
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
    def player_remove_self(self):
        self.kill()

    def animate(self):
        animation = self.animations[self.status]
        self.frame_index += self.animation_speed
        if self.frame_index >= len(animation):
            self.frame_index = 0
        self.image = animation[int(self.frame_index)].convert_alpha()
        self.rect = self.image.get_rect(center = self.hitbox.center)

        if not self.vulnerable:
            #flicker
            alpha = self.wave_value()
            self.image.set_alpha(alpha)
        else:
            self.image.set_alpha(255)
    def check_death(self):
        if self.tutorial_state and self.health <=10:
            self.health = self.stats['health']
        if self.health <= 0:
            self.kill()
            self.show_retry_screen()
    def check_gadget(self):
        if self.gadget_effect:
            self.status_effect = False
    def update(self):
        self.input()
        self.cooldown()
        self.animate()
        self.get_status()
        self.move(self.speed)
        self.check_death()
        self.check_gadget()
