WIDTH = 1280
HEIGHT = 720
FPS = 60
TILESIZE = 64


map = [
    {
        'objective_finished': 'Find the exit of tutorial level.',
        'map_image': 'tutorial_room.png',
        'boundary': 'tutorial_room_boundary.csv',
        'breakable': 'tutorial_room_breakable.csv',
        'entity': 'tutorial_room_entity.csv',
        'teleporter': 'tutorial_room_teleporter.csv',
        'objective_amount': -1

    },
    {
        'objective': 'Destroy all 6 boxes:',
        'map_image': 'new_map.png',
        'boundary': 'new_map_colision.csv',
        'breakable': 'new_map_breakable.csv',
        'entity': 'new_map_entity.csv',
        'teleporter': 'new_map_next_room.csv',
        'objective_amount': 6,
        'objective_finished': 'Exit the Level.',
        'treasure-type': 'gadget',
        'treasure': 'Purifier'
    },
    {
        'objective': 'Defeat the Slime Boss',
        'map_image': 'boss_domain.png',
        'boundary': 'boss_domain_collision.csv',
        'breakable': 'boss_domain_breakable.csv',
        'entity': 'boss_domain_entity.csv',
        'teleporter': 'boss_domain_teleporter.csv',
        'objective_amount': -1,
        'objective_finished': 'Exit the Level.',
    }
]
gadget = [
    {
        'name': 'Purifier',
        'description': 'Removes any status effect.',
        'cooldown': 20,
        'path': '../assets\spell\purify.png',
        'path_used': '../assets\spell\purify_used.png'
    }
]



BAR_HEIGH = 20
HEALT_BAR_WIDTH = 300
UI_FONT = '../assets/font\joystix.ttf'
UI_FONT_SIZE = 18
UI_COLOR = '#8f8b8b'
TEXT_COLOR = 'white'

HEALTH_COLOR = 'green'
STAMINA_COLOR = 'yellow'

monster_data = {
    'slime': {'health': 50, 'damage': 3, 'attack_type': 'bump', 'speed': 3, 'resistance': 10, 'attack_radius': 50, 'notice_radius': 400},
    'boss_slime': {'health': 200, 'damage': 15, 'attack_type': 'multi_attack', 'speed': 5, 'resistance': 3, 'attack_radius': 100, 'notice_radius': 400}
}