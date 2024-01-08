import pygame
from config import *
from tile import Tile
from player import Player
from support import *
from random import choice
from weapon import Weapon
from ui import UI
from enemy import Enemy
from retry_screen import Retry
from win_screen import Win

class Level:
    def __init__(self, bgm_control, close_game):

        self.tutorial_state = True
        self.tutorial_state_number = 0
        self.control_text = False
        self.moving_time = None

        self.close_game = close_game
        self.objective_achived = 0

        self.objective_done = False

        self.display_surface = pygame.display.get_surface()
        self.map_location = 0
        self.visible_spirtes = YSortCameraGroup()
        self.obstacle_sprites = pygame.sprite.Group()
        self.player_sprite = pygame.sprite.Group()

        self.bgm_control = bgm_control

        self.current_attack = None
        self.attack_sprites = pygame.sprite.Group()
        self.attackable_srpites = pygame.sprite.Group()
        self.teleporter = pygame.sprite.Group()

        self.can_next_text = False
        self.space_pressed_time = None

        self.attack_string = True

        self.display_text = True

        self.paused = False

        self.gadget_effect = False

        self.treasure_shown = False

        self.gadget_used = False
        self.gadget_used_time = None


        self.blinded = False
        self.normal_screen = True

        self.retry_screen = None
        self.win_screen = None

        self.create_map()

        self.ui = UI()

        self.ore_destroy_sound = pygame.mixer.Sound('../audio\ore_destroy.wav')
        self.ore_destroy_sound.set_volume(0.8)
    def draw_text(self, text,text_col,font_size,x = None, y = None):
        font = pygame.font.Font('../assets/font\joystix.ttf', font_size)
        if self.display_text:
            img = font.render(text, True, text_col)
    
            # Get the rect of the text surface
            text_rect = img.get_rect()

            # Calculate the center of the screen
            if x == None:
                x = (self.display_surface.get_width() - text_rect.width) // 2
            if y == None:
                y = (self.display_surface.get_height() - text_rect.height) // 2

            # Draw the text at the calculated position
            self.display_surface.blit(img, (x, y))

    def create_map(self):
        locations = map[self.map_location] 
        layouts = {
            'boundary': import_csv_layout(f"../map/{locations['boundary']}"),
            'breakable': import_csv_layout(f"../map/{locations['breakable']}"),
            'entity': import_csv_layout(f"../map/{locations['entity']}"),
            'teleporter': import_csv_layout(f"../map/{locations['teleporter']}")
        }
        graphics = {
            'breakable_box': import_folder('../assets\objects/breakable')
        }
        for style, layout in layouts.items():
            for row_index ,row in enumerate(layout):
                for col_index, col in enumerate(row):
                    if col != '-1':
                        x = col_index * TILESIZE
                        y = row_index * TILESIZE
                        if style == 'boundary':
                            Tile((x,y),[self.obstacle_sprites],'invisible')
                        if style == 'teleporter':
                            Tile((x,y),[self.teleporter],'next_room_teleporter')
                        if style == 'breakable':
                            if col == '44':
                                Tile((x,y),[self.visible_spirtes, self.obstacle_sprites, self.attackable_srpites],'break_box',graphics['breakable_box'][0])

                        if style == 'entity':
                            if col == '93':
                                self.player = Player((x,y),[self.visible_spirtes, self.player_sprite],self.obstacle_sprites, self.create_attack, self.destroy_attack, self.use_gadget, self.show_retry_screen)
                            elif col == '321':
                                    Enemy('slime', (x,y), [self.visible_spirtes, self.attackable_srpites], self.obstacle_sprites, self.damage_player, self.bgm_control)
                            elif col == '91':
                                Enemy('boss_slime', (x,y), [self.visible_spirtes, self.attackable_srpites], self.obstacle_sprites, self.damage_player, self.bgm_control, self.summon_ally, self.show_win)
    def summon_ally(self, pos, name):
        Enemy(name, pos, [self.visible_spirtes, self.attackable_srpites], self.obstacle_sprites, self.damage_player, self.bgm_control)
    def create_attack(self):
        self.current_attack = Weapon(self.player,[self.visible_spirtes, self.attack_sprites], self.attack_string)
        self.attack_string = not self.attack_string
    def destroy_attack(self):
        if self.current_attack:
            
            self.current_attack.kill()
        self.current_attack = None
    def use_gadget(self):
        if not self.gadget_used:
            if not self.normal_screen:
                    if not self.gadget_used_time:
                        self.visible_spirtes.mask = self.visible_spirtes.create_screen_mask()
                    self.normal_screen = True
                    self.blinded = False
            self.gadget_used_time = pygame.time.get_ticks()
            self.gadget_used = True
            self.gadget_effect = True

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
                        if target_sprite.sprite_type == 'break_box':
                            if not self.player.health > self.player.stats['health']:
                                self.player.health += 10
                                if self.player.health > self.player.stats['health']:
                                    self.player.health = self.player.stats['health']
                            self.objective_achived +=1
                            self.ore_destroy_sound.play()
                            target_sprite.kill()
                        else:
                            target_sprite.get_damage(self.player)
    def next_room_teleport(self):
        if self.objective_done:
            collided = pygame.sprite.spritecollide(self.player, self.teleporter, dokill=True)
            if collided:
                if collided[0].sprite_type == 'next_room_teleporter':
                    self.display_text = False
                    # Remove old player sprite from groups
                    self.player_sprite.remove(self.player)
                    
                    # Empty relevant sprite groups
                    self.player.player_remove_self()
                    self.teleporter.empty()
                    self.player_sprite.empty()
                    self.visible_spirtes.empty()
                    self.obstacle_sprites.empty()
                    self.attack_sprites.empty()
                    self.attackable_srpites.empty()
                    
                    # Increment map location
                    self.map_location += 1
                    
                    # Update map for the YSortCameraGroup
                    self.visible_spirtes.update_map(self.map_location)
                    
                    # Create a new map and player sprite
                    self.create_map()
                    
                    # Add the new player sprite to the player sprite group
                    self.player_sprite.add(self.player)
                    self.player.focused = True
                    self.player.tutorial_attack = True
                    self.player.tutorial_move = True
                    self.objective_done = False
                    self.objective_achived = 0
                    self.show_objective()
                    self.display_text = True

    def create_tutorial_screen(self):
        if self.can_next_text and not self.control_text:
            self.draw_text("Press Space to Continue.",(225,225,225), 16, None, HEIGHT-50)
        if self.tutorial_state_number == 0:
            if not self.space_pressed_time and not self.can_next_text:
                self.space_pressed_time = pygame.time.get_ticks()
                self.can_next_text = False
            self.draw_text("You have awaken from a long slumber.", (225,225,225), 30, None, HEIGHT-100)
        elif self.tutorial_state_number == 1:
            if not self.space_pressed_time and not self.can_next_text:
                self.space_pressed_time = pygame.time.get_ticks()
                self.can_next_text = False
            self.draw_text("And placed in a unsuall place.",(225,225,225), 30, None, HEIGHT-100)
        elif self.tutorial_state_number == 2:
            if not self.space_pressed_time and not self.can_next_text:
                self.space_pressed_time = pygame.time.get_ticks()
                self.can_next_text = False
            self.draw_text("You feel that you can't control your own body.",(225,225,225), 30, None, HEIGHT-100)
        elif self.tutorial_state_number == 3:
            if not self.space_pressed_time and not self.can_next_text:
                self.space_pressed_time = pygame.time.get_ticks()
                self.can_next_text = False
            self.draw_text("Use WSAD on your keyboard to move around.",(55, 255, 0), 30, None, 100)
            self.control_text =True
            self.player.tutorial_move = True
            self.player.focused = True
            if self.player.moved and not self.moving_time:
                self.moving_time = pygame.time.get_ticks()
        elif self.tutorial_state_number == 4:
            if not self.space_pressed_time and not self.can_next_text:
                self.space_pressed_time = pygame.time.get_ticks()
                self.can_next_text = False
            self.draw_text("Use right mouse click to attack.",(55, 255, 0), 30, None, 100)
            self.control_text =True
            self.player.tutorial_attack = True
            if self.player.attack_time:
                self.tutorial_state_number += 1
        elif self.tutorial_state_number == 5:
            if not self.space_pressed_time and not self.can_next_text:
                self.space_pressed_time = pygame.time.get_ticks()
                self.can_next_text = False
            self.draw_text("Use left mouse click to sprint.",(55, 255, 0), 30, None, 100)
            self.control_text =True
            self.player.tutorial_attack = True
            if self.player.running:
                self.moving_time = pygame.time.get_ticks()
        elif self.tutorial_state_number == 6:
            self.player.tutorial_state = True
            self.control_text =False
            if not self.space_pressed_time and not self.can_next_text:
                self.space_pressed_time = pygame.time.get_ticks()
                self.can_next_text = False
            self.draw_text("Now let's try the movement in a real battle.",(55, 255, 0), 30, None, 100)
        if not self.control_text:
            keys = pygame.key.get_pressed()
            if keys[pygame.K_SPACE] and self.can_next_text and not self.control_text:
                self.tutorial_state_number += 1
                self.can_next_text = False
                if self.tutorial_state_number == 7:
                    player_vec = pygame.math.Vector2(self.player.rect.center)
                    x = player_vec[0] 
                    y = player_vec [1]-100
                    self.tutiorial_slime = Enemy('slime', (x,y), [self.visible_spirtes, self.attackable_srpites], self.obstacle_sprites, self.damage_player, self.bgm_control)
    
    def check_cooldown(self):
        current_time = pygame.time.get_ticks()
        if self.tutorial_state:
            if self.space_pressed_time:
                if current_time - self.space_pressed_time >= 1000:
                    self.can_next_text = True
                    self.space_pressed_time = None
            if self.moving_time:
                if current_time - self.moving_time >=700:
                    self.tutorial_state_number += 1
                    self.moving_time = None
        if self.gadget_used:
            if current_time - self.gadget_used_time >= 20000:
                self.gadget_used = False
                self.gadget_used_time = None
                self.player.gadget_used = False
                self.player.gadget_on_cooldown = False
            elif current_time - self.gadget_used_time >= 1000:
                self.gadget_effect = False
                self.player.gadget_effect = False
    def show_retry_screen(self):
        self.retry_screen = Retry(self.reset_level)
    def show_win(self):
        self.player.player_remove_self()
        self.win_screen = Win(self.close_game)
    def finished_tutorial(self):
        self.tutorial_state = False
        self.objective_done = True
        self.player.tutorial_state = False
    
    def show_objective(self):
        location = map[self.map_location]
        counter = ''
        if location['objective_amount'] > 0:
            counter = f"{self.objective_achived}/{location['objective_amount']}"
        if not self.objective_done:
            self.draw_text(f"Objective: {location['objective']} {counter}",(255, 255, 255), 18, 10, 65)

    def check_objective_finished(self):
        location = map[self.map_location]
        if self.objective_achived >= location['objective_amount'] and not location['objective_amount'] < 0:
            self.objective_done = True
            if not self.treasure_shown:
                self.show_treasure()
    def check_status_effect(self):
        if self.player.status_effect and not self.blinded:
            self.visible_spirtes.create_blindess()
            self.blinded = True
            self.normal_screen = False
        elif not self.player.status_effect and self.blinded and not self.gadget_effect:
            self.visible_spirtes.mask = self.visible_spirtes.create_screen_mask()
            self.player.status_effect = False
            self.blinded = False
            self.normal_screen = True
            
    def show_treasure(self):
        treasure = gadget[0]
        content_container = pygame.Rect((WIDTH/2)-200,(HEIGHT/2)-200, 400,400)
        pygame.draw.rect(self.display_surface, (73,77,82), content_container, border_radius= 20)
        treasure_image = pygame.image.load(f"{treasure['path']}").convert_alpha()
        treasure_image= pygame.transform.scale(treasure_image, (100,100))
        image_rect = treasure_image.get_rect()
        image_rect.topleft = (content_container.left+150, content_container.top +50)
        self.display_surface.blit(treasure_image, image_rect)
        self.draw_text(f"{treasure['name']}",(255, 255, 255), 20, None, (HEIGHT/2)-50)
        self.draw_text(f"{treasure['description']}",(255, 255, 255), 16, None, (HEIGHT/2)+20)
        self.draw_text(f"Cooldown: {treasure['cooldown']} s",(255, 255, 255), 16, None, (HEIGHT/2)+60)
        pygame.display.flip()  # Update the display
        new_gadget = pygame.mixer.Sound('../audio\gadget_new.wav')
        new_gadget.set_volume(0.8)
        new_gadget.play()
        self.treasure_shown = True

        pygame.time.wait(2000)

    def reset_level(self):
        self.display_text = False
        # Remove old player sprite from groups
        self.player_sprite.remove(self.player)
        
        # Empty relevant sprite groups
        self.player.player_remove_self()
        self.teleporter.empty()
        self.player_sprite.empty()
        self.visible_spirtes.empty()
        self.obstacle_sprites.empty()
        self.attack_sprites.empty()
        self.attackable_srpites.empty()
        
        # Update map for the YSortCameraGroup
        self.visible_spirtes.update_map(self.map_location)
        
        # Create a new map and player sprite
        self.retry_screen = None
        self.create_map()
        
        # Add the new player sprite to the player sprite group
        self.player_sprite.add(self.player)
        self.player.focused = True
        self.player.tutorial_attack = True
        self.player.tutorial_move = True
        self.objective_done = False
        self.objective_achived = 0
        self.show_objective()
        self.display_text = True

    def run(self):
        self.visible_spirtes.custom_draw(self.player)
        self.visible_spirtes.update()
        self.visible_spirtes.enemy_update(self.player)
        self.player_attack_logic()
        self.next_room_teleport()

        self.visible_spirtes.draw_screen_mask()
        self.check_cooldown()
        if self.tutorial_state:
            self.create_tutorial_screen()
            if self.tutorial_state_number == 7:
                if self.tutiorial_slime.health <= 0:
                    self.finished_tutorial()
        else:
            self.show_objective()
        if self.treasure_shown:
            if self.gadget_used:
                path = gadget[0]
                self.ui.show_gadget(path["path_used"])
            else:
                path = gadget[0]
                self.ui.show_gadget(path["path"])
        self.check_status_effect()
        
        self.check_objective_finished()
        if self.objective_done:
            location = map[self.map_location]
            self.draw_text(f"{location['objective_finished']}",(255, 255, 255), 18, 10, 65)
        self.ui.display(self.player)
        if self.win_screen:
            self.win_screen.show_win_screen()
        if self.retry_screen and not self.win_screen:
            self.retry_screen.show_retry_screen()


