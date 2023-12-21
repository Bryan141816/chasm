import pygame
from config import *
from entity import Entity
from support import *
from node import Node
import random
from traversal import Traversal
class Enemy(Entity):
    def __init__(self, mosnster_name, pos, groups, obstacle_sprites, damage_player, summon_ally = None):
        super().__init__(groups)
        self.boss = False
        self.sprite_type = 'enemy'
        self.import_graphics(mosnster_name)
        self.status = 'idle'
        self.image = self.animations[self.status][self.frame_index]

        self.create_behaivor(mosnster_name)
        self.summon_ally = summon_ally
        if mosnster_name == 'boss_slime':
            self.boss = True
            self.create_attack_pattern()

        self.rect = self.image.get_rect(topleft = pos)
        self.hitbox = self.rect.inflate(0, -26)
        self.obstacle_sprites = obstacle_sprites

        self.monster_name = mosnster_name
        monster_info = monster_data[self.monster_name]
        self.max_health =  monster_info['health']
        self.health = self.max_health
        self.speed = monster_info['speed']
        self.attack_damage = monster_info['damage']
        self.resistance = monster_info['resistance']
        self.attack_radius = monster_info['attack_radius']
        self.notice_radius = monster_info['notice_radius']

        self.can_attack = True
        self.attack_time = None
        self.attack_colldown = 400
        self.damage_player = damage_player

        self.can_special_attack = True
        self.special_attack_time = None
        self.special_attack_cooldown = 5000


        self.vulnerable = True
        self.hit_time = None
        self.invisibility_duction = 300

        self.hit_sound = pygame.mixer.Sound('../audio\hit.wav')
        self.hit_sound.set_volume(0.4)


    def import_graphics(self, name):

        self.animations = {'idle': [],'move':[], 'attack': []}
        main_path = f'../assets\enemy\mob/{name}/'
        for animation in self.animations.keys():
            self.animations[animation] = import_folder(main_path + animation)

    def create_behaivor(self, name):
        self.root = Node(name)
        self.root.left = Node('idle')
        self.root.right = Node('move')
        self.root.right.left = Node('attack')
    
    def create_attack_pattern(self):
        self.attack_root = Node('normal')
        self.attack_root.left = Node('summon')
        self.attack_root.right = Node('heavy')
        


    def get_player_distance_direction(self, player):
        enemy_vec = pygame.math.Vector2(self.rect.center)
        player_vec = pygame.math.Vector2(player.rect.center)
        distance = (player_vec - enemy_vec).magnitude()
        if distance > 0:
            direction = (player_vec- enemy_vec).normalize()
        else:
            direction = pygame.math.Vector2()
        return (distance, direction)
    def get_status(self, player):
        distance = self.get_player_distance_direction(player)[0]
        if distance <= self.attack_radius and self.can_attack:
            if self.status != 'attack':
                self.frame_index = 0
            self.status = self.root.right.left.val
        elif distance <= self.notice_radius:
            self.status = self.root.right.val
        else:
            self.status = self.root.left.val
    def actions(self, player):
        if self.status == 'attack':
            
            if self.boss and self.can_special_attack and self.health <= self.max_health * 0.75:
                self.special_attack_time = pygame.time.get_ticks()
                player_vec = pygame.math.Vector2(player.rect.center)
                self.attack_time = pygame.time.get_ticks()
                random_number = random.choice([0, 1, 2, 3])
                traversal = Traversal()
                attack_type = None
                if random_number == 0:
                    attack_type = traversal.bfs_traversal(self.attack_root)
                elif random_number == 1:
                    attack_type = traversal.dfs_inorder(self.attack_root)
                elif random_number == 2:
                    attack_type = traversal.dfs_postorder(self.attack_root)
                else:
                    attack_type = traversal.dfs_preorder(self.attack_root)
                for attack in attack_type:
                    if attack == 'summon':
                        for i in range(4):
                            random_location = random.randrange(30)
                            x = player_vec[0] + i + random_location
                            y = player_vec [1]+ i + random_location
                            self.summon_ally((x,y), 'slime')
                    elif attack == 'normal':
                        self.damage_player(self.attack_damage)
                    elif attack == 'heavy':
                        self.damage_player(self.attack_damage*2)

                self.can_special_attack = False

            else:
                self.attack_time = pygame.time.get_ticks()
                self.damage_player(self.attack_damage)
        elif self.status == 'move':
            self.direction = self.get_player_distance_direction(player)[1]

        else:
            self.direction = pygame.math.Vector2()
            
    def animate(self):
        animation = self.animations[self.status]

        self.frame_index += self.animation_speed
        if self.frame_index >= len(animation):
            if self.status == 'attack':
                self.can_attack = False
            self.frame_index = 0
        self.image = animation[int(self.frame_index)]
        self.rect = self.image.get_rect(center = self.hitbox.center)

        if not self.vulnerable:
            #flicker
            alpha = self.wave_value()
            self.image.set_alpha(alpha)
        else:
            self.image.set_alpha(255)
    
    def attack_cooldown(self):
        current_time = pygame.time.get_ticks()
        if not self.can_attack:
            if current_time - self.attack_time >= self.attack_colldown:
                self.can_attack = True
        
        if not self.vulnerable:
            if current_time - self.hit_time >= self.invisibility_duction:
                self.vulnerable = True
        if not self.can_special_attack:
            if current_time - self.special_attack_time >= self.special_attack_cooldown:
                self.can_special_attack = True


    def get_damage(self, player):
        if self.vulnerable:
            self.hit_sound.play()
            self.direction = self.get_player_distance_direction(player)[1]
            self.health -= player.get_full_weapon_damage()
            self.hit_time = pygame.time.get_ticks()
            self.vulnerable = False
    
    def check_death(self, player):
        if self.health <= 0:
            if not player.health >= player.stats['health']:
                if self.boss:
                    player.health = player.stats['health']
                else:
                    player.health += 50
                    if player.health > player.stats['health']:
                        player.health = player.stats['health']
            self.kill()
    
    def hit_reaction(self):
        if not self.vulnerable:
            self.direction *= -self.resistance
    def update(self):
        self.hit_reaction()
        self.move(self.speed)
        self.animate()
        self.attack_cooldown()
    
    def enemy_update(self, player):
        self.check_death(player)
        self.get_status(player)
        self.actions(player)
