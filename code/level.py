import pygame
from config import *
from tile import Tile
from player import Player
from support import *
from random import choice
from weapon import Weapon
from ui import UI
from enemy import Enemy
class Level:
    def __init__(self, bgm_control):
        self.display_surface = pygame.display.get_surface()
        self.visible_spirtes = YSortCameraGroup()
        self.obstacle_sprites = pygame.sprite.Group()

        self.bgm_control = bgm_control

        self.current_attack = None
        self.attack_sprites = pygame.sprite.Group()
        self.attackable_srpites = pygame.sprite.Group()

        self.create_map()

        self.ui = UI()

        self.ore_destroy_sound = pygame.mixer.Sound('../audio\ore_destroy.wav')
        self.ore_destroy_sound.set_volume(0.8)
    def create_map(self):        
        layouts = {
            'boundary': import_csv_layout('../map/world level._collision.csv'),
            'ore': import_csv_layout('../map\world level._Ore.csv'),
            'entity': import_csv_layout('../map\world level._entity.csv')
        }
        graphics = {
            'ore': import_folder('../assets\ores')
        }
        for style, layout in layouts.items():
            for row_index ,row in enumerate(layout):
                for col_index, col in enumerate(row):
                    if col != '-1':
                        x = col_index * TILESIZE
                        y = row_index * TILESIZE
                        if style == 'boundary':
                            Tile((x,y),[self.obstacle_sprites],'invisible')
                        if style == 'ore':
                            random_ore_image = choice(graphics['ore'])
                            Tile((x,y),[self.visible_spirtes, self.obstacle_sprites, self.attackable_srpites], 'ore', random_ore_image)

                        if style == 'entity':
                            if col == '296':
                                self.player = Player((x,y),[self.visible_spirtes],self.obstacle_sprites, self.create_attack, self.destroy_attack)
                            elif col == '280':
                                Enemy('slime', (x,y), [self.visible_spirtes, self.attackable_srpites], self.obstacle_sprites, self.damage_player, self.bgm_control)
                            elif col == '281':
                                Enemy('boss_slime', (x,y), [self.visible_spirtes, self.attackable_srpites], self.obstacle_sprites, self.damage_player, self.bgm_control, self.summon_ally)
    def summon_ally(self, pos, name):
        Enemy(name, pos, [self.visible_spirtes, self.attackable_srpites], self.obstacle_sprites, self.damage_player, self.bgm_control)
    def create_attack(self):
        self.current_attack = Weapon(self.player,[self.visible_spirtes, self.attack_sprites])
    def destroy_attack(self):
        if self.current_attack:
            
            self.current_attack.kill()
        self.current_attack = None

    def damage_player(self, amount):
        if self.player.vulnerable:
            self.player.health -= amount
            self.player.vulnerable = False
            self.player.hurt_time = pygame.time.get_ticks()
    
    def player_attack_logic(self):
        if self.attack_sprites:
            for attack_sprite  in self.attack_sprites:
                collsion_sprites = pygame.sprite.spritecollide(attack_sprite,self.attackable_srpites, False)
                if collsion_sprites:
                    for target_sprite in collsion_sprites:
                        if target_sprite.sprite_type == 'ore':
                            if not self.player.health > self.player.stats['health']:
                                self.player.health += 10
                                if self.player.health > self.player.stats['health']:
                                    self.player.health = self.player.stats['health']
                            self.ore_destroy_sound.play()
                            target_sprite.kill()
                        else:
                            target_sprite.get_damage(self.player)
    def run(self):
        self.visible_spirtes.custom_draw(self.player)
        self.visible_spirtes.update()
        self.visible_spirtes.enemy_update(self.player)
        self.player_attack_logic()
        self.ui.display(self.player)

class YSortCameraGroup(pygame.sprite.Group):
    def __init__(self):

        super().__init__()
        self.display_surface = pygame.display.get_surface()
        self.half_width = self.display_surface.get_size()[0]//2
        self.half_height = self.display_surface.get_size()[1]//2
        self.offset = pygame.math.Vector2(100,200)

        #create floor
        self.floor_surface = pygame.image.load('../map/world level.png')
        self.floor_rect = self.floor_surface.get_rect(topleft = (0,0))
    
    def enemy_update(self, player):
        enemy_sprite = [sprite for sprite in self.sprites() if hasattr(sprite, 'sprite_type') and sprite.sprite_type == 'enemy']
        for sprite in enemy_sprite:
            sprite.enemy_update(player)

    
    def custom_draw(self, player):

        self.offset.x = player.rect.centerx - self.half_width
        self.offset.y = player.rect.centery - self.half_height

        floor_offset_pos = self.floor_rect.topleft - self.offset
        self.display_surface.blit(self.floor_surface, floor_offset_pos)

        #for sprite in self.sprites():
        for sprite in sorted(self.sprites(), key = lambda sprite: sprite.rect.centery):
            offset_pos = sprite.rect.topleft - self.offset
            self.display_surface.blit(sprite.image, offset_pos)