class YSortCameraGroup(pygame.sprite.Group):
    def __init__(self):

        super().__init__()
        self.display_surface = pygame.display.get_surface()
        self.half_width = self.display_surface.get_size()[0]//2
        self.half_height = self.display_surface.get_size()[1]//2
        self.offset = pygame.math.Vector2(100,200)

        #create floor
        image = map[0]
        self.floor_surface = pygame.image.load(f"../map/{image['map_image']}").convert_alpha()
        self.floor_rect = self.floor_surface.get_rect(topleft = (0,0))

        self.mask = self.create_screen_mask()
    def update_map(self, location):
        image = map[location]
        self.floor_surface = pygame.image.load(f"../map/{image['map_image']}").convert_alpha()
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
    

    
    def create_blindess(self):
        resolution_scale = 0.3
        scaled_width = int(self.display_surface.get_width() * resolution_scale)
        scaled_height = int(self.display_surface.get_height() * resolution_scale)

        # Create a surface for the screen mask with the new size
        mask = pygame.Surface((scaled_width, scaled_height), pygame.SRCALPHA)
        mask.fill((0, 0, 0, 230))  # Semi-transparent black color

        # Calculate the scaled screen center and glow radius
        scaled_screen_center = (int(self.half_width * resolution_scale), int(self.half_height * resolution_scale))
        scaled_glow_radius = int(50 * resolution_scale)  # Adjust the radius of the glow effect

        # Draw a circle for the fixed glow effect centered on the scaled screen
        pygame.draw.circle(mask, (0, 0, 0, 20), scaled_screen_center, scaled_glow_radius)

        # Draw the scaled screen mask onto the display surface
        scaled_mask = pygame.transform.scale(mask, self.display_surface.get_size())
        self.mask = scaled_mask

        
    
    def create_screen_mask(self):
        # Create a surface for the screen mask
        resolution_scale = 0.3
        scaled_width = int(self.display_surface.get_width() * resolution_scale)
        scaled_height = int(self.display_surface.get_height() * resolution_scale)

        # Create a surface for the screen mask with the new size
        mask = pygame.Surface((scaled_width, scaled_height), pygame.SRCALPHA)
        mask.fill((0, 0, 0, 200))  # Semi-transparent black color

        # Calculate the scaled screen center and glow radius
        scaled_screen_center = (int(self.half_width * resolution_scale), int(self.half_height * resolution_scale))
        scaled_glow_radius = int(200 * resolution_scale)  # Adjust the radius of the glow effect

        # Draw a circle for the fixed glow effect centered on the scaled screen
        pygame.draw.circle(mask, (0, 0, 0, 20), scaled_screen_center, scaled_glow_radius)

        # Draw the scaled screen mask onto the display surface
        scaled_mask = pygame.transform.scale(mask, self.display_surface.get_size())
        return scaled_mask
    def draw_screen_mask(self):
        self.display_surface.blit(self.mask, (0, 0))