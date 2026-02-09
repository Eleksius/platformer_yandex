import json

try:
    achievements = json.load(open("achievements.json"))
except FileNotFoundError:
    achievements = {}
    with open('achievements.json', 'w', encoding='utf-8') as f:
        json.dump(achievements, f)

def add_achievement(name, description):
    achievements[name] = description
    with open('achievements.json', 'w', encoding='utf-8') as f:
        json.dump(achievements, f)

def get_achievements():
    return achievements


# Разрешение экрана
SCREEN_WIDTH = 1000
SCREEN_HEIGHT = 650
SCREEN_TITLE = "Platformer"

# Масштаб объектов
CHARACTER_SCALING = 0.7
TILE_SCALING = 0.8
COIN_SCALING = 1

# Движение игрока
PLAYER_MOVEMENT_SPEED = 10
GRAVITY = 1
PLAYER_JUMP_SPEED = 20

# Анимация
RIGHT_FACING = 0
LEFT_FACING = 1