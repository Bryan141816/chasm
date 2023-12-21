WIDTH = 1280
HEIGHT = 720
FPS = 60
TILESIZE = 64


BAR_HEIGH = 20
HEALT_BAR_WIDTH = 300
UI_FONT = '../assets/font\joystix.ttf'
UI_FONT_SIZE = 18
UI_COLOR = '#8f8b8b'
TEXT_COLOR = 'white'

HEALTH_COLOR = 'green'
STAMINA_COLOR = 'yellow'

monster_data = {
    'slime': {'health': 250, 'damage': 50, 'attack_type': 'bump', 'speed': 3, 'resistance': 3, 'attack_radius': 50, 'notice_radius': 400},
    'boss_slime': {'health': 2000, 'damage': 80, 'attack_type': 'multi_attack', 'speed': 5, 'resistance': 8, 'attack_radius': 100, 'notice_radius': 400}
}