import json
import math
import random
from array import array
from datetime import datetime
from pathlib import Path

import pygame


WIDTH = 1152
HEIGHT = 700
HUD_HEIGHT = 60
GRID_ROWS = 80
GRID_COLS = 80
CELL_WIDTH = 16.0
CELL_HEIGHT = 16.0
BOARD_TOP = HUD_HEIGHT
BOARD_HEIGHT = HEIGHT - HUD_HEIGHT
WORLD_WIDTH = GRID_COLS * CELL_WIDTH
WORLD_HEIGHT = GRID_ROWS * CELL_HEIGHT
VIEW_CENTER_X = WIDTH / 2
VIEW_CENTER_Y = BOARD_TOP + BOARD_HEIGHT / 2
BOARD_RECT = pygame.Rect(0, BOARD_TOP, WIDTH, BOARD_HEIGHT)
PAUSE_BUTTON_RECT = pygame.Rect(842, 10, 132, 40)
RESUME_BUTTON_RECT = pygame.Rect(986, 10, 148, 40)
RADAR_SIZE = 168
RADAR_RECT = pygame.Rect(16, BOARD_TOP + 16, RADAR_SIZE, RADAR_SIZE)
JOYSTICK_RADIUS = 96
JOYSTICK_CENTER = (WIDTH - 132, BOARD_TOP + 138)
JOYSTICK_DEADZONE = 16

SCORE_FILE = Path(__file__).resolve().with_name("snake_scores.json")
ASSET_DIR = Path(__file__).resolve().with_name("assets")
PORTRAIT_DIR = ASSET_DIR / "portraits"

BG_TOP = (14, 26, 43)
BG_BOTTOM = (27, 49, 70)
PANEL_COLOR = (25, 43, 61)
PANEL_BORDER = (73, 104, 128)
TEXT_COLOR = (239, 246, 248)
MUTED_TEXT = (166, 190, 201)
ACCENT = (52, 205, 151)
ACCENT_HOVER = (78, 226, 173)
FOOD_COLOR = (255, 196, 67)
BOARD_COLOR = (246, 248, 244)
GRID_COLOR = (232, 238, 233)

PLAYER_START_THICKNESS = 8.5
SMALL_START_THICKNESS = 6.0
MIN_THICKNESS = 3.2
MAX_THICKNESS = min(CELL_WIDTH, CELL_HEIGHT) - 2.0

FOOD_TARGET = 28
CLEAR_RADIUS = 10
CLEAR_COOLDOWN_MS = 7000
MAX_EXTRA_SNAKES = 2
CLEAR_SCORE = 20
FULL_CLEAR_SCORE = 100
REINFORCEMENT_THICKNESS = 8.0

TEAM_COLS = 120
TEAM_ROWS = 120
TEAM_MATCH_MS = 5 * 60 * 1000
TEAM_FOOD_TARGET = 70
TEAM_MEMBERS = 5
TEAM_RESPAWN_MS = 2800
TEAM_FOOD_SCORE = 10
TEAM_KILL_SCORE = 25
TEAM_INTERVAL_MS = 130

DIRECTION_STEPS = {
    "up": (0, -1),
    "down": (0, 1),
    "left": (-1, 0),
    "right": (1, 0),
    "up-left": (-1, -1),
    "up-right": (1, -1),
    "down-left": (-1, 1),
    "down-right": (1, 1),
}
OPPOSITE = {
    "up": "down",
    "down": "up",
    "left": "right",
    "right": "left",
    "up-left": "down-right",
    "up-right": "down-left",
    "down-left": "up-right",
    "down-right": "up-left",
}

SKINS = [
    {
        "name": "橘猫",
        "avatar": "cat",
        "pattern": "stripes",
        "body": (244, 176, 96),
        "body_dark": (204, 124, 52),
        "head": (252, 214, 160),
        "outline": (92, 54, 22),
        "highlight": (255, 240, 204),
        "belly": (255, 244, 220),
        "accent": (255, 150, 150),
        "eye": (58, 160, 110),
    },
    {
        "name": "赤狐",
        "avatar": "fox",
        "pattern": "plain",
        "body": (244, 132, 60),
        "body_dark": (200, 82, 28),
        "head": (248, 176, 116),
        "outline": (96, 44, 18),
        "highlight": (255, 224, 190),
        "belly": (255, 248, 236),
        "accent": (255, 250, 240),
        "eye": (80, 50, 20),
    },
    {
        "name": "熊猫",
        "avatar": "panda",
        "pattern": "spots",
        "body": (236, 238, 240),
        "body_dark": (48, 54, 62),
        "head": (250, 250, 252),
        "outline": (24, 28, 34),
        "highlight": (255, 255, 255),
        "belly": (255, 255, 255),
        "accent": (34, 38, 44),
        "eye": (20, 22, 26),
    },
    {
        "name": "白兔",
        "avatar": "rabbit",
        "pattern": "plain",
        "body": (246, 230, 238),
        "body_dark": (212, 184, 200),
        "head": (255, 248, 252),
        "outline": (110, 78, 94),
        "highlight": (255, 255, 255),
        "belly": (255, 252, 254),
        "accent": (255, 150, 180),
        "eye": (96, 64, 84),
    },
    {
        "name": "老虎",
        "avatar": "tiger",
        "pattern": "stripes",
        "body": (246, 166, 62),
        "body_dark": (44, 40, 36),
        "head": (252, 196, 112),
        "outline": (70, 44, 18),
        "highlight": (255, 232, 176),
        "belly": (255, 244, 218),
        "accent": (255, 240, 214),
        "eye": (60, 150, 90),
    },
    {
        "name": "企鹅",
        "avatar": "penguin",
        "pattern": "plain",
        "body": (44, 58, 78),
        "body_dark": (18, 26, 40),
        "head": (30, 40, 56),
        "outline": (8, 12, 18),
        "highlight": (120, 160, 190),
        "belly": (248, 250, 252),
        "accent": (255, 168, 54),
        "eye": (26, 30, 36),
    },
    {
        "name": "青蛙",
        "avatar": "frog",
        "pattern": "spots",
        "body": (96, 198, 98),
        "body_dark": (50, 146, 64),
        "head": (132, 222, 122),
        "outline": (20, 74, 36),
        "highlight": (206, 250, 186),
        "belly": (226, 250, 198),
        "accent": (255, 170, 180),
        "eye": (250, 252, 250),
    },
    {
        "name": "柴犬",
        "avatar": "shiba",
        "pattern": "plain",
        "body": (224, 164, 96),
        "body_dark": (176, 112, 58),
        "head": (244, 198, 140),
        "outline": (86, 50, 24),
        "highlight": (255, 232, 192),
        "belly": (255, 246, 228),
        "accent": (255, 255, 255),
        "eye": (58, 38, 22),
    },
    {
        "name": "粉发少女",
        "avatar": "anime",
        "pattern": "plain",
        "body": (248, 182, 196),
        "body_dark": (214, 130, 156),
        "head": (255, 224, 208),
        "outline": (120, 72, 86),
        "highlight": (255, 246, 248),
        "belly": (255, 238, 240),
        "accent": (255, 142, 164),
        "eye": (72, 120, 200),
        "hair": (255, 150, 186),
    },
    {
        "name": "独角兽",
        "avatar": "unicorn",
        "pattern": "spots",
        "body": (226, 214, 246),
        "body_dark": (180, 160, 220),
        "head": (255, 250, 255),
        "outline": (104, 88, 140),
        "highlight": (255, 255, 255),
        "belly": (255, 255, 255),
        "accent": (255, 214, 120),
        "eye": (110, 80, 180),
        "mane": (186, 150, 255),
    },
]


def _rgb_lighten(color, amount):
    return tuple(min(255, value + amount) for value in color)


def make_skin(
    name,
    avatar,
    body,
    body_dark,
    head,
    outline,
    accent,
    pattern="plain",
    eye=(40, 40, 40),
    **extra
):
    skin = {
        "name": name,
        "avatar": avatar,
        "pattern": pattern,
        "body": body,
        "body_dark": body_dark,
        "head": head,
        "outline": outline,
        "highlight": _rgb_lighten(body, 45),
        "belly": _rgb_lighten(head, 30),
        "accent": accent,
        "eye": eye,
    }
    skin.update(extra)
    return skin


ZODIAC_SKINS = [
    make_skin("灵鼠", "mouse", (170, 170, 185), (120, 120, 140), (225, 220, 220), (55, 50, 60), (255, 170, 180)),
    make_skin("金牛", "ox", (200, 150, 80), (140, 95, 45), (235, 200, 150), (70, 45, 20), (255, 230, 160)),
    make_skin("白虎", "tiger", (235, 235, 240), (130, 135, 150), (250, 250, 252), (70, 75, 90), (120, 120, 130), "stripes"),
    make_skin("玉兔", "rabbit", (246, 230, 238), (212, 184, 200), (255, 248, 252), (110, 78, 94), (255, 150, 180)),
    make_skin("青龙", "dragon", (80, 200, 190), (30, 130, 130), (150, 240, 230), (10, 60, 60), (255, 220, 120), "stripes"),
    make_skin("青蛇", "snake", (90, 190, 110), (35, 120, 60), (160, 230, 170), (12, 55, 25), (255, 180, 120), "spots"),
    make_skin("天马", "horse", (210, 220, 250), (140, 150, 200), (245, 245, 255), (60, 60, 100), (255, 220, 150)),
    make_skin("山羊", "goat", (240, 225, 190), (190, 165, 120), (255, 245, 220), (90, 70, 40), (180, 140, 90)),
    make_skin("金猴", "monkey", (230, 180, 90), (170, 120, 50), (250, 215, 160), (80, 50, 20), (255, 230, 180)),
    make_skin("锦鸡", "rooster", (235, 120, 60), (170, 60, 30), (255, 200, 120), (80, 30, 10), (255, 80, 80), "spots"),
    make_skin("瑞狗", "shiba", (210, 160, 100), (150, 100, 55), (240, 200, 150), (75, 45, 20), (255, 240, 220)),
    make_skin("福猪", "pig", (245, 170, 180), (200, 110, 130), (255, 210, 215), (95, 45, 60), (255, 120, 140)),
]

BOONIE_SKINS = [
    make_skin("熊大", "bear", (150, 100, 60), (95, 60, 35), (200, 150, 95), (50, 30, 15), (255, 220, 180)),
    make_skin("熊二", "bear", (190, 140, 85), (130, 85, 45), (225, 180, 120), (60, 35, 15), (255, 230, 190)),
    make_skin("光头强", "anime", (245, 200, 160), (180, 120, 80), (255, 220, 185), (70, 45, 30), (80, 60, 40), hair=(40, 35, 30)),
    make_skin("吉吉国王", "monkey", (160, 110, 60), (100, 65, 30), (220, 170, 110), (50, 30, 10), (255, 220, 160)),
    make_skin("毛毛", "monkey", (190, 140, 85), (130, 85, 45), (230, 185, 130), (60, 35, 15), (255, 230, 180)),
    make_skin("蹦蹦", "rabbit", (235, 210, 170), (185, 155, 115), (250, 235, 205), (90, 65, 35), (255, 180, 150)),
    make_skin("涂涂", "bird", (130, 170, 200), (70, 110, 150), (220, 235, 245), (30, 50, 70), (255, 190, 80)),
    make_skin("萝卜头", "mouse", (230, 150, 70), (170, 90, 35), (250, 200, 130), (80, 40, 10), (255, 230, 180)),
    make_skin("肥波", "cat", (150, 155, 165), (100, 105, 115), (210, 215, 220), (45, 50, 60), (255, 190, 190)),
    make_skin("老鳄", "croc", (90, 160, 80), (50, 110, 45), (150, 200, 120), (20, 60, 20), (250, 240, 200)),
    make_skin("翠花", "bear", (210, 150, 140), (155, 95, 90), (235, 190, 180), (75, 40, 40), (255, 220, 210)),
    make_skin("纳雅", "anime", (90, 190, 180), (50, 130, 125), (255, 225, 205), (30, 70, 70), (255, 200, 120), hair=(40, 90, 90)),
]

GOAT_SKINS = [
    make_skin("喜羊羊", "goat", (245, 245, 245), (190, 195, 205), (255, 255, 255), (80, 85, 95), (255, 210, 80)),
    make_skin("美羊羊", "goat", (250, 210, 225), (210, 150, 170), (255, 235, 240), (110, 60, 75), (255, 150, 180)),
    make_skin("懒羊羊", "goat", (250, 235, 190), (210, 185, 130), (255, 248, 220), (100, 80, 40), (255, 180, 120)),
    make_skin("沸羊羊", "goat", (220, 170, 110), (170, 115, 60), (245, 210, 160), (85, 50, 20), (255, 120, 80)),
    make_skin("暖羊羊", "goat", (230, 235, 240), (175, 185, 195), (250, 250, 255), (80, 90, 100), (255, 180, 160)),
    make_skin("慢羊羊", "goat", (200, 200, 190), (150, 150, 140), (235, 235, 225), (75, 75, 65), (200, 200, 180)),
    make_skin("灰太狼", "wolf", (130, 140, 155), (80, 90, 105), (190, 200, 210), (35, 40, 50), (255, 200, 120)),
    make_skin("红太狼", "wolf", (220, 90, 80), (150, 45, 45), (245, 170, 150), (75, 20, 20), (255, 220, 180)),
    make_skin("小灰灰", "wolf", (180, 190, 200), (125, 135, 150), (225, 230, 235), (55, 65, 75), (255, 220, 160)),
    make_skin("蕉太狼", "wolf", (230, 200, 90), (170, 140, 45), (250, 230, 150), (80, 65, 20), (255, 240, 180)),
    make_skin("潇洒哥", "anime", (245, 245, 250), (190, 190, 210), (255, 255, 255), (80, 80, 110), (120, 180, 255), hair=(255, 255, 255)),
    make_skin("黑大帅", "anime", (60, 60, 75), (30, 30, 40), (90, 90, 110), (10, 10, 15), (180, 80, 220), hair=(20, 20, 30)),
]

GG_SKINS = [
    make_skin("猪猪侠", "pig", (230, 80, 70), (165, 45, 40), (255, 190, 170), (80, 20, 20), (255, 220, 120)),
    make_skin("菲菲", "pig", (250, 170, 190), (205, 110, 140), (255, 210, 220), (100, 45, 65), (255, 120, 160)),
    make_skin("小呆呆", "pig", (120, 180, 230), (70, 120, 180), (200, 230, 250), (30, 60, 100), (255, 230, 160)),
    make_skin("超人强", "anime", (80, 130, 220), (45, 80, 160), (255, 215, 185), (25, 45, 90), (255, 220, 80), hair=(40, 60, 120)),
    make_skin("波比", "pig", (245, 200, 80), (190, 150, 40), (255, 230, 160), (90, 65, 15), (255, 120, 100)),
    make_skin("迷糊老师", "anime", (160, 165, 175), (110, 115, 125), (235, 220, 200), (50, 55, 65), (120, 200, 255), hair=(80, 80, 90)),
    make_skin("玫瑰王子", "anime", (180, 120, 220), (125, 75, 165), (255, 220, 210), (65, 30, 90), (255, 160, 200), hair=(120, 60, 160)),
    make_skin("白雪", "anime", (245, 245, 255), (190, 195, 220), (255, 240, 235), (85, 85, 120), (180, 220, 255), hair=(240, 240, 255)),
    make_skin("小圣", "robot", (230, 190, 70), (170, 135, 35), (255, 230, 150), (80, 60, 15), (120, 230, 255)),
    make_skin("暗影", "robot", (55, 60, 80), (25, 28, 40), (90, 100, 130), (5, 8, 15), (180, 80, 255)),
    make_skin("铁拳虎", "robot", (230, 130, 60), (170, 80, 30), (250, 190, 120), (70, 30, 10), (120, 220, 255)),
    make_skin("五灵王", "anime", (200, 190, 100), (140, 130, 50), (240, 230, 170), (65, 60, 20), (120, 255, 180), hair=(80, 70, 30)),
]

ULTRA_SKINS = [
    make_skin("初代奥特曼", "ultra", (220, 225, 235), (160, 170, 190), (240, 245, 255), (70, 75, 95), (230, 60, 60), eye=(255, 230, 80)),
    make_skin("赛文", "ultra", (220, 70, 70), (150, 40, 45), (230, 235, 245), (70, 25, 30), (230, 60, 60), eye=(255, 230, 80)),
    make_skin("杰克", "ultra", (210, 215, 230), (150, 160, 185), (240, 245, 255), (60, 70, 95), (220, 70, 70), eye=(255, 235, 90)),
    make_skin("艾斯", "ultra", (80, 130, 210), (45, 85, 155), (230, 240, 255), (25, 45, 90), (220, 70, 70), eye=(140, 220, 255)),
    make_skin("泰罗", "ultra", (220, 75, 70), (150, 45, 45), (245, 235, 210), (75, 30, 25), (255, 205, 70), eye=(255, 230, 80)),
    make_skin("雷欧", "ultra", (190, 60, 60), (120, 30, 35), (230, 220, 220), (55, 20, 20), (240, 200, 80), eye=(255, 220, 70)),
    make_skin("迪迦", "ultra", (150, 120, 220), (95, 75, 160), (235, 240, 255), (45, 35, 85), (220, 180, 70), eye=(255, 240, 120)),
    make_skin("戴拿", "ultra", (70, 140, 220), (35, 90, 160), (235, 245, 255), (20, 45, 85), (230, 70, 70), eye=(140, 230, 255)),
    make_skin("盖亚", "ultra", (210, 70, 70), (145, 40, 45), (240, 235, 225), (70, 25, 25), (255, 205, 70), eye=(255, 230, 80)),
    make_skin("高斯", "ultra", (90, 170, 230), (45, 110, 170), (240, 250, 255), (25, 55, 90), (220, 220, 240), eye=(255, 240, 140)),
    make_skin("赛罗", "ultra", (60, 110, 210), (30, 65, 150), (235, 245, 255), (15, 30, 80), (225, 70, 70), eye=(255, 235, 90)),
    make_skin("泽塔", "ultra", (200, 215, 235), (135, 155, 185), (245, 250, 255), (55, 70, 100), (220, 80, 80), eye=(140, 230, 255)),
]

SKIN_GROUPS = [
    {"key": "classic", "name": "经典", "skins": SKINS},
    {"key": "zodiac", "name": "生肖", "skins": ZODIAC_SKINS},
    {"key": "boonie", "name": "熊出没", "skins": BOONIE_SKINS},
    {"key": "goat", "name": "喜羊羊", "skins": GOAT_SKINS},
    {"key": "gg", "name": "猪猪侠", "skins": GG_SKINS},
    {"key": "ultra", "name": "奥特曼", "skins": ULTRA_SKINS},
]

for _group in SKIN_GROUPS:
    for _skin in _group["skins"]:
        _skin.setdefault("group", _group["name"])

ALL_SKINS = [skin for group in SKIN_GROUPS for skin in group["skins"]]


DIFFICULTIES = [
    {
        "name": "简单",
        "interval": 180,
        "speed": 5.6,
        "color": (66, 190, 115),
        "text_color": (8, 43, 27),
        "small_snakes": 4,
        "respawn": 5200,
    },
    {
        "name": "中等",
        "interval": 120,
        "speed": 8.3,
        "color": (241, 181, 57),
        "text_color": (54, 37, 3),
        "small_snakes": 5,
        "respawn": 4200,
    },
    {
        "name": "很难",
        "interval": 70,
        "speed": 14.3,
        "color": (225, 76, 76),
        "text_color": (255, 245, 245),
        "small_snakes": 6,
        "respawn": 3200,
    },
]

TEAMS = [
    {
        "name": "生肖队",
        "short": "生肖",
        "body": (220, 62, 62),
        "body_dark": (150, 34, 44),
        "outline": (70, 16, 22),
        "highlight": (255, 150, 150),
        "text_color": (255, 245, 245),
        "skins": ZODIAC_SKINS,
    },
    {
        "name": "熊出没队",
        "short": "熊出没",
        "body": (64, 124, 220),
        "body_dark": (36, 74, 160),
        "outline": (16, 34, 80),
        "highlight": (150, 190, 255),
        "text_color": (245, 250, 255),
        "skins": BOONIE_SKINS,
    },
    {
        "name": "喜羊羊与灰太狼队",
        "short": "喜羊羊",
        "body": (70, 190, 110),
        "body_dark": (34, 125, 70),
        "outline": (14, 60, 30),
        "highlight": (160, 240, 190),
        "text_color": (245, 255, 248),
        "skins": GOAT_SKINS,
    },
    {
        "name": "猪猪侠队",
        "short": "猪猪侠",
        "body": (52, 56, 66),
        "body_dark": (24, 26, 32),
        "outline": (8, 9, 12),
        "highlight": (130, 140, 155),
        "text_color": (245, 248, 255),
        "skins": GG_SKINS,
    },
    {
        "name": "奥特曼队",
        "short": "奥特曼",
        "body": (244, 246, 252),
        "body_dark": (188, 194, 212),
        "outline": (80, 88, 110),
        "highlight": (255, 255, 255),
        "text_color": (30, 38, 52),
        "skins": ULTRA_SKINS,
    },
]


pygame.mixer.pre_init(44100, -16, 2, 512)
pygame.init()
AUDIO_ENABLED = pygame.mixer.get_init() is not None
SCREEN = pygame.display.set_mode((WIDTH, HEIGHT))
pygame.display.set_caption("贪吃蛇 - 蛇群争食 / 5 队团队赛")
CLOCK = pygame.time.Clock()

FONT_PATHS = [
    Path("C:/Windows/Fonts/msyh.ttc"),
    Path("C:/Windows/Fonts/simhei.ttf"),
    Path("C:/Windows/Fonts/simsun.ttc"),
]
FONT_PATH = next((path for path in FONT_PATHS if path.exists()), None)
FONT_CACHE = {}
PORTRAIT_CACHE = {}
PORTRAIT_SCALED_CACHE = {}


def create_note_sound(notes, volume):
    if not AUDIO_ENABLED:
        return None

    mixer_settings = pygame.mixer.get_init()
    if mixer_settings is None:
        return None

    sample_rate, sample_format, channels = mixer_settings
    if sample_format != -16:
        return None

    samples = array("h")
    for frequency, duration in notes:
        frame_count = max(1, int(sample_rate * duration))
        for frame in range(frame_count):
            time_value = frame / sample_rate
            envelope = min(
                1.0,
                time_value / 0.015,
                max(0.0, (duration - time_value) / 0.045),
            )
            if frequency <= 0:
                sample_value = 0
            else:
                phase = 2 * math.pi * frequency * time_value
                wave = math.sin(phase) + 0.23 * math.sin(phase * 2)
                sample_value = int(32767 * volume * envelope * wave / 1.23)
            for _ in range(channels):
                samples.append(sample_value)

    try:
        return pygame.mixer.Sound(buffer=samples.tobytes())
    except pygame.error:
        return None


BACKGROUND_MUSIC = create_note_sound(
    [
        (392.00, 0.20),
        (523.25, 0.20),
        (659.25, 0.20),
        (783.99, 0.34),
        (698.46, 0.20),
        (659.25, 0.20),
        (523.25, 0.20),
        (587.33, 0.36),
        (659.25, 0.20),
        (783.99, 0.20),
        (880.00, 0.34),
        (783.99, 0.20),
        (659.25, 0.20),
        (523.25, 0.34),
        (392.00, 0.24),
        (0, 0.12),
    ],
    0.15,
)
EAT_SOUND = create_note_sound(
    [
        (659.25, 0.055),
        (880.00, 0.065),
        (1174.66, 0.10),
    ],
    0.32,
)
DEATH_SOUND = create_note_sound(
    [
        (440.00, 0.15),
        (349.23, 0.16),
        (261.63, 0.22),
        (196.00, 0.34),
    ],
    0.30,
)
SNAKE_DOWN_SOUND = create_note_sound(
    [
        (392.00, 0.07),
        (293.66, 0.09),
        (220.00, 0.13),
    ],
    0.20,
)


def play_sound(sound):
    if sound is None or not AUDIO_ENABLED:
        return
    try:
        sound.play()
    except pygame.error:
        pass


def start_background_music():
    if BACKGROUND_MUSIC is None or not AUDIO_ENABLED:
        return
    try:
        BACKGROUND_MUSIC.stop()
        BACKGROUND_MUSIC.play(loops=-1, fade_ms=220)
    except pygame.error:
        pass


def stop_background_music():
    if BACKGROUND_MUSIC is None:
        return
    try:
        BACKGROUND_MUSIC.fadeout(280)
    except pygame.error:
        pass


def wrapped_delta(value, size):
    value %= size
    if value > size / 2:
        value -= size
    return value


def grid_distance(first, second):
    return abs(first.col - second.col) + abs(first.row - second.row)


def same_team(first, second):
    return first.team_id is not None and first.team_id == second.team_id


def orientation(first, second, third):
    return (
        (second.col - first.col) * (third.row - first.row)
        - (second.row - first.row) * (third.col - first.col)
    )


def segments_cross(a_start, a_end, b_start, b_end):
    first_side = orientation(a_start, a_end, b_start)
    second_side = orientation(a_start, a_end, b_end)
    third_side = orientation(b_start, b_end, a_start)
    fourth_side = orientation(b_start, b_end, a_end)
    return first_side * second_side < 0 and third_side * fourth_side < 0


class Point:
    __slots__ = ("col", "row")

    def __init__(self, col, row):
        self.col = col
        self.row = row

    def copy(self):
        return Point(row=self.row, col=self.col)


class Snake:
    def __init__(
        self,
        body,
        direction,
        skin,
        thickness,
        is_player=False,
        team_id=None,
        name=None,
    ):
        self.body = [part.copy() for part in body]
        self.direction = direction
        self.skin = skin
        self.thickness = thickness
        self.is_player = is_player
        self.team_id = team_id
        self.name = name or skin["name"]
        self.base_skin = skin
        self.eaten = 0
        self.score = 0
        self.kills = 0
        self.alive = True
        self.death_reason = ""

    @property
    def head(self):
        return self.body[0]


def get_font(size, bold=False):
    key = (size, bold)
    if key in FONT_CACHE:
        return FONT_CACHE[key]

    if FONT_PATH is not None:
        font = pygame.font.Font(str(FONT_PATH), size)
        font.set_bold(bold)
    else:
        font = pygame.font.Font(None, size)
        font.set_bold(bold)
    FONT_CACHE[key] = font
    return font


def draw_text(text, size, color, center, bold=False):
    surface = get_font(size, bold).render(text, True, color)
    rect = surface.get_rect(center=center)
    SCREEN.blit(surface, rect)
    return rect


def draw_left_text(text, size, color, position, bold=False):
    surface = get_font(size, bold).render(text, True, color)
    SCREEN.blit(surface, position)
    return surface.get_rect(topleft=position)


def lighten(color, amount):
    return tuple(min(255, value + amount) for value in color)


def mix_color(first, second, ratio):
    ratio = max(0.0, min(1.0, ratio))
    return tuple(
        int(first[index] * (1 - ratio) + second[index] * ratio)
        for index in range(3)
    )


def team_skin(skin, team):
    result = dict(skin)
    result["body"] = team["body"]
    result["body_dark"] = team["body_dark"]
    result["outline"] = team["outline"]
    result["highlight"] = team["highlight"]
    result["belly"] = lighten(team["body"], 42)
    return result


def team_ui_color(team):
    red, green, blue = team["body"]
    if red + green + blue < 300:
        return team["highlight"]
    return team["body"]


def draw_button(rect, label, mouse_pos, color=ACCENT, text_color=(10, 33, 26)):
    hovered = rect.collidepoint(mouse_pos)
    button_color = lighten(color, 24) if hovered else color
    shadow_rect = rect.move(0, 5)
    pygame.draw.rect(SCREEN, (9, 20, 28), shadow_rect, border_radius=14)
    pygame.draw.rect(SCREEN, button_color, rect, border_radius=14)
    pygame.draw.rect(SCREEN, lighten(color, 45), rect, 2, border_radius=14)
    draw_text(label, 25, text_color, rect.center, bold=True)


def draw_hud_button(rect, label, mouse_pos, enabled, color):
    hovered = enabled and rect.collidepoint(mouse_pos)
    shadow_rect = rect.move(0, 3)
    pygame.draw.rect(SCREEN, (9, 20, 28), shadow_rect, border_radius=10)

    if enabled:
        button_color = lighten(color, 22) if hovered else color
        border_color = lighten(color, 45)
        text_color = (23, 32, 28)
    else:
        button_color = (45, 61, 71)
        border_color = (69, 87, 99)
        text_color = (125, 145, 154)

    pygame.draw.rect(SCREEN, button_color, rect, border_radius=10)
    pygame.draw.rect(SCREEN, border_color, rect, 2, border_radius=10)
    draw_text(label, 18, text_color, rect.center, bold=True)


def draw_avatar(surface, center, radius, skin):
    cx = int(center[0])
    cy = int(center[1])
    r = max(6, int(radius))
    kind = skin.get("avatar", "cat")
    outline = skin["outline"]
    body = skin["body"]
    dark = skin["body_dark"]
    face = skin["head"]
    accent = skin.get("accent", skin["highlight"])
    eye_color = skin.get("eye", (44, 44, 44))
    hair = skin.get("hair", dark)
    mane = skin.get("mane", accent)

    def ell(color, x, y, rx, ry, width=0):
        rect = pygame.Rect(0, 0, max(1, int(rx * 2)), max(1, int(ry * 2)))
        rect.center = (int(x), int(y))
        pygame.draw.ellipse(surface, color, rect, width)

    def poly(color, points, width=0):
        pygame.draw.polygon(
            surface,
            color,
            [(int(px), int(py)) for px, py in points],
            width,
        )

    def ear(sign, height, width, inner):
        points = [
            (cx + sign * r * 0.60, cy - r * 0.20),
            (cx + sign * r * (0.60 + width), cy - r * height),
            (cx + sign * r * 0.10, cy - r * 0.55),
        ]
        poly(body, points)
        poly(outline, points, 2)
        inner_points = [
            (cx + sign * r * 0.56, cy - r * 0.28),
            (cx + sign * r * (0.56 + width * 0.55), cy - r * (height - 0.22)),
            (cx + sign * r * 0.20, cy - r * 0.52),
        ]
        poly(inner, inner_points)

    if kind in ("cat", "shiba"):
        ear(-1, 1.35, 0.42, accent)
        ear(1, 1.35, 0.42, accent)
    elif kind == "fox":
        ear(-1, 1.55, 0.50, (255, 246, 232))
        ear(1, 1.55, 0.50, (255, 246, 232))
    elif kind == "tiger":
        ear(-1, 1.22, 0.38, accent)
        ear(1, 1.22, 0.38, accent)
    elif kind == "panda":
        for sign in (-1, 1):
            pygame.draw.circle(
                surface,
                outline,
                (cx + int(sign * r * 0.66), cy - int(r * 0.72)),
                max(3, int(r * 0.38)),
            )
            pygame.draw.circle(
                surface,
                dark,
                (cx + int(sign * r * 0.66), cy - int(r * 0.72)),
                max(2, int(r * 0.30)),
            )
    elif kind == "rabbit":
        for sign in (-1, 1):
            ell(outline, cx + sign * r * 0.38, cy - r * 1.15, r * 0.25, r * 0.72)
            ell(face, cx + sign * r * 0.38, cy - r * 1.15, r * 0.19, r * 0.64)
            ell(accent, cx + sign * r * 0.38, cy - r * 1.18, r * 0.09, r * 0.42)
    elif kind == "frog":
        for sign in (-1, 1):
            pygame.draw.circle(
                surface,
                outline,
                (cx + int(sign * r * 0.46), cy - int(r * 0.80)),
                max(3, int(r * 0.34)),
            )
            pygame.draw.circle(
                surface,
                face,
                (cx + int(sign * r * 0.46), cy - int(r * 0.80)),
                max(2, int(r * 0.28)),
            )
    elif kind == "anime":
        pygame.draw.circle(surface, outline, (cx, cy), r + 4)
        pygame.draw.circle(surface, hair, (cx, cy), r + 2)
    elif kind == "unicorn":
        ear(-1, 1.35, 0.32, accent)
        ear(1, 1.35, 0.32, accent)
        poly(accent, [(cx, cy - r * 1.80), (cx - r * 0.16, cy - r * 0.90), (cx + r * 0.16, cy - r * 0.90)])
        poly(
            outline,
            [(cx, cy - r * 1.80), (cx - r * 0.16, cy - r * 0.90), (cx + r * 0.16, cy - r * 0.90)],
            1,
        )
    elif kind == "dragon":
        for sign in (-1, 1):
            poly(
                accent,
                [
                    (cx + sign * r * 0.32, cy - r * 0.90),
                    (cx + sign * r * 0.65, cy - r * 1.65),
                    (cx + sign * r * 0.85, cy - r * 0.80),
                ],
            )
            poly(
                outline,
                [
                    (cx + sign * r * 0.32, cy - r * 0.90),
                    (cx + sign * r * 0.65, cy - r * 1.65),
                    (cx + sign * r * 0.85, cy - r * 0.80),
                ],
                1,
            )
        ear(-1, 1.20, 0.30, accent)
        ear(1, 1.20, 0.30, accent)
    elif kind == "mouse":
        for sign in (-1, 1):
            pygame.draw.circle(
                surface,
                outline,
                (cx + int(sign * r * 0.62), cy - int(r * 0.72)),
                max(3, int(r * 0.40)),
            )
            pygame.draw.circle(
                surface,
                face,
                (cx + int(sign * r * 0.62), cy - int(r * 0.72)),
                max(2, int(r * 0.30)),
            )
            pygame.draw.circle(
                surface,
                accent,
                (cx + int(sign * r * 0.62), cy - int(r * 0.72)),
                max(1, int(r * 0.16)),
            )
    elif kind == "bear":
        for sign in (-1, 1):
            pygame.draw.circle(
                surface,
                outline,
                (cx + int(sign * r * 0.62), cy - int(r * 0.70)),
                max(3, int(r * 0.34)),
            )
            pygame.draw.circle(
                surface,
                body,
                (cx + int(sign * r * 0.62), cy - int(r * 0.70)),
                max(2, int(r * 0.25)),
            )
    elif kind == "goat":
        for sign in (-1, 1):
            points = [
                (cx + sign * r * 0.30, cy - r * 0.72),
                (cx + sign * r * 0.52, cy - r * 1.22),
                (cx + sign * r * 0.86, cy - r * 1.02),
            ]
            poly(accent, points)
            poly(outline, points, 2)
        ear(-1, 1.10, 0.30, face)
        ear(1, 1.10, 0.30, face)
    elif kind == "pig":
        for sign in (-1, 1):
            pygame.draw.circle(
                surface,
                outline,
                (cx + int(sign * r * 0.58), cy - int(r * 0.68)),
                max(3, int(r * 0.30)),
            )
            pygame.draw.circle(
                surface,
                body,
                (cx + int(sign * r * 0.58), cy - int(r * 0.68)),
                max(2, int(r * 0.22)),
            )
    elif kind == "wolf":
        ear(-1, 1.48, 0.46, accent)
        ear(1, 1.48, 0.46, accent)
    elif kind == "monkey":
        for sign in (-1, 1):
            pygame.draw.circle(
                surface,
                outline,
                (cx + int(sign * r * 0.68), cy - int(r * 0.55)),
                max(3, int(r * 0.30)),
            )
            pygame.draw.circle(
                surface,
                face,
                (cx + int(sign * r * 0.68), cy - int(r * 0.55)),
                max(2, int(r * 0.22)),
            )
    elif kind == "horse":
        ear(-1, 1.18, 0.28, accent)
        ear(1, 1.18, 0.28, accent)
        poly(
            dark,
            [
                (cx - r * 0.70, cy - r * 0.75),
                (cx - r * 0.05, cy - r * 1.10),
                (cx + r * 0.30, cy - r * 0.85),
                (cx - r * 0.10, cy - r * 0.45),
            ],
        )
    elif kind == "rooster":
        for offset in (-0.30, 0.0, 0.30):
            pygame.draw.circle(
                surface,
                (220, 60, 60),
                (cx + int(r * offset), cy - int(r * 0.98)),
                max(2, int(r * 0.16)),
            )
            pygame.draw.circle(
                surface,
                outline,
                (cx + int(r * offset), cy - int(r * 0.98)),
                max(2, int(r * 0.16)),
                1,
            )
    elif kind == "snake":
        pygame.draw.circle(surface, body, (cx, cy), r + 4)
    elif kind == "croc":
        for sign in (-1, 1):
            pygame.draw.circle(
                surface,
                outline,
                (cx + int(sign * r * 0.45), cy - int(r * 0.75)),
                max(2, int(r * 0.16)),
            )
            pygame.draw.circle(
                surface,
                face,
                (cx + int(sign * r * 0.45), cy - int(r * 0.75)),
                max(2, int(r * 0.12)),
            )
    elif kind == "bird":
        poly(
            accent,
            [
                (cx - r * 0.18, cy - r * 0.90),
                (cx, cy - r * 1.30),
                (cx + r * 0.18, cy - r * 0.90),
            ],
        )
    elif kind == "ox":
        for sign in (-1, 1):
            points = [
                (cx + sign * r * 0.34, cy - r * 0.72),
                (cx + sign * r * 0.72, cy - r * 1.20),
                (cx + sign * r * 0.94, cy - r * 0.92),
            ]
            poly(accent, points)
            poly(outline, points, 2)
        ear(-1, 1.15, 0.32, face)
        ear(1, 1.15, 0.32, face)
    elif kind == "ultra":
        poly(
            (220, 60, 60),
            [
                (cx, cy - r * 1.85),
                (cx - r * 0.16, cy - r * 0.85),
                (cx + r * 0.16, cy - r * 0.85),
            ],
        )
        poly(
            outline,
            [
                (cx, cy - r * 1.85),
                (cx - r * 0.16, cy - r * 0.85),
                (cx + r * 0.16, cy - r * 0.85),
            ],
            1,
        )
    elif kind == "robot":
        pygame.draw.line(
            surface,
            outline,
            (cx, cy - r),
            (cx, cy - r * 1.55),
            max(1, int(r * 0.10)),
        )
        pygame.draw.circle(
            surface,
            accent,
            (cx, cy - int(r * 1.58)),
            max(2, int(r * 0.15)),
        )

    pygame.draw.circle(surface, outline, (cx, cy), r + 2)
    pygame.draw.circle(surface, face, (cx, cy), r)
    if r >= 18:
        pygame.draw.circle(
            surface,
            mix_color(face, (255, 255, 255), 0.30),
            (cx - int(r * 0.36), cy - int(r * 0.44)),
            max(2, int(r * 0.18)),
        )
        pygame.draw.arc(
            surface,
            mix_color(face, outline, 0.20),
            pygame.Rect(
                cx - r + 2,
                cy - r + 2,
                max(2, 2 * r - 4),
                max(2, 2 * r - 4),
            ),
            0,
            math.pi,
            max(1, int(r * 0.06)),
        )

    if kind == "penguin":
        ell((248, 250, 252), cx, cy + r * 0.16, r * 0.78, r * 0.64)
    elif kind == "anime":
        poly(
            hair,
            [
                (cx - r * 0.98, cy - r * 0.15),
                (cx - r * 0.75, cy - r * 0.95),
                (cx - r * 0.30, cy - r * 0.55),
                (cx, cy - r * 1.05),
                (cx + r * 0.30, cy - r * 0.55),
                (cx + r * 0.78, cy - r * 0.95),
                (cx + r * 0.98, cy - r * 0.15),
            ],
        )
        if r >= 18:
            for offset in (-0.55, -0.15, 0.25):
                pygame.draw.line(
                    surface,
                    mix_color(hair, (255, 255, 255), 0.40),
                    (cx + int(r * offset), cy - int(r * 0.80)),
                    (cx + int(r * (offset + 0.18)), cy - int(r * 0.45)),
                    max(1, int(r * 0.06)),
                )
    elif kind == "unicorn":
        for index in range(3):
            pygame.draw.circle(
                surface,
                mane,
                (cx - int(r * 0.72), cy - int(r * 0.15) + index * int(r * 0.32)),
                max(2, int(r * 0.18)),
            )

    if kind == "pig":
        ell((255, 180, 190), cx, cy + r * 0.18, r * 0.40, r * 0.26)
        for sign in (-1, 1):
            pygame.draw.circle(
                surface,
                outline,
                (cx + int(sign * r * 0.13), cy + int(r * 0.18)),
                max(1, int(r * 0.05)),
            )
    elif kind == "goat":
        ell(face, cx, cy + r * 0.42, r * 0.24, r * 0.34)
        pygame.draw.line(
            surface,
            outline,
            (cx - r * 0.10, cy + r * 0.42),
            (cx + r * 0.10, cy + r * 0.42),
            max(1, int(r * 0.05)),
        )
    elif kind == "wolf":
        ell(face, cx, cy + r * 0.24, r * 0.32, r * 0.22)
        pygame.draw.circle(
            surface,
            outline,
            (cx, cy + int(r * 0.16)),
            max(1, int(r * 0.06)),
        )
    elif kind == "mouse":
        ell(face, cx, cy + r * 0.28, r * 0.20, r * 0.14)
        pygame.draw.circle(
            surface,
            (255, 160, 170),
            (cx, cy + int(r * 0.26)),
            max(1, int(r * 0.05)),
        )
    elif kind == "ultra":
        for sign in (-1, 1):
            pygame.draw.line(
                surface,
                (220, 60, 60),
                (cx + sign * int(r * 0.72), cy - int(r * 0.28)),
                (cx + sign * int(r * 0.92), cy + int(r * 0.22)),
                max(1, int(r * 0.10)),
            )
    elif kind == "robot":
        visor = pygame.Rect(
            cx - int(r * 0.62),
            cy - int(r * 0.28),
            int(r * 1.24),
            int(r * 0.46),
        )
        pygame.draw.rect(surface, (18, 28, 38), visor, border_radius=max(2, int(r * 0.12)))
        pygame.draw.rect(
            surface,
            (90, 220, 255),
            visor,
            2,
            border_radius=max(2, int(r * 0.12)),
        )

    if kind == "monkey":
        ell(lighten(face, 18), cx, cy + r * 0.05, r * 0.60, r * 0.55)
    elif kind == "horse":
        ell(lighten(face, 12), cx, cy + r * 0.28, r * 0.40, r * 0.28)
        for sign in (-1, 1):
            pygame.draw.circle(
                surface,
                outline,
                (cx + sign * int(r * 0.12), cy + int(r * 0.32)),
                max(1, int(r * 0.05)),
            )
    elif kind == "rooster":
        poly(
            (255, 180, 60),
            [
                (cx - r * 0.16, cy + r * 0.18),
                (cx + r * 0.16, cy + r * 0.18),
                (cx, cy + r * 0.48),
            ],
        )
    elif kind == "snake":
        pygame.draw.line(
            surface,
            (255, 80, 100),
            (cx, cy + int(r * 0.18)),
            (cx, cy + int(r * 0.55)),
            max(1, int(r * 0.05)),
        )
        pygame.draw.line(
            surface,
            (255, 80, 100),
            (cx, cy + int(r * 0.55)),
            (cx - int(r * 0.14), cy + int(r * 0.70)),
            max(1, int(r * 0.04)),
        )
        pygame.draw.line(
            surface,
            (255, 80, 100),
            (cx, cy + int(r * 0.55)),
            (cx + int(r * 0.14), cy + int(r * 0.70)),
            max(1, int(r * 0.04)),
        )
    elif kind == "croc":
        ell(face, cx, cy + r * 0.30, r * 0.55, r * 0.28)
        for sign in (-1, 1):
            poly(
                (250, 250, 240),
                [
                    (cx + sign * r * 0.10, cy + r * 0.40),
                    (cx + sign * r * 0.22, cy + r * 0.40),
                    (cx + sign * r * 0.16, cy + r * 0.52),
                ],
            )
    elif kind == "bird":
        poly(
            (255, 180, 60),
            [
                (cx - r * 0.14, cy + r * 0.20),
                (cx + r * 0.14, cy + r * 0.20),
                (cx, cy + r * 0.46),
            ],
        )
    if kind == "goat" and skin.get("group") == "喜羊羊":
        bell_y = cy + int(r * 0.95)
        pygame.draw.circle(
            surface,
            (255, 204, 64),
            (cx, bell_y),
            max(2, int(r * 0.10)),
        )
        pygame.draw.circle(
            surface,
            outline,
            (cx, bell_y),
            max(2, int(r * 0.10)),
            1,
        )
    if kind == "tiger":
        for offset in (-0.28, 0.0, 0.28):
            pygame.draw.line(
                surface,
                dark,
                (cx + int(r * offset), cy - int(r * 0.78)),
                (cx + int(r * offset), cy - int(r * 0.42)),
                max(1, int(r * 0.08)),
            )
    if kind == "panda":
        for sign in (-1, 1):
            ell(dark, cx + sign * r * 0.36, cy - r * 0.06, r * 0.24, r * 0.30)

    if kind == "frog":
        for sign in (-1, 1):
            pygame.draw.circle(
                surface,
                (20, 24, 28),
                (cx + int(sign * r * 0.46), cy - int(r * 0.80)),
                max(1, int(r * 0.11)),
            )
    elif kind == "ultra":
        for sign in (-1, 1):
            ex = cx + sign * int(r * 0.36)
            ey = cy - int(r * 0.05)
            ell((255, 245, 150), ex, ey, r * 0.22, r * 0.14)
            pygame.draw.circle(surface, (255, 230, 80), (ex, ey), max(1, int(r * 0.08)))
    elif kind == "robot":
        for sign in (-1, 1):
            ex = cx + sign * int(r * 0.30)
            ey = cy - int(r * 0.04)
            pygame.draw.circle(surface, (120, 240, 255), (ex, ey), max(2, int(r * 0.12)))
            pygame.draw.circle(surface, (255, 255, 255), (ex, ey), max(1, int(r * 0.05)))
    elif kind == "anime":
        for sign in (-1, 1):
            ex = cx + sign * int(r * 0.38)
            ey = cy + int(r * 0.05)
            ell((255, 255, 255), ex, ey, r * 0.22, r * 0.28)
            pygame.draw.circle(surface, eye_color, (ex, ey), max(2, int(r * 0.15)))
            pygame.draw.circle(surface, (20, 22, 28), (ex, ey), max(1, int(r * 0.08)))
            pygame.draw.circle(
                surface,
                (255, 255, 255),
                (ex - int(r * 0.05), ey - int(r * 0.07)),
                max(1, int(r * 0.04)),
            )
            if r >= 18:
                pygame.draw.line(
                    surface,
                    outline,
                    (ex - int(r * 0.22), ey - int(r * 0.20)),
                    (ex + int(r * 0.22), ey - int(r * 0.22)),
                    max(1, int(r * 0.05)),
                )
        for sign in (-1, 1):
            ell((255, 150, 170), cx + sign * r * 0.62, cy + r * 0.38, r * 0.14, r * 0.08)
        pygame.draw.arc(
            surface,
            outline,
            pygame.Rect(cx - int(r * 0.12), cy + int(r * 0.32), max(2, int(r * 0.24)), max(2, int(r * 0.16))),
            math.pi,
            math.tau,
            1,
        )
    else:
        eye_radius = max(1, int(r * 0.15))
        for sign in (-1, 1):
            ex = cx + sign * int(r * 0.34)
            ey = cy - int(r * 0.08)
            if r >= 18:
                pygame.draw.circle(
                    surface,
                    mix_color(face, outline, 0.18),
                    (ex, ey),
                    eye_radius + 3,
                )
            pygame.draw.circle(surface, (250, 252, 250), (ex, ey), eye_radius + 1)
            pygame.draw.circle(surface, eye_color, (ex, ey), eye_radius)
            if kind in ("cat", "tiger", "snake", "croc"):
                pupil_w = max(1, int(eye_radius * 0.38))
                pupil_h = max(2, int(eye_radius * 1.10))
                pygame.draw.ellipse(
                    surface,
                    (18, 20, 26),
                    pygame.Rect(
                        ex - pupil_w,
                        ey - pupil_h,
                        pupil_w * 2,
                        pupil_h * 2,
                    ),
                )
            else:
                pygame.draw.circle(
                    surface,
                    (18, 20, 26),
                    (ex, ey),
                    max(1, int(eye_radius * 0.55)),
                )
            pygame.draw.circle(
                surface,
                (255, 255, 255),
                (
                    ex - max(1, eye_radius // 3),
                    ey - max(1, eye_radius // 3),
                ),
                max(1, eye_radius // 3),
            )

        if r >= 18 and kind not in ("snake", "croc"):
            for sign in (-1, 1):
                ex = cx + sign * int(r * 0.34)
                ey = cy - int(r * 0.08)
                pygame.draw.line(
                    surface,
                    outline,
                    (ex - int(r * 0.12), ey - int(r * 0.22)),
                    (ex + int(r * 0.12), ey - int(r * 0.24)),
                    max(1, int(r * 0.05)),
                )
    if kind in ("cat", "tiger"):
        for sign in (-1, 1):
            for delta in (-0.06, 0.10):
                pygame.draw.line(
                    surface,
                    outline,
                    (cx + int(sign * r * 0.42), cy + int(r * 0.30)),
                    (cx + int(sign * r * 0.95), cy + int(r * (0.20 + delta))),
                    1,
                )

    if kind == "penguin":
        poly((255, 168, 54), [(cx - r * 0.18, cy + r * 0.20), (cx + r * 0.18, cy + r * 0.20), (cx, cy + r * 0.52)])
    elif kind == "frog":
        pygame.draw.arc(
            surface,
            outline,
            pygame.Rect(cx - int(r * 0.55), cy + int(r * 0.02), max(2, int(r * 1.1)), max(2, int(r * 0.45))),
            math.pi,
            math.tau,
            2,
        )
    elif kind not in ("anime", "ultra", "robot", "pig", "rooster", "bird", "snake", "croc"):
        ell(skin["belly"], cx, cy + r * 0.36, r * 0.46, r * 0.28)
        poly(
            outline,
            [
                (cx - r * 0.09, cy + r * 0.20),
                (cx + r * 0.09, cy + r * 0.20),
                (cx, cy + r * 0.34),
            ],
        )
        pygame.draw.arc(
            surface,
            outline,
            pygame.Rect(cx - int(r * 0.22), cy + int(r * 0.30), max(2, int(r * 0.44)), max(2, int(r * 0.22))),
            0,
            math.pi,
            1,
        )

    if kind in ("rabbit", "anime", "bear", "mouse", "goat", "pig"):
        for sign in (-1, 1):
            ell((255, 150, 170), cx + sign * r * 0.62, cy + r * 0.38, r * 0.14, r * 0.08)


# Optional licensed PNG portraits. Live2D/Spine runtimes are not bundled.
def load_portrait_image(skin):
    image_module = getattr(pygame, "image", None)
    if image_module is None or not PORTRAIT_DIR.exists():
        return None
    candidates = [
        PORTRAIT_DIR / f"{skin.get('group', '经典')}_{skin['name']}.png",
        PORTRAIT_DIR / f"{skin['name']}.png",
    ]
    for path in candidates:
        if not path.exists():
            continue
        key = str(path)
        if key not in PORTRAIT_CACHE:
            try:
                image = image_module.load(key).convert_alpha()
            except (pygame.error, OSError):
                image = None
            PORTRAIT_CACHE[key] = image
        if PORTRAIT_CACHE[key] is not None:
            return PORTRAIT_CACHE[key], key
    return None


def scaled_portrait_image(image, key, size):
    cache_key = (key, size)
    if cache_key not in PORTRAIT_SCALED_CACHE:
        try:
            scaled = pygame.transform.smoothscale(image, size)
        except (pygame.error, ValueError):
            scaled = image
        PORTRAIT_SCALED_CACHE[cache_key] = scaled
    return PORTRAIT_SCALED_CACHE[cache_key]


def draw_closed_eyes(surface, center, radius, skin):
    cx = int(center[0])
    cy = int(center[1])
    r = max(6, int(radius))
    kind = skin.get("avatar", "cat")
    if kind == "frog":
        x_offset, y_offset = 0.46, -0.80
    elif kind == "ultra":
        x_offset, y_offset = 0.36, -0.05
    elif kind == "robot":
        x_offset, y_offset = 0.30, -0.04
    elif kind == "anime":
        x_offset, y_offset = 0.38, 0.05
    else:
        x_offset, y_offset = 0.34, -0.08
    color = skin["outline"]
    width = max(1, int(r * 0.07))
    for sign in (-1, 1):
        ex = cx + sign * int(r * x_offset)
        ey = cy + int(r * y_offset)
        pygame.draw.line(
            surface,
            color,
            (ex - int(r * 0.15), ey),
            (ex + int(r * 0.15), ey),
            width,
        )
        pygame.draw.line(
            surface,
            color,
            (ex + sign * int(r * 0.14), ey),
            (ex + sign * int(r * 0.20), ey + int(r * 0.03)),
            max(1, int(r * 0.04)),
        )

def draw_avatar_portrait(surface, center, radius, skin, team=None, show_badge=True):
    cx = int(center[0])
    cy = int(center[1])
    r = max(10, int(radius))
    if team is not None:
        ring = team_ui_color(team)
        ring_light = team["highlight"]
    else:
        red, green, blue = skin["body"]
        ring = skin["highlight"] if red + green + blue < 300 else skin["body"]
        ring_light = skin["highlight"]

    shadow = pygame.Rect(
        cx - r - 8,
        cy + r - 2,
        (r + 8) * 2,
        max(6, r // 3),
    )
    pygame.draw.ellipse(surface, (7, 14, 21), shadow)

    for step in range(3):
        radius = r + 10 - step * 2
        pygame.draw.circle(
            surface,
            mix_color((14, 27, 39), ring, 0.10 + step * 0.08),
            (cx, cy),
            radius,
        )
    pygame.draw.circle(surface, ring, (cx, cy), r + 10, 3)
    pygame.draw.circle(
        surface,
        mix_color(ring, (255, 255, 255), 0.35),
        (cx, cy),
        r + 7,
        1,
    )
    pygame.draw.circle(surface, (25, 43, 57), (cx, cy), r + 4)
    now = pygame.time.get_ticks() / 1000.0
    phase = (sum(ord(character) for character in skin["name"]) % 360) * math.pi / 180.0
    bob = math.sin(now * 1.7 + phase) * (r * 0.025)
    sway = math.sin(now * 1.15 + phase) * (r * 0.035)
    breath = 1.0 + math.sin(now * 1.45 + phase) * 0.012
    head_r = max(10, int(r * breath))
    head_cx = cx + int(sway)
    head_cy = cy + int(bob)

    asset = load_portrait_image(skin)
    if asset is not None:
        image, key = asset
        image_width = max(1, image.get_width())
        image_height = max(1, image.get_height())
        fit = min(
            (head_r * 2) / image_width,
            (head_r * 2) / image_height,
        )
        size = (
            max(1, int(image_width * fit)),
            max(1, int(image_height * fit)),
        )
        scaled = scaled_portrait_image(image, key, size)
        image_rect = scaled.get_rect(center=(head_cx, head_cy))
        surface.blit(scaled, image_rect)
    else:
        draw_avatar(surface, (head_cx, head_cy), head_r, skin)
        blink = ((now + phase * 0.37) % 4.2) < 0.13
        if blink and r >= 18:
            draw_closed_eyes(surface, (head_cx, head_cy), head_r, skin)

    group = skin.get("group", "经典")
    if group == "生肖":
        collar_color = (255, 204, 64)
    elif group == "熊出没":
        collar_color = (96, 180, 110)
    elif group == "喜羊羊":
        collar_color = (
            (220, 80, 80)
            if skin.get("avatar") == "wolf"
            else (130, 220, 150)
        )
    elif group == "猪猪侠":
        collar_color = (230, 80, 70)
    elif group == "奥特曼":
        collar_color = (220, 70, 70)
    else:
        collar_color = skin.get("accent", (255, 255, 255))

    collar_h = max(3, int(r * 0.10))
    collar_rect = pygame.Rect(
        cx - int(r * 0.58),
        cy + r + 2,
        int(r * 1.16),
        collar_h,
    )
    pygame.draw.rect(
        surface,
        collar_color,
        collar_rect,
        border_radius=max(1, collar_h // 2),
    )
    pygame.draw.circle(
        surface,
        (18, 30, 40),
        (cx, collar_rect.centery),
        max(2, int(r * 0.06)),
    )
    pygame.draw.circle(
        surface,
        (255, 255, 255),
        (cx, collar_rect.centery),
        max(1, int(r * 0.04)),
    )
    shine = (math.sin(now * 2.1 + phase) + 1.0) * 0.5
    shine_x = cx - int(r * 0.35) + int(shine * r * 0.70)
    pygame.draw.circle(
        surface,
        (255, 255, 255),
        (shine_x, collar_rect.centery),
        max(1, int(r * 0.03)),
    )
    if show_badge:
        badge_r = max(9, int(r * 0.34))
        badge_x = cx + int(r * 0.72)
        badge_y = cy + int(r * 0.72)
        pygame.draw.circle(surface, (9, 18, 27), (badge_x, badge_y), badge_r + 2)
        pygame.draw.circle(
            surface,
            ring_light,
            (badge_x, badge_y),
            badge_r + 2,
            1,
        )
        pygame.draw.circle(surface, (18, 32, 45), (badge_x, badge_y), badge_r)
        font = get_font(max(10, int(badge_r * 1.25)), bold=True)
        label = skin["name"][0]
        label_surface = font.render(label, True, (255, 255, 255))
        label_rect = label_surface.get_rect(center=(badge_x, badge_y))
        surface.blit(label_surface, label_rect)


def build_menu_background():
    surface = pygame.Surface((WIDTH, HEIGHT))
    for y in range(HEIGHT):
        ratio = y / max(1, HEIGHT - 1)
        color = tuple(
            int(BG_TOP[index] * (1 - ratio) + BG_BOTTOM[index] * ratio)
            for index in range(3)
        )
        pygame.draw.line(surface, color, (0, y), (WIDTH, y))

    decoration = pygame.Surface((WIDTH, HEIGHT), pygame.SRCALPHA)
    pygame.draw.circle(decoration, (56, 151, 139, 38), (90, 110), 150)
    pygame.draw.circle(decoration, (81, 117, 188, 32), (730, 90), 180)
    pygame.draw.circle(decoration, (48, 197, 151, 22), (680, 520), 210)
    surface.blit(decoration, (0, 0))
    return surface


MENU_BACKGROUND = build_menu_background()


def draw_menu_background():
    SCREEN.blit(MENU_BACKGROUND, (0, 0))


def draw_snake_art(center, skin, length=13, spacing=18, radius=12, amplitude=16):
    render_scale = 4
    body_radius = max(4, int(radius * render_scale))
    span = max(1, int(spacing * (length - 1) * render_scale))
    horizontal_padding = body_radius * 3
    preview_width = span + horizontal_padding * 2
    preview_height = max(
        body_radius * 5,
        int(amplitude * render_scale * 2 + body_radius * 4),
    )
    preview = pygame.Surface((preview_width, preview_height), pygame.SRCALPHA)

    sample_count = max(48, length * 10)
    points = []
    for index in range(sample_count):
        ratio = index / (sample_count - 1)
        x = horizontal_padding + ratio * span
        y = (
            preview_height / 2
            + math.sin(ratio * math.pi * 2.15) * amplitude * render_scale
        )
        points.append((int(x), int(y)))

    for index, point in enumerate(points):
        ratio = index / (sample_count - 1)
        body_color = mix_color(skin["body_dark"], skin["body"], ratio)
        pygame.draw.circle(
            preview,
            skin["outline"],
            point,
            body_radius + 3 * render_scale,
        )
        pygame.draw.circle(preview, body_color, point, body_radius)

    for index, (x, y) in enumerate(points):
        if index % 5 != 0:
            continue
        ratio = index / (sample_count - 1)
        highlight_color = mix_color(
            skin["body"],
            skin["highlight"],
            0.55 + ratio * 0.25,
        )
        pygame.draw.circle(
            preview,
            highlight_color,
            (x, int(y - body_radius * 0.28)),
            max(2, body_radius // 5),
        )

    head_x, head_y = points[-1]
    draw_avatar(
        preview,
        (head_x + body_radius * 0.2, head_y),
        body_radius * 1.25,
        skin,
    )

    target_size = (
        max(1, preview_width // render_scale),
        max(1, preview_height // render_scale),
    )
    preview = pygame.transform.smoothscale(preview, target_size)
    shadow = pygame.Surface(target_size, pygame.SRCALPHA)
    pygame.draw.ellipse(
        shadow,
        (4, 15, 22, 58),
        (target_size[0] // 8, target_size[1] - 10, target_size[0] * 3 // 4, 8),
    )
    preview_rect = preview.get_rect(center=center)
    SCREEN.blit(shadow, preview_rect)
    SCREEN.blit(preview, preview_rect)


class SnakeGame:
    def __init__(self, skin, difficulty):
        self.mode = "classic"
        self.skin = skin
        self.difficulty = difficulty
        self.cols = GRID_COLS
        self.rows = GRID_ROWS
        self.cell_w = CELL_WIDTH
        self.cell_h = CELL_HEIGHT
        self.world_w = self.cols * self.cell_w
        self.world_h = self.rows * self.cell_h
        self.food_target = FOOD_TARGET
        self.food_cap = self.food_target + 8
        self.score = 0
        self.food_eaten = 0
        self.small_deaths = 0
        self.last_clear_event = -CLEAR_COOLDOWN_MS
        self.foods = []
        self.small_snakes = []
        self.respawn_at = []
        self.dead_reason = ""
        self.notice_message = ""
        self.notice_started_at = 0
        self.notice_duration = 0
        self.notice_color = ACCENT
        self.paused = False
        self.pause_resume_rect = None
        self.pause_exit_rect = None
        self.prev_bodies = {}
        self.render_t = 1.0

        start_row = self.rows // 2
        start_col = self.cols // 2
        body = [Point(col=start_col + index, row=start_row) for index in range(5)]
        self.player = Snake(body, "left", skin, PLAYER_START_THICKNESS, True)
        self.next_direction = "left"
        self.last_move = pygame.time.get_ticks()
        head = self.player.head
        self.cam_x = (head.col + 0.5) * self.cell_w
        self.cam_y = (head.row + 0.5) * self.cell_h

        for _ in range(difficulty["small_snakes"]):
            self.spawn_small_snake(initial=True)
        self.spawn_food(self.food_target)
        self.show_notice(
            "右上圆盘控制方向 · 撞到方形边界墙会死",
            ACCENT,
            3000,
        )

    @property
    def snake(self):
        return self.player.body

    @property
    def head(self):
        return self.player.head

    @property
    def direction(self):
        return self.player.direction

    def all_snakes(self):
        return [self.player] + self.small_snakes

    def leader_snake(self):
        return max(
            self.all_snakes(),
            key=lambda snake: (snake.thickness, len(snake.body)),
        )

    def show_notice(self, message, color=ACCENT, duration=1800):
        self.notice_message = message
        self.notice_color = color
        self.notice_started_at = pygame.time.get_ticks()
        self.notice_duration = duration

    def set_paused(self, paused):
        if self.paused == paused:
            return
        self.paused = paused
        if not paused:
            self.last_move = pygame.time.get_ticks()

    def cell_is_free(self, col, row):
        for snake in self.all_snakes():
            for part in snake.body:
                if part.col == col and part.row == row:
                    return False
        for food in self.foods:
            if food.col == col and food.row == row:
                return False
        return True

    def spawn_food(self, amount=1, near=None, min_radius=6.0, max_radius=12.0):
        if len(self.foods) >= self.food_target + 8:
            return
        for _ in range(amount):
            for _attempt in range(500):
                if near is not None:
                    angle = random.uniform(0.0, math.tau)
                    radius = random.uniform(min_radius, max_radius)
                    col = int(round(near.col + math.cos(angle) * radius))
                    row = int(round(near.row + math.sin(angle) * radius))
                else:
                    col = random.randrange(self.cols)
                    row = random.randrange(self.rows)
                if not (0 <= col < self.cols and 0 <= row < self.rows):
                    continue
                if not self.cell_is_free(col, row):
                    continue
                if grid_distance(Point(col, row), self.player.head) < 4:
                    continue
                self.foods.append(Point(col=col, row=row))
                break

    def spawn_small_snake(self, initial=False, thickness=SMALL_START_THICKNESS):
        palettes = [skin for skin in ALL_SKINS if skin is not self.skin] or ALL_SKINS
        for _attempt in range(400):
            direction = random.choice(list(DIRECTION_STEPS))
            step_col, step_row = DIRECTION_STEPS[direction]
            head_col = random.randrange(self.cols)
            head_row = random.randrange(self.rows)
            body = []
            valid = True
            length = random.randint(4, 6)
            for index in range(length):
                col = head_col - step_col * index
                row = head_row - step_row * index
                if not (0 <= col < self.cols and 0 <= row < self.rows):
                    valid = False
                    break
                if not self.cell_is_free(col, row):
                    valid = False
                    break
                body.append(Point(col=col, row=row))
            if not valid:
                continue
            distance = grid_distance(body[0], self.player.head)
            if distance < 6 or (initial and distance < 14):
                continue
            self.small_snakes.append(
                Snake(body, direction, random.choice(palettes), thickness)
            )
            return True
        return False

    def nearest_food(self, point):
        best = None
        best_distance = 10 ** 9
        for food in self.foods:
            distance = grid_distance(point, food)
            if distance < best_distance:
                best_distance = distance
                best = food
        return best

    def choose_ai_direction(self, snake):
        head = snake.head
        target = self.nearest_food(head)

        danger = set()
        heads = []
        for other in self.all_snakes():
            if other is snake or same_team(snake, other):
                continue
            for part in other.body:
                danger.add((part.row, part.col))
            heads.append(other.head)

        options = []
        for direction, (step_col, step_row) in DIRECTION_STEPS.items():
            if direction == OPPOSITE[snake.direction]:
                continue
            col = head.col + step_col
            row = head.row + step_row
            score = random.random() * 0.35
            if not (0 <= col < self.cols and 0 <= row < self.rows):
                score += 1000
                options.append((score, direction))
                continue
            if (row, col) in danger:
                score += 80
            if step_col and step_row:
                side_a = (head.row, head.col + step_col)
                side_b = (head.row + step_row, head.col)
                if side_a in danger or side_b in danger:
                    score += 80
            if target is not None:
                score += grid_distance(Point(col, row), target)
            for other_head in heads:
                if other_head is head:
                    continue
                if grid_distance(Point(col, row), other_head) <= 1:
                    score += 45
            if direction == snake.direction:
                score -= 0.4
            options.append((score, direction))

        if not options:
            return snake.direction
        options.sort(key=lambda item: item[0])
        return options[0][1]

    def turn(self, direction):
        if self.next_direction != self.direction:
            return
        if direction != OPPOSITE[self.direction]:
            self.next_direction = direction

    def update(self):
        now = pygame.time.get_ticks()
        while self.respawn_at and now >= self.respawn_at[0]:
            self.respawn_at.pop(0)
            if len(self.small_snakes) < self.difficulty["small_snakes"]:
                self.spawn_small_snake()

        self.player.direction = self.next_direction
        snakes = self.all_snakes()
        self.prev_bodies = {
            snake: [part.copy() for part in snake.body]
            for snake in snakes
        }

        decisions = {}
        for snake in snakes:
            if snake.is_player:
                decisions[snake] = self.player.direction
            else:
                decisions[snake] = self.choose_ai_direction(snake)

        new_heads = {}
        eating = {}
        for snake in snakes:
            direction = decisions[snake]
            snake.direction = direction
            step_col, step_row = DIRECTION_STEPS[direction]
            head = snake.head
            new_head = Point(
                col=head.col + step_col,
                row=head.row + step_row,
            )
            new_heads[snake] = new_head
            in_bounds = (
                0 <= new_head.col < self.cols
                and 0 <= new_head.row < self.rows
            )
            eating[snake] = in_bounds and any(
                food.col == new_head.col and food.row == new_head.row
                for food in self.foods
            )

        after_cells = {}
        for snake in snakes:
            cells = {(part.row, part.col) for part in snake.body}
            if not eating[snake]:
                tail = snake.body[-1]
                cells.discard((tail.row, tail.col))
            after_cells[snake] = cells

        deaths = {}
        for snake in snakes:
            new_head = new_heads[snake]
            if not (
                0 <= new_head.col < self.cols
                and 0 <= new_head.row < self.rows
            ):
                deaths[snake] = "撞到了边界墙！"
                continue
            cell = (new_head.row, new_head.col)
            for other in snakes:
                if other is snake:
                    continue
                if cell in after_cells[other]:
                    if other.is_player:
                        deaths[snake] = "撞到了大蛇的身体！"
                    else:
                        deaths[snake] = "撞到了小蛇的身体！"
                    break

        target_cells = {}
        for snake in snakes:
            cell = (new_heads[snake].row, new_heads[snake].col)
            target_cells.setdefault(cell, []).append(snake)
        for group in target_cells.values():
            if len(group) > 1:
                for snake in group:
                    deaths.setdefault(snake, "和另一条蛇撞头了！")

        if self.player in deaths:
            self.dead_reason = deaths[self.player]
            return self.dead_reason

        for snake in snakes:
            if snake in deaths:
                continue
            snake.body.insert(0, new_heads[snake])
            if not eating[snake]:
                snake.body.pop()

        for snake in snakes:
            if snake in deaths:
                if not snake.is_player:
                    self.handle_small_death(snake, now)
                continue
            if eating[snake]:
                self.consume_food(snake, new_heads[snake])

        return ""

    def handle_small_death(self, snake, now):
        if snake in self.small_snakes:
            self.small_snakes.remove(snake)
        self.small_deaths += 1
        play_sound(SNAKE_DOWN_SOUND)
        for index, part in enumerate(snake.body):
            if index % 2:
                continue
            if len(self.foods) >= self.food_target + 12:
                break
            if self.cell_is_free(part.col, part.row):
                self.foods.append(part.copy())
        self.respawn_at.append(now + self.difficulty["respawn"])
        if len(self.foods) > self.food_target + 2:
            self.show_notice("一条小蛇倒下，身体变成了食物", (255, 156, 120), 1700)

    def consume_food(self, snake, cell):
        for index, food in enumerate(self.foods):
            if food.col == cell.col and food.row == cell.row:
                del self.foods[index]
                break

        snake.eaten += 1
        refilled_locally = False
        if snake.is_player:
            self.food_eaten += 1
            self.score += 10
            snake.thickness = min(MAX_THICKNESS, snake.thickness + 0.55)
            for small in self.small_snakes:
                small.thickness = max(MIN_THICKNESS, small.thickness - 0.16)
            play_sound(EAT_SOUND)
            nearby = any(
                grid_distance(food, self.head) <= CLEAR_RADIUS
                for food in self.foods
            )
            if nearby:
                self.show_notice("吃到食物：身体变长变粗，小蛇被压瘦", (82, 213, 160), 1500)
            else:
                self.handle_local_clear()
                refilled_locally = True
        else:
            snake.thickness = min(MAX_THICKNESS, snake.thickness + 0.62)
            if random.random() < 0.25:
                self.show_notice("小蛇抢到了一颗食物，正在长大", (120, 190, 255), 1100)

        if not refilled_locally:
            self.spawn_food(1)

    def handle_local_clear(self):
        if not self.foods:
            self.spawn_food(12)
            self.spawn_food(
                4,
                near=self.head,
                min_radius=6.0,
                max_radius=11.0,
            )
            for _ in range(2):
                self.spawn_small_snake(thickness=REINFORCEMENT_THICKNESS)
            self.score += FULL_CLEAR_SCORE
            self.show_notice(
                "全场食物清空：蛇群增援，食物重新铺满",
                (255, 96, 96),
                3000,
            )
            return

        self.spawn_food(3, near=self.head, min_radius=6.0, max_radius=11.0)
        now = pygame.time.get_ticks()
        can_reinforce = (
            now - self.last_clear_event >= CLEAR_COOLDOWN_MS
            and len(self.small_snakes)
            < self.difficulty["small_snakes"] + MAX_EXTRA_SNAKES
        )
        if can_reinforce and self.spawn_small_snake(
            thickness=REINFORCEMENT_THICKNESS
        ):
            self.last_clear_event = now
            self.score += CLEAR_SCORE
            self.show_notice(
                "周围食物清空：一条新的小蛇被引来",
                (255, 140, 110),
                2200,
            )
            return
        self.show_notice(
            "周围食物吃完了，附近又长出一批",
            (255, 196, 67),
            1900,
        )

    def head_world(self):
        head = self.player.head
        return (
            (head.col + 0.5) * self.cell_w,
            (head.row + 0.5) * self.cell_h,
        )

    def interpolated_head_world(self, t):
        head = self.player.head
        previous = self.prev_bodies.get(self.player)
        if previous:
            old = previous[0]
            col = old.col + (head.col - old.col) * t
            row = old.row + (head.row - old.row) * t
        else:
            col = head.col
            row = head.row
        return (
            (col + 0.5) * self.cell_w,
            (row + 0.5) * self.cell_h,
        )

    def body_centers(self, snake, t):
        previous = self.prev_bodies.get(snake)
        centers = []
        for index, part in enumerate(snake.body):
            if previous is not None and index < len(previous):
                old = previous[index]
            else:
                old = part
            col = old.col + (part.col - old.col) * t
            row = old.row + (part.row - old.row) * t
            centers.append(
                self.to_screen(
                    (col + 0.5) * self.cell_w,
                    (row + 0.5) * self.cell_h,
                )
            )
        return centers

    def to_screen(self, x, y):
        return (
            int(VIEW_CENTER_X + x - self.cam_x),
            int(VIEW_CENTER_Y + y - self.cam_y),
        )

    def cell_screen(self, part):
        return self.to_screen(
            (part.col + 0.5) * self.cell_w,
            (part.row + 0.5) * self.cell_h,
        )

    def draw_line(self, color, start, end, width):
        pygame.draw.line(SCREEN, color, start, end, width)

    def draw_circle(self, color, center, radius):
        pygame.draw.circle(SCREEN, color, center, radius)

    def draw_head(self, snake, center, thickness):
        radius = max(8, int(round(thickness)))
        draw_avatar(SCREEN, center, radius, snake.skin)
    def draw_snake(self, snake):
        thickness = max(4, int(round(snake.thickness)))
        centers = self.body_centers(snake, self.render_t)

        for index in range(len(centers) - 1):
            self.draw_line(
                snake.skin["outline"],
                centers[index],
                centers[index + 1],
                thickness + 4,
            )
        for index in range(len(centers) - 1):
            self.draw_line(
                mix_color(snake.skin["body_dark"], snake.skin["body"], 0.7),
                centers[index],
                centers[index + 1],
                thickness,
            )

        radius = max(3, thickness // 2)
        for index, center in enumerate(centers[1:]):
            band = (index % 4) / 3
            body_color = mix_color(
                snake.skin["body_dark"],
                snake.skin["body"],
                0.55 + band * 0.45,
            )
            self.draw_circle(body_color, center, radius)
            highlight_center = (
                center[0] - max(1, radius // 3),
                center[1] - max(1, radius // 3),
            )
            self.draw_circle(
                snake.skin["highlight"],
                highlight_center,
                max(1, radius // 4),
            )

        pattern = snake.skin.get("pattern")
        if pattern == "stripes":
            for index, center in enumerate(centers[1:]):
                if index % 3 == 0:
                    self.draw_circle(
                        snake.skin["body_dark"],
                        center,
                        max(2, radius // 2),
                    )
        elif pattern == "spots":
            for index, center in enumerate(centers[1:]):
                if index % 4 == 2:
                    self.draw_circle(
                        snake.skin["body_dark"],
                        (
                            center[0] + radius // 3,
                            center[1] - radius // 3,
                        ),
                        max(1, radius // 4),
                    )

        tail = centers[-1]
        self.draw_circle(snake.skin["outline"], tail, radius + 2)
        self.draw_circle(
            mix_color(snake.skin["body_dark"], snake.skin["body"], 0.35),
            tail,
            radius,
        )

        self.draw_head(snake, centers[0], thickness)

        if snake.is_player:
            font = get_font(13, bold=True)
            label_surface = font.render(snake.name, True, (255, 255, 255))
            shadow_surface = font.render(snake.name, True, (8, 16, 22))
            label_x = centers[0][0] - label_surface.get_width() // 2
            label_y = centers[0][1] - thickness - 16
            SCREEN.blit(shadow_surface, (label_x + 1, label_y + 1))
            SCREEN.blit(label_surface, (label_x, label_y))

    def draw_grid(self, world_rect):
        left = max(0, world_rect.left)
        right = min(WIDTH, world_rect.right)
        top = max(BOARD_TOP, world_rect.top)
        bottom = min(HEIGHT, world_rect.bottom)
        if left >= right or top >= bottom:
            return
        for col in range(0, self.cols, 4):
            screen_x = world_rect.left + int(col * self.cell_w)
            if left <= screen_x <= right:
                pygame.draw.line(
                    SCREEN,
                    GRID_COLOR,
                    (screen_x, top),
                    (screen_x, bottom),
                    1,
                )
        for row in range(0, self.rows, 4):
            screen_y = world_rect.top + int(row * self.cell_h)
            if top <= screen_y <= bottom:
                pygame.draw.line(
                    SCREEN,
                    GRID_COLOR,
                    (left, screen_y),
                    (right, screen_y),
                    1,
                )

    def draw_food(self):
        now = pygame.time.get_ticks()
        for index, food in enumerate(self.foods):
            center = self.cell_screen(food)
            pulse = 1.0 + 0.10 * math.sin(now / 260.0 + index * 1.7)
            glow_radius = max(4, int(8 * pulse))
            self.draw_circle((255, 224, 138), center, glow_radius)
            self.draw_circle((126, 78, 14), center, max(3, int(6 * pulse)))
            self.draw_circle(FOOD_COLOR, center, max(2, int(5 * pulse)))

    def update_pointer(self, mouse_pos):
        delta_x = mouse_pos[0] - JOYSTICK_CENTER[0]
        delta_y = mouse_pos[1] - JOYSTICK_CENTER[1]
        if delta_x * delta_x + delta_y * delta_y > JOYSTICK_RADIUS ** 2:
            return
        if abs(delta_x) < JOYSTICK_DEADZONE and abs(delta_y) < JOYSTICK_DEADZONE:
            return
        angle = math.atan2(delta_y, delta_x)
        sector = int(round(angle / (math.pi / 4))) % 8
        directions = (
            "right",
            "down-right",
            "down",
            "down-left",
            "left",
            "up-left",
            "up",
            "up-right",
        )
        self.turn(directions[sector])

    def draw_joystick(self):
        mouse_pos = pygame.mouse.get_pos()
        delta_x = mouse_pos[0] - JOYSTICK_CENTER[0]
        delta_y = mouse_pos[1] - JOYSTICK_CENTER[1]
        distance = math.hypot(delta_x, delta_y)

        diameter = JOYSTICK_RADIUS * 2
        surface = pygame.Surface((diameter, diameter), pygame.SRCALPHA)
        center = (JOYSTICK_RADIUS, JOYSTICK_RADIUS)
        pygame.draw.circle(surface, (4, 12, 18, 64), center, JOYSTICK_RADIUS)
        pygame.draw.circle(
            surface,
            (255, 255, 255, 40),
            center,
            JOYSTICK_RADIUS,
            2,
        )
        pygame.draw.circle(
            surface,
            (255, 255, 255, 24),
            center,
            JOYSTICK_RADIUS - 26,
            1,
        )
        if distance <= JOYSTICK_RADIUS:
            knob = (
                int(center[0] + delta_x),
                int(center[1] + delta_y),
            )
            pygame.draw.line(
                surface,
                (210, 236, 236, 80),
                center,
                knob,
                2,
            )
            pygame.draw.circle(surface, (232, 244, 244, 150), knob, 9)
            pygame.draw.circle(surface, (20, 36, 44, 120), knob, 4)
        SCREEN.blit(
            surface,
            (
                int(JOYSTICK_CENTER[0] - JOYSTICK_RADIUS),
                int(JOYSTICK_CENTER[1] - JOYSTICK_RADIUS),
            ),
        )

    def draw_radar(self):
        rect = RADAR_RECT
        panel = pygame.Surface((rect.w, rect.h), pygame.SRCALPHA)
        panel.fill((8, 20, 28, 190))
        pygame.draw.rect(
            panel,
            (92, 170, 192, 235),
            panel.get_rect(),
            2,
        )
        for step in range(1, 4):
            x = rect.w * step // 4
            y = rect.h * step // 4
            pygame.draw.line(
                panel,
                (64, 104, 124, 90),
                (x, 0),
                (x, rect.h),
                1,
            )
            pygame.draw.line(
                panel,
                (64, 104, 124, 90),
                (0, y),
                (rect.w, y),
                1,
            )
        SCREEN.blit(panel, rect.topleft)

        for snake in self.small_snakes:
            head = snake.head
            dot_x = rect.x + (head.col + 0.5) / self.cols * rect.w
            dot_y = rect.y + (head.row + 0.5) / self.rows * rect.h
            pygame.draw.circle(
                SCREEN,
                (238, 78, 78),
                (int(dot_x), int(dot_y)),
                3,
            )

        head = self.player.head
        dot_x = rect.x + (head.col + 0.5) / self.cols * rect.w
        dot_y = rect.y + (head.row + 0.5) / self.rows * rect.h
        pygame.draw.circle(SCREEN, (250, 255, 250), (int(dot_x), int(dot_y)), 5)
        pygame.draw.circle(SCREEN, (56, 232, 118), (int(dot_x), int(dot_y)), 3)

        leader = self.leader_snake()
        leader_head = leader.head
        leader_x = rect.x + (leader_head.col + 0.5) / self.cols * rect.w
        leader_y = rect.y + (leader_head.row + 0.5) / self.rows * rect.h
        pygame.draw.circle(
            SCREEN,
            (255, 204, 64),
            (int(leader_x), int(leader_y)),
            6,
            1,
        )
        crown_y = (
            leader_y - 11
            if leader_y - 11 > rect.y + 6
            else leader_y + 11
        )
        self.draw_crown(leader_x, crown_y)

    def draw_crown(self, center_x, center_y):
        cx = int(center_x)
        cy = int(center_y)
        points = [
            (cx - 6, cy + 3),
            (cx - 6, cy - 4),
            (cx - 3, cy - 1),
            (cx, cy - 6),
            (cx + 3, cy - 1),
            (cx + 6, cy - 4),
            (cx + 6, cy + 3),
        ]
        pygame.draw.polygon(SCREEN, (255, 204, 64), points)
        pygame.draw.lines(SCREEN, (92, 62, 10), True, points, 1)
        pygame.draw.line(
            SCREEN,
            (92, 62, 10),
            (cx - 6, cy + 4),
            (cx + 6, cy + 4),
            2,
        )

    def draw(self):
        interval = max(1, self.difficulty["interval"])
        elapsed = pygame.time.get_ticks() - self.last_move
        self.render_t = (
            1.0
            if self.paused
            else max(0.0, min(1.0, elapsed / interval))
        )
        self.cam_x, self.cam_y = self.interpolated_head_world(self.render_t)
        SCREEN.fill((10, 18, 26))
        world_rect = pygame.Rect(
            int(VIEW_CENTER_X - self.cam_x),
            int(VIEW_CENTER_Y - self.cam_y),
            int(self.world_w),
            int(self.world_h),
        )
        pygame.draw.rect(SCREEN, BOARD_COLOR, world_rect)
        self.draw_grid(world_rect)
        self.draw_joystick()
        self.draw_food()
        for snake in self.small_snakes:
            self.draw_snake(snake)
        self.draw_snake(self.player)
        pygame.draw.rect(SCREEN, (56, 72, 86), world_rect, 4)
        pygame.draw.rect(SCREEN, (120, 150, 165), world_rect.inflate(-8, -8), 1)
        self.draw_radar()
        self.draw_notice()
        if self.paused:
            self.draw_paused_overlay()
        self.draw_hud()

    def draw_notice(self):
        if not self.notice_message:
            return

        elapsed = pygame.time.get_ticks() - self.notice_started_at
        if elapsed >= self.notice_duration:
            return

        remaining = max(0.0, 1.0 - elapsed / self.notice_duration)
        fade = remaining ** 1.35
        text_alpha = int(245 * fade)
        box_alpha = int(68 * fade)
        if text_alpha <= 0:
            return

        font = get_font(22, bold=True)
        text_surface = font.render(self.notice_message, True, (250, 253, 250))
        text_surface.set_alpha(text_alpha)
        shadow_surface = font.render(self.notice_message, True, (8, 16, 20))
        shadow_surface.set_alpha(int(text_alpha * 0.65))

        box_width = text_surface.get_width() + 42
        box_height = text_surface.get_height() + 20
        box = pygame.Surface((box_width, box_height), pygame.SRCALPHA)
        pygame.draw.rect(
            box,
            (15, 29, 38, box_alpha),
            box.get_rect(),
            border_radius=14,
        )
        pygame.draw.rect(
            box,
            (*self.notice_color, min(160, text_alpha)),
            box.get_rect(),
            2,
            border_radius=14,
        )

        center = (WIDTH // 2, HEIGHT - 48)
        box_rect = box.get_rect(center=center)
        SCREEN.blit(box, box_rect)
        text_rect = text_surface.get_rect(center=center)
        SCREEN.blit(shadow_surface, text_rect.move(2, 2))
        SCREEN.blit(text_surface, text_rect)

    def draw_paused_overlay(self):
        overlay = pygame.Surface((WIDTH, BOARD_HEIGHT), pygame.SRCALPHA)
        overlay.fill((8, 18, 27, 150))
        SCREEN.blit(overlay, (0, BOARD_TOP))

        panel = pygame.Rect(
            WIDTH // 2 - 270,
            BOARD_TOP + BOARD_HEIGHT // 2 - 120,
            540,
            240,
        )
        pygame.draw.rect(SCREEN, (20, 36, 50), panel, border_radius=22)
        pygame.draw.rect(SCREEN, (87, 194, 164), panel, 2, border_radius=22)
        draw_text(
            "游戏已暂停",
            36,
            TEXT_COLOR,
            (panel.centerx, panel.y + 50),
            bold=True,
        )
        draw_text(
            "按 P / 空格继续，ESC 退出本局",
            17,
            MUTED_TEXT,
            (panel.centerx, panel.y + 92),
        )

        resume_rect = pygame.Rect(panel.centerx - 220, panel.y + 124, 200, 56)
        exit_rect = pygame.Rect(panel.centerx + 20, panel.y + 124, 200, 56)
        mouse_pos = pygame.mouse.get_pos()
        draw_button(
            resume_rect,
            "继续游戏",
            mouse_pos,
            color=ACCENT,
            text_color=(10, 33, 26),
        )
        draw_button(
            exit_rect,
            "退出比赛" if self.mode == "team" else "退出游戏",
            mouse_pos,
            color=(198, 82, 82),
            text_color=(255, 246, 246),
        )
        self.pause_resume_rect = resume_rect
        self.pause_exit_rect = exit_rect

    def draw_hud(self):
        pygame.draw.rect(SCREEN, (18, 31, 42), (0, 0, WIDTH, HUD_HEIGHT))
        pygame.draw.line(
            SCREEN,
            (104, 133, 147),
            (0, HUD_HEIGHT - 1),
            (WIDTH, HUD_HEIGHT - 1),
            2,
        )
        draw_left_text(
            f"分数 {self.score}",
            26,
            TEXT_COLOR,
            (20, 8),
            bold=True,
        )
        draw_left_text(
            f"食物 {self.food_eaten}",
            19,
            MUTED_TEXT,
            (20, 37),
        )
        size_level = max(
            1,
            int(round((self.player.thickness - PLAYER_START_THICKNESS) / 0.55)) + 1,
        )
        draw_left_text(
            f"长度 {len(self.player.body)}  ·  体型 {size_level} 级",
            21,
            TEXT_COLOR,
            (210, 18),
            bold=True,
        )
        draw_left_text(
            f"小蛇 {len(self.small_snakes)} 条  ·  已倒下 {self.small_deaths} 条",
            20,
            (150, 210, 235),
            (468, 18),
            bold=True,
        )
        draw_left_text(
            f"皮肤 {self.skin['name']}  ·  难度 {self.difficulty['name']}",
            17,
            self.difficulty["color"],
            (212, 40),
            bold=True,
        )
        mouse_pos = pygame.mouse.get_pos()
        draw_hud_button(
            PAUSE_BUTTON_RECT,
            "暂停游戏",
            mouse_pos,
            enabled=not self.paused,
            color=(227, 166, 58),
        )
        draw_hud_button(
            RESUME_BUTTON_RECT,
            "继续游戏",
            mouse_pos,
            enabled=self.paused,
            color=ACCENT,
        )


class TeamGame(SnakeGame):
    def __init__(self, player_team_index, player_skin_index):
        self.mode = "team"
        self.player_team_index = player_team_index
        self.team = TEAMS[player_team_index]
        self.skin = self.team["skins"][player_skin_index]
        self.player_skin = self.skin
        self.difficulty = dict(DIFFICULTIES[1])
        self.difficulty["interval"] = TEAM_INTERVAL_MS
        self.cols = TEAM_COLS
        self.rows = TEAM_ROWS
        self.cell_w = 16.0
        self.cell_h = 16.0
        self.world_w = self.cols * self.cell_w
        self.world_h = self.rows * self.cell_h
        self.food_target = TEAM_FOOD_TARGET
        self.food_cap = TEAM_FOOD_TARGET + 30
        self.score = 0
        self.food_eaten = 0
        self.small_deaths = 0
        self.dead_reason = ""
        self.notice_message = ""
        self.notice_started_at = 0
        self.notice_duration = 0
        self.notice_color = ACCENT
        self.paused = False
        self.pause_resume_rect = None
        self.pause_exit_rect = None
        self.prev_bodies = {}
        self.render_t = 1.0
        self.snakes = []
        self.player = None
        self.next_direction = "left"
        self.last_move = pygame.time.get_ticks()
        self.foods = []
        self.respawn_queue = []
        self.team_scores = [0 for _ in TEAMS]
        self.member_scores = {}
        self.team_kills = [0 for _ in TEAMS]
        self.match_started_at = pygame.time.get_ticks()
        self.match_end_at = self.match_started_at + TEAM_MATCH_MS
        self.paused_remaining = TEAM_MATCH_MS
        self.match_over = False
        self.results = None
        self.camera_world = (
            self.cols * self.cell_w / 2,
            self.rows * self.cell_h / 2,
        )
        self.cam_x, self.cam_y = self.camera_world
        self._spawn_all_teams()
        self.spawn_food(self.food_target)
        self.show_notice(
            "5 队团队赛开始 · 5 分钟积分赛 · 撞到别的蛇会死",
            team_ui_color(self.team),
            3600,
        )

    @property
    def snake(self):
        return self.player.body if self.player is not None else []

    @property
    def head(self):
        return self.player.head if self.player is not None else None

    @property
    def direction(self):
        return self.player.direction if self.player is not None else self.next_direction

    def all_snakes(self):
        return [snake for snake in self.snakes if snake.alive]

    def team_rank(self):
        order = sorted(
            range(len(TEAMS)),
            key=lambda index: (-self.team_scores[index], index),
        )
        return order.index(self.player_team_index) + 1

    def time_left_ms(self):
        if self.match_over:
            return 0
        if self.paused:
            return max(0, self.paused_remaining)
        return max(0, self.match_end_at - pygame.time.get_ticks())

    def set_paused(self, paused):
        if self.match_over or self.paused == paused:
            return
        now = pygame.time.get_ticks()
        if paused:
            self.paused_remaining = max(0, self.match_end_at - now)
            self.paused = True
        else:
            self.paused = False
            self.match_end_at = now + self.paused_remaining
            self.last_move = now

    def add_score(self, snake, points):
        snake.score += points
        self.team_scores[snake.team_id] += points
        key = (snake.team_id, snake.name)
        self.member_scores[key] = self.member_scores.get(key, 0) + points

    def _team_member_skins(self, team_index):
        skins = list(TEAMS[team_index]["skins"])
        if team_index == self.player_team_index:
            chosen = self.skin
            others = [skin for skin in skins if skin is not chosen]
            random.shuffle(others)
            return [chosen] + others[:TEAM_MEMBERS - 1]
        random.shuffle(skins)
        return skins[:TEAM_MEMBERS]

    def _spawn_all_teams(self):
        for team_index in range(len(TEAMS)):
            for skin in self._team_member_skins(team_index):
                is_player = (
                    team_index == self.player_team_index
                    and skin is self.skin
                )
                self.spawn_team_snake(team_index, skin, is_player=is_player)

    def spawn_team_snake(self, team_index, skin, is_player=False, name=None):
        team = TEAMS[team_index]
        display_skin = team_skin(skin, team)
        display_name = name or skin["name"]
        for _attempt in range(900):
            direction = random.choice(list(DIRECTION_STEPS))
            step_col, step_row = DIRECTION_STEPS[direction]
            head_col = random.randrange(2, self.cols - 2)
            head_row = random.randrange(2, self.rows - 2)
            body = []
            valid = True
            for index in range(5):
                col = head_col - step_col * index
                row = head_row - step_row * index
                if not (0 <= col < self.cols and 0 <= row < self.rows):
                    valid = False
                    break
                if not self.cell_is_free(col, row):
                    valid = False
                    break
                body.append(Point(col=col, row=row))
            if not valid:
                continue
            too_close = False
            for other in self.all_snakes():
                if grid_distance(body[0], other.head) < 7:
                    too_close = True
                    break
            if too_close:
                continue
            snake = Snake(
                body,
                direction,
                display_skin,
                7.5,
                is_player,
                team_id=team_index,
                name=display_name,
            )
            snake.base_skin = skin
            self.snakes.append(snake)
            self.member_scores.setdefault((team_index, display_name), 0)
            if is_player:
                self.player = snake
                self.next_direction = direction
                self.cam_x = (snake.head.col + 0.5) * self.cell_w
                self.cam_y = (snake.head.row + 0.5) * self.cell_h
                self.camera_world = (self.cam_x, self.cam_y)
            return snake

        if is_player:
            center_col = self.cols // 2
            center_row = self.rows // 2
            body = [
                Point(col=center_col - index, row=center_row)
                for index in range(5)
            ]
            snake = Snake(
                body,
                "right",
                display_skin,
                7.5,
                True,
                team_id=team_index,
                name=display_name,
            )
            snake.base_skin = skin
            self.snakes.append(snake)
            self.member_scores.setdefault((team_index, display_name), 0)
            self.player = snake
            self.next_direction = "right"
            self.cam_x = (snake.head.col + 0.5) * self.cell_w
            self.cam_y = (snake.head.row + 0.5) * self.cell_h
            self.camera_world = (self.cam_x, self.cam_y)
            return snake
        return None

    def spawn_food(self, amount=1, near=None, min_radius=6.0, max_radius=12.0):
        for _ in range(amount):
            if len(self.foods) >= self.food_cap:
                return
            for _attempt in range(900):
                if near is not None:
                    angle = random.uniform(0.0, math.tau)
                    radius = random.uniform(min_radius, max_radius)
                    col = int(round(near.col + math.cos(angle) * radius))
                    row = int(round(near.row + math.sin(angle) * radius))
                else:
                    col = random.randrange(self.cols)
                    row = random.randrange(self.rows)
                if not (0 <= col < self.cols and 0 <= row < self.rows):
                    continue
                if not self.cell_is_free(col, row):
                    continue
                if (
                    self.player is not None
                    and self.player.alive
                    and grid_distance(Point(col, row), self.player.head) < 3
                ):
                    continue
                self.foods.append(Point(col=col, row=row))
                break

    def consume_food(self, snake, cell):
        for index, food in enumerate(self.foods):
            if food.col == cell.col and food.row == cell.row:
                del self.foods[index]
                break
        snake.eaten += 1
        self.add_score(snake, TEAM_FOOD_SCORE)
        snake.thickness = min(MAX_THICKNESS, snake.thickness + 0.45)
        if snake.is_player:
            play_sound(EAT_SOUND)
        missing = self.food_target - len(self.foods)
        if missing > 0:
            self.spawn_food(min(3, missing))

    def handle_team_death(self, snake, reason, now, killer=None):
        if not snake.alive:
            return
        snake.alive = False
        snake.death_reason = reason
        if killer is not None and killer is not snake and killer.alive:
            killer.kills += 1
            self.team_kills[killer.team_id] += 1
            self.add_score(killer, TEAM_KILL_SCORE)
        for index, part in enumerate(snake.body):
            if index % 2:
                continue
            if len(self.foods) >= self.food_cap:
                break
            if self.cell_is_free(part.col, part.row):
                self.foods.append(part.copy())
        self.respawn_queue.append(
            (
                now + TEAM_RESPAWN_MS,
                snake.team_id,
                snake.base_skin,
                snake.is_player,
                snake.name,
            )
        )
        if snake.is_player:
            self.dead_reason = reason
            self.camera_world = (
                (snake.head.col + 0.5) * self.cell_w,
                (snake.head.row + 0.5) * self.cell_h,
            )
            self.show_notice(
                f"你被击倒：{reason} · {TEAM_RESPAWN_MS // 1000} 秒后复活",
                (255, 120, 120),
                2400,
            )
            play_sound(SNAKE_DOWN_SOUND)
        elif killer is not None and killer.is_player:
            self.show_notice(
                f"你击倒了 {snake.name}！",
                (255, 220, 120),
                1600,
            )
            play_sound(SNAKE_DOWN_SOUND)

    def update(self):
        if self.match_over:
            return ""
        now = pygame.time.get_ticks()
        while self.respawn_queue and now >= self.respawn_queue[0][0]:
            _, team_index, skin, is_player, name = self.respawn_queue.pop(0)
            self.spawn_team_snake(
                team_index,
                skin,
                is_player=is_player,
                name=name,
            )

        if self.player is not None and self.player.alive:
            self.player.direction = self.next_direction

        snakes = self.all_snakes()
        if not snakes:
            return ""
        self.prev_bodies = {
            snake: [part.copy() for part in snake.body]
            for snake in snakes
        }

        decisions = {}
        for snake in snakes:
            if snake.is_player:
                decisions[snake] = self.next_direction
            else:
                decisions[snake] = self.choose_ai_direction(snake)

        new_heads = {}
        eating = {}
        for snake in snakes:
            direction = decisions[snake]
            snake.direction = direction
            step_col, step_row = DIRECTION_STEPS[direction]
            head = snake.head
            new_head = Point(
                col=head.col + step_col,
                row=head.row + step_row,
            )
            new_heads[snake] = new_head
            in_bounds = (
                0 <= new_head.col < self.cols
                and 0 <= new_head.row < self.rows
            )
            eating[snake] = in_bounds and any(
                food.col == new_head.col and food.row == new_head.row
                for food in self.foods
            )

        after_cells = {}
        for snake in snakes:
            after_cells[snake] = {
                (part.row, part.col) for part in snake.body
            }

        body_owner = {}
        for snake in snakes:
            for part in snake.body:
                body_owner.setdefault((part.row, part.col), []).append(snake)
        deaths = {}
        for snake in snakes:
            new_head = new_heads[snake]
            if not (
                0 <= new_head.col < self.cols
                and 0 <= new_head.row < self.rows
            ):
                deaths[snake] = ("撞到了边界墙！", None)
                continue
            direction = decisions[snake]
            step_col, step_row = DIRECTION_STEPS[direction]
            if step_col and step_row:
                old_head = snake.head
                side_cells = (
                    (old_head.row, old_head.col + step_col),
                    (old_head.row + step_row, old_head.col),
                )
                for side_cell in side_cells:
                    for other in body_owner.get(side_cell, ()):
                        if other is not snake and not same_team(snake, other):
                            deaths[snake] = ("斜穿过了敌方蛇的身体！", other)
                            break
                    if snake in deaths:
                        break
                if snake in deaths:
                    continue
            cell = (new_head.row, new_head.col)
            for other in snakes:
                if other is snake or same_team(snake, other):
                    continue
                if cell in after_cells[other]:
                    deaths[snake] = ("撞到了其他蛇的身体！", other)
                    break

        target_cells = {}
        for snake in snakes:
            cell = (new_heads[snake].row, new_heads[snake].col)
            target_cells.setdefault(cell, []).append(snake)
        for group in target_cells.values():
            if len(group) > 1:
                for snake in group:
                    has_enemy = any(
                        other is not snake and not same_team(snake, other)
                        for other in group
                    )
                    if has_enemy:
                        deaths.setdefault(snake, ("和另一条蛇撞头了！", None))

        for first_index, first in enumerate(snakes):
            for second in snakes[first_index + 1:]:
                if same_team(first, second):
                    continue
                if segments_cross(
                    first.head,
                    new_heads[first],
                    second.head,
                    new_heads[second],
                ):
                    deaths.setdefault(first, ("和敌方蛇交叉穿过！", second))
                    deaths.setdefault(second, ("和敌方蛇交叉穿过！", first))

        for snake in snakes:
            if snake in deaths:
                continue
            snake.body.insert(0, new_heads[snake])
            if not eating[snake]:
                snake.body.pop()

        body_cells = {}
        for snake in snakes:
            if snake in deaths:
                continue
            for part in snake.body:
                body_cells.setdefault((part.row, part.col), []).append(snake)
        for occupants in body_cells.values():
            if len(occupants) < 2:
                continue
            if len({snake.team_id for snake in occupants}) < 2:
                continue
            for snake in occupants:
                if any(other.team_id != snake.team_id for other in occupants):
                    deaths.setdefault(
                        snake,
                        ("和敌方蛇身体重叠了！", None),
                    )

        for snake in snakes:
            if snake in deaths:
                reason, killer = deaths[snake]
                self.handle_team_death(snake, reason, now, killer)
            elif eating[snake]:
                self.consume_food(snake, new_heads[snake])
        return ""

    def finish_match(self):
        if self.match_over:
            return
        self.match_over = True
        self.paused = False
        totals = list(self.team_scores)
        team_top = []
        for team_index in range(len(TEAMS)):
            members = [
                (name, score)
                for (member_team, name), score in self.member_scores.items()
                if member_team == team_index
            ]
            members.sort(key=lambda item: (-item[1], item[0]))
            team_top.append(members[:3])
        best_total = max(totals) if totals else 0
        tied = [index for index, total in enumerate(totals) if total == best_total]
        winner = max(
            range(len(TEAMS)),
            key=lambda index: (
                totals[index],
                team_top[index][0][1] if team_top[index] else 0,
            ),
        )
        winner_members = [
            (name, score)
            for (member_team, name), score in self.member_scores.items()
            if member_team == winner
        ]
        winner_members.sort(key=lambda item: (-item[1], item[0]))
        self.results = {
            "winner": winner,
            "tied": tied,
            "totals": totals,
            "team_top": team_top,
            "winner_top5": winner_members[:5],
            "team_kills": list(self.team_kills),
        }

    def head_world(self):
        if self.player is not None and self.player.alive:
            head = self.player.head
            return (
                (head.col + 0.5) * self.cell_w,
                (head.row + 0.5) * self.cell_h,
            )
        return self.camera_world

    def interpolated_head_world(self, t):
        if self.player is None or not self.player.alive:
            return self.camera_world
        head = self.player.head
        previous = self.prev_bodies.get(self.player)
        if previous:
            old = previous[0]
            col = old.col + (head.col - old.col) * t
            row = old.row + (head.row - old.row) * t
        else:
            col = head.col
            row = head.row
        return (
            (col + 0.5) * self.cell_w,
            (row + 0.5) * self.cell_h,
        )

    def draw_radar(self):
        rect = RADAR_RECT
        panel = pygame.Surface((rect.w, rect.h), pygame.SRCALPHA)
        panel.fill((8, 20, 28, 200))
        pygame.draw.rect(panel, (92, 170, 192, 235), panel.get_rect(), 2)
        for step in range(1, 4):
            x = rect.w * step // 4
            y = rect.h * step // 4
            pygame.draw.line(panel, (64, 104, 124, 90), (x, 0), (x, rect.h), 1)
            pygame.draw.line(panel, (64, 104, 124, 90), (0, y), (rect.w, y), 1)
        SCREEN.blit(panel, rect.topleft)

        for snake in self.all_snakes():
            head = snake.head
            dot_x = rect.x + (head.col + 0.5) / self.cols * rect.w
            dot_y = rect.y + (head.row + 0.5) / self.rows * rect.h
            color = TEAMS[snake.team_id]["body"]
            pygame.draw.circle(SCREEN, (220, 230, 240), (int(dot_x), int(dot_y)), 4, 1)
            pygame.draw.circle(SCREEN, color, (int(dot_x), int(dot_y)), 3)
            if snake.is_player:
                pygame.draw.circle(
                    SCREEN,
                    (255, 255, 255),
                    (int(dot_x), int(dot_y)),
                    6,
                    1,
                )

        leaders = self.all_snakes()
        if leaders:
            leader = max(
                leaders,
                key=lambda snake: (self.member_scores.get((snake.team_id, snake.name), 0), snake.thickness, len(snake.body)),
            )
            leader_head = leader.head
            leader_x = rect.x + (leader_head.col + 0.5) / self.cols * rect.w
            leader_y = rect.y + (leader_head.row + 0.5) / self.rows * rect.h
            crown_y = (
                leader_y - 11
                if leader_y - 11 > rect.y + 6
                else leader_y + 11
            )
            self.draw_crown(leader_x, crown_y)

    def draw_team_timer(self):
        rect = pygame.Rect(WIDTH // 2 - 48, BOARD_TOP + 10, 96, 96)
        panel = pygame.Surface((rect.w, rect.h), pygame.SRCALPHA)
        panel.fill((8, 18, 28, 212))
        pygame.draw.rect(
            panel,
            team_ui_color(self.team),
            panel.get_rect(),
            3,
            border_radius=16,
        )
        SCREEN.blit(panel, rect.topleft)
        remaining = self.time_left_ms()
        total_seconds = max(0, (remaining + 999) // 1000)
        minutes = total_seconds // 60
        seconds = total_seconds % 60
        draw_text("剩余", 13, MUTED_TEXT, (rect.centerx, rect.y + 17))
        time_color = (255, 120, 120) if remaining <= 30000 else TEXT_COLOR
        draw_text(
            f"{minutes:02d}:{seconds:02d}",
            30,
            time_color,
            (rect.centerx, rect.y + 48),
            bold=True,
        )
        draw_text(
            self.team["short"],
            13,
            team_ui_color(self.team),
            (rect.centerx, rect.y + 77),
            bold=True,
        )

    def draw_team_hud(self):
        pygame.draw.rect(SCREEN, (18, 31, 42), (0, 0, WIDTH, HUD_HEIGHT))
        pygame.draw.line(
            SCREEN,
            (104, 133, 147),
            (0, HUD_HEIGHT - 1),
            (WIDTH, HUD_HEIGHT - 1),
            2,
        )
        player_name = self.player.name if self.player is not None else self.skin["name"]
        player_score = self.member_scores.get(
            (self.player_team_index, player_name),
            0,
        )
        draw_left_text(
            f"{self.team['name']} · {player_name}",
            21,
            TEXT_COLOR,
            (18, 7),
            bold=True,
        )
        draw_left_text(
            f"个人 {player_score} 分  ·  队伍 {self.team_scores[self.player_team_index]} 分  ·  第 {self.team_rank()} 名",
            17,
            team_ui_color(self.team),
            (18, 35),
            bold=True,
        )
        draw_text(
            "5 队团队赛 · 5 分钟",
            17,
            MUTED_TEXT,
            (WIDTH // 2, 18),
            bold=True,
        )
        if self.player is None or not self.player.alive:
            draw_text(
                "复活中",
                14,
                (255, 170, 120),
                (WIDTH // 2, 42),
                bold=True,
            )
        mouse_pos = pygame.mouse.get_pos()
        draw_hud_button(
            PAUSE_BUTTON_RECT,
            "暂停游戏",
            mouse_pos,
            enabled=not self.paused,
            color=(227, 166, 58),
        )
        draw_hud_button(
            RESUME_BUTTON_RECT,
            "继续游戏",
            mouse_pos,
            enabled=self.paused,
            color=ACCENT,
        )

    def draw_team_score_strip(self):
        bar = pygame.Surface((WIDTH, 36), pygame.SRCALPHA)
        bar.fill((8, 18, 28, 188))
        SCREEN.blit(bar, (0, HEIGHT - 36))
        total_width = 5 * 178
        start_x = (WIDTH - total_width) // 2 + 12
        y = HEIGHT - 18
        for index, team in enumerate(TEAMS):
            x = start_x + index * 178
            pygame.draw.circle(SCREEN, (220, 230, 240), (x, y), 8, 1)
            pygame.draw.circle(SCREEN, team["body"], (x, y), 6)
            draw_left_text(
                f"{team['short']} {self.team_scores[index]}",
                15,
                TEXT_COLOR,
                (x + 12, y - 10),
                bold=(index == self.player_team_index),
            )

    def draw_respawn_overlay(self):
        remaining = None
        for item in self.respawn_queue:
            if item[3]:
                remaining = max(0, item[0] - pygame.time.get_ticks())
                break
        if remaining is None:
            text = "等待复活..."
        else:
            text = f"复活倒计时 {remaining / 1000:.1f}s"
        draw_text(
            text,
            26,
            (255, 190, 130),
            (WIDTH // 2, BOARD_TOP + 128),
            bold=True,
        )

    def draw(self):
        interval = max(1, self.difficulty["interval"])
        elapsed = pygame.time.get_ticks() - self.last_move
        self.render_t = (
            1.0
            if self.paused
            else max(0.0, min(1.0, elapsed / interval))
        )
        cam_x, cam_y = self.interpolated_head_world(self.render_t)
        if self.player is not None and self.player.alive:
            self.camera_world = (cam_x, cam_y)
        self.cam_x, self.cam_y = cam_x, cam_y

        SCREEN.fill((8, 14, 22))
        world_rect = pygame.Rect(
            int(VIEW_CENTER_X - self.cam_x),
            int(VIEW_CENTER_Y - self.cam_y),
            int(self.world_w),
            int(self.world_h),
        )
        pygame.draw.rect(SCREEN, BOARD_COLOR, world_rect)
        self.draw_grid(world_rect)
        self.draw_joystick()
        self.draw_food()
        for snake in self.all_snakes():
            if not snake.is_player:
                self.draw_snake(snake)
        if self.player is not None and self.player.alive:
            self.draw_snake(self.player)
        pygame.draw.rect(SCREEN, (56, 72, 86), world_rect, 4)
        pygame.draw.rect(SCREEN, (120, 150, 165), world_rect.inflate(-8, -8), 1)
        self.draw_radar()
        self.draw_team_timer()
        self.draw_notice()
        if self.paused:
            self.draw_paused_overlay()
        self.draw_team_hud()
        self.draw_team_score_strip()
        if self.player is None or not self.player.alive:
            self.draw_respawn_overlay()


def load_scores():
    if not SCORE_FILE.exists():
        return []
    try:
        data = json.loads(SCORE_FILE.read_text(encoding="utf-8"))
    except (OSError, json.JSONDecodeError):
        return []
    if not isinstance(data, list):
        return []

    scores = []
    for item in data:
        if not isinstance(item, dict):
            continue
        try:
            scores.append(
                {
                    "score": int(item.get("score", 0)),
                    "length": int(item.get("length", 0)),
                    "difficulty": str(item.get("difficulty", "未知")),
                    "skin": str(item.get("skin", "未知")),
                    "date": str(item.get("date", "")),
                }
            )
        except (TypeError, ValueError):
            continue
    scores.sort(key=lambda item: (-item["score"], -item["length"], item["date"]))
    return scores


def save_scores(scores):
    try:
        temp_file = SCORE_FILE.with_suffix(".tmp")
        temp_file.write_text(
            json.dumps(scores, ensure_ascii=False, indent=2),
            encoding="utf-8",
        )
        temp_file.replace(SCORE_FILE)
    except OSError as error:
        print(f"排行榜保存失败：{error}")


def record_score(game):
    scores = load_scores()
    entry = {
        "score": game.score,
        "length": len(game.snake) + 1,
        "difficulty": game.difficulty["name"],
        "skin": game.skin["name"],
        "date": datetime.now().strftime("%Y-%m-%d %H:%M"),
    }
    scores.append(entry)
    scores.sort(key=lambda item: (-item["score"], -item["length"], item["date"]))
    rank = 1 + sum(
        1
        for item in scores
        if (item["score"], item["length"]) > (entry["score"], entry["length"])
    )
    save_scores(scores)
    return scores, entry, rank


def draw_home(selected_skin, selected_difficulty, scores, mouse_pos):
    draw_menu_background()
    draw_text("贪 吃 蛇", 66, TEXT_COLOR, (WIDTH // 2, 64), bold=True)
    draw_text(
        "经典蛇群争食 · 5 队团队赛 · 12 生肖 / 动画角色皮肤",
        20,
        MUTED_TEXT,
        (WIDTH // 2, 112),
    )

    draw_avatar_portrait(
        SCREEN,
        (WIDTH // 2, 235),
        56,
        selected_skin,
    )

    draw_text(
        f"当前皮肤：{selected_skin['name']}（{selected_skin.get('group', '经典')}）",
        20,
        MUTED_TEXT,
        (WIDTH // 2, 340),
    )

    start_rect = pygame.Rect(206, 386, 170, 62)
    team_rect = pygame.Rect(396, 386, 170, 62)
    skin_rect = pygame.Rect(586, 386, 170, 62)
    difficulty_rect = pygame.Rect(776, 386, 170, 62)
    draw_button(start_rect, "开始游戏", mouse_pos)
    draw_button(
        team_rect,
        "团队模式",
        mouse_pos,
        color=(226, 120, 72),
        text_color=(255, 248, 240),
    )
    draw_button(
        skin_rect,
        "换皮肤",
        mouse_pos,
        color=(77, 135, 197),
        text_color=(244, 249, 252),
    )
    draw_button(
        difficulty_rect,
        f"难度：{selected_difficulty['name']}",
        mouse_pos,
        color=selected_difficulty["color"],
        text_color=selected_difficulty["text_color"],
    )

    if scores:
        high_score = scores[0]["score"]
        draw_text(
            f"历史最高分：{high_score}",
            22,
            (255, 226, 145),
            (WIDTH // 2, 500),
        )
    else:
        draw_text(
            "还没有游戏记录，来创造第一条成绩吧",
            19,
            MUTED_TEXT,
            (WIDTH // 2, 500),
        )

    draw_text(
        "团队模式：选队伍 → 选角色 → 5 分钟积分赛",
        18,
        (150, 210, 235),
        (WIDTH // 2, 550),
        bold=True,
    )
    draw_text(
        "经典：右上圆盘 / 方向键 / WASD / QEZC · ESC 返回主页",
        18,
        MUTED_TEXT,
        (WIDTH // 2, 660),
    )
    return start_rect, team_rect, skin_rect, difficulty_rect


def skin_card_rects(count=12):
    per_row = 6
    card_width = 170
    card_height = 164
    gap_x = 10
    gap_y = 14
    total_width = per_row * card_width + (per_row - 1) * gap_x
    start_x = (WIDTH - total_width) // 2
    cards = []
    for index in range(count):
        row = index // per_row
        col = index % per_row
        cards.append(
            pygame.Rect(
                start_x + col * (card_width + gap_x),
                150 + row * (card_height + gap_y),
                card_width,
                card_height,
            )
        )
    return cards


def draw_skin_page(selected_index, group_index, mouse_pos):
    draw_menu_background()
    draw_text("选择角色皮肤", 42, TEXT_COLOR, (WIDTH // 2, 40), bold=True)
    draw_text(
        "经典 / 生肖 / 熊出没 / 喜羊羊 / 猪猪侠 / 奥特曼",
        18,
        MUTED_TEXT,
        (WIDTH // 2, 74),
    )

    tab_width = 150
    tab_height = 34
    tab_gap = 8
    total_tabs_width = len(SKIN_GROUPS) * tab_width + (len(SKIN_GROUPS) - 1) * tab_gap
    tab_start = (WIDTH - total_tabs_width) // 2
    tab_rects = []
    for index, group in enumerate(SKIN_GROUPS):
        tab = pygame.Rect(
            tab_start + index * (tab_width + tab_gap),
            88,
            tab_width,
            tab_height,
        )
        tab_rects.append(tab)
        active = index == group_index
        pygame.draw.rect(
            SCREEN,
            (37, 62, 83) if active else PANEL_COLOR,
            tab,
            border_radius=10,
        )
        pygame.draw.rect(
            SCREEN,
            ACCENT if active else PANEL_BORDER,
            tab,
            2,
            border_radius=10,
        )
        draw_text(
            group["name"],
            17,
            TEXT_COLOR if active else MUTED_TEXT,
            tab.center,
            bold=active,
        )

    group = SKIN_GROUPS[group_index]
    cards = skin_card_rects(len(group["skins"]))
    for card, skin in zip(cards, group["skins"]):
        selected = skin is ALL_SKINS[selected_index]
        hovered = card.collidepoint(mouse_pos)
        card_color = (37, 62, 83) if hovered else PANEL_COLOR
        border_color = ACCENT if selected else PANEL_BORDER
        pygame.draw.rect(SCREEN, card_color, card, border_radius=14)
        pygame.draw.rect(
            SCREEN,
            border_color,
            card,
            4 if selected else 2,
            border_radius=14,
        )
        draw_avatar_portrait(
            SCREEN,
            (card.centerx, card.y + 62),
            30,
            skin,
        )
        draw_text(skin["name"], 18, TEXT_COLOR, (card.centerx, card.y + 116), bold=True)
        draw_text(
            skin.get("group", "经典"),
            13,
            MUTED_TEXT,
            (card.centerx, card.y + 136),
        )
        if selected:
            draw_text("已选择", 14, ACCENT, (card.centerx, card.y + 152), bold=True)
        else:
            draw_text("点击选择", 14, MUTED_TEXT, (card.centerx, card.y + 152))

    start_rect = pygame.Rect(411, 520, 160, 56)
    back_rect = pygame.Rect(591, 520, 160, 56)
    draw_button(start_rect, "开始游戏", mouse_pos)
    draw_button(
        back_rect,
        "返回",
        mouse_pos,
        color=(86, 112, 132),
        text_color=TEXT_COLOR,
    )
    return cards, tab_rects, start_rect, back_rect


def difficulty_card_rects():
    card_width = 270
    gap = 30
    total_width = len(DIFFICULTIES) * card_width + (len(DIFFICULTIES) - 1) * gap
    start_x = (WIDTH - total_width) // 2
    return [
        pygame.Rect(start_x + index * (card_width + gap), 135, card_width, 300)
        for index in range(len(DIFFICULTIES))
    ]


def draw_difficulty_page(selected_index, mouse_pos):
    draw_menu_background()
    draw_text("选择游戏难度", 50, TEXT_COLOR, (WIDTH // 2, 60), bold=True)
    draw_text("难度越高，蛇移动越快，小蛇也越多", 20, MUTED_TEXT, (WIDTH // 2, 101))

    cards = difficulty_card_rects()
    for index, (card, difficulty) in enumerate(zip(cards, DIFFICULTIES)):
        selected = index == selected_index
        hovered = card.collidepoint(mouse_pos)
        card_color = (37, 62, 83) if hovered else PANEL_COLOR
        border_color = difficulty["color"] if selected else PANEL_BORDER
        pygame.draw.rect(SCREEN, card_color, card, border_radius=18)
        pygame.draw.rect(
            SCREEN,
            border_color,
            card,
            5 if selected else 2,
            border_radius=18,
        )

        badge = pygame.Rect(card.centerx - 64, card.y + 28, 128, 44)
        pygame.draw.rect(SCREEN, difficulty["color"], badge, border_radius=12)
        draw_text(
            difficulty["name"],
            26,
            difficulty["text_color"],
            badge.center,
            bold=True,
        )

        draw_text(
            f"约 {difficulty['speed']:.1f} 格/秒",
            27,
            TEXT_COLOR,
            (card.centerx, card.y + 105),
            bold=True,
        )
        draw_text(
            f"每 {difficulty['interval']} 毫秒移动一格",
            20,
            MUTED_TEXT,
            (card.centerx, card.y + 147),
        )
        draw_text(
            f"初始小蛇 {difficulty['small_snakes']} 条",
            20,
            (150, 210, 235),
            (card.centerx, card.y + 180),
            bold=True,
        )

        bar_left = card.x + 38
        bar_top = card.y + 205
        bar_width = card.w - 76
        pygame.draw.rect(
            SCREEN,
            (45, 67, 85),
            (bar_left, bar_top, bar_width, 16),
            border_radius=8,
        )
        fill_width = int(bar_width * ((index + 1) / len(DIFFICULTIES)))
        pygame.draw.rect(
            SCREEN,
            difficulty["color"],
            (bar_left, bar_top, fill_width, 16),
            border_radius=8,
        )

        if selected:
            draw_text("已选择", 20, difficulty["color"], (card.centerx, card.y + 250), bold=True)
        else:
            draw_text("点击选择", 19, MUTED_TEXT, (card.centerx, card.y + 250))

    start_rect = pygame.Rect(411, 495, 170, 62)
    back_rect = pygame.Rect(601, 495, 150, 62)
    draw_button(start_rect, "开始游戏", mouse_pos)
    draw_button(back_rect, "返回主页", mouse_pos, color=(86, 112, 132), text_color=TEXT_COLOR)
    return cards, start_rect, back_rect


def draw_team_select(mouse_pos):
    draw_menu_background()
    draw_text("选择你的队伍", 50, TEXT_COLOR, (WIDTH // 2, 52), bold=True)
    draw_text(
        "5 队 × 5 名角色 · 5 分钟积分赛 · 红 / 蓝 / 绿 / 黑 / 白",
        19,
        MUTED_TEXT,
        (WIDTH // 2, 98),
    )

    top_back_rect = pygame.Rect(20, 16, 170, 46)
    draw_button(
        top_back_rect,
        "← 返回主页",
        mouse_pos,
        color=(86, 112, 132),
        text_color=TEXT_COLOR,
    )

    card_width = 200
    gap = 18
    total_width = len(TEAMS) * card_width + (len(TEAMS) - 1) * gap
    start_x = (WIDTH - total_width) // 2
    cards = []
    for index, team in enumerate(TEAMS):
        card = pygame.Rect(start_x + index * (card_width + gap), 140, card_width, 340)
        cards.append(card)
        hovered = card.collidepoint(mouse_pos)
        pygame.draw.rect(
            SCREEN,
            (37, 62, 83) if hovered else PANEL_COLOR,
            card,
            border_radius=18,
        )
        pygame.draw.rect(SCREEN, team_ui_color(team), card, 4, border_radius=18)
        band = pygame.Rect(card.x, card.y, card.w, 66)
        pygame.draw.rect(
            SCREEN,
            team["body"],
            band,
            border_top_left_radius=14,
            border_top_right_radius=14,
        )
        draw_text(
            team["name"],
            19,
            team["text_color"],
            band.center,
            bold=True,
        )
        draw_text(
            "12 名角色",
            22,
            TEXT_COLOR,
            (card.centerx, card.y + 102),
            bold=True,
        )
        draw_text(
            "队伍色：" + ("红" if index == 0 else "蓝" if index == 1 else "绿" if index == 2 else "黑" if index == 3 else "白"),
            16,
            MUTED_TEXT,
            (card.centerx, card.y + 132),
        )
        for preview_index in range(3):
            skin = team_skin(team["skins"][preview_index], team)
            draw_avatar_portrait(
                SCREEN,
                (card.centerx - 62 + preview_index * 62, card.y + 200),
                20,
                skin,
                team=team,
                show_badge=False,
            )
        draw_text(
            "点击选择",
            17,
            team_ui_color(team),
            (card.centerx, card.y + 280),
            bold=True,
        )

    back_rect = pygame.Rect(486, 560, 180, 56)
    draw_button(
        back_rect,
        "返回主页",
        mouse_pos,
        color=(86, 112, 132),
        text_color=TEXT_COLOR,
    )
    return cards, [top_back_rect, back_rect]


def draw_team_skin_page(team_index, selected_index, mouse_pos):
    team = TEAMS[team_index]
    draw_menu_background()
    draw_text(
        f"{team['name']} · 选择角色",
        40,
        TEXT_COLOR,
        (WIDTH // 2, 42),
        bold=True,
    )
    draw_text(
        "点击角色卡片，再点「开始比赛」",
        18,
        MUTED_TEXT,
        (WIDTH // 2, 80),
    )
    draw_text(
        f"队伍色：{team['short']} · 5 分钟积分赛",
        17,
        team_ui_color(team),
        (WIDTH // 2, 108),
        bold=True,
    )

    top_back_rect = pygame.Rect(20, 16, 170, 46)
    draw_button(
        top_back_rect,
        "← 返回队伍",
        mouse_pos,
        color=(86, 112, 132),
        text_color=TEXT_COLOR,
    )

    cards = skin_card_rects(len(team["skins"]))
    for index, (card, skin) in enumerate(zip(cards, team["skins"])):
        selected = index == selected_index
        hovered = card.collidepoint(mouse_pos)
        pygame.draw.rect(
            SCREEN,
            (37, 62, 83) if hovered else PANEL_COLOR,
            card,
            border_radius=14,
        )
        pygame.draw.rect(
            SCREEN,
            team_ui_color(team) if selected else PANEL_BORDER,
            card,
            4 if selected else 2,
            border_radius=14,
        )
        preview = team_skin(skin, team)
        draw_avatar_portrait(
            SCREEN,
            (card.centerx, card.y + 62),
            30,
            preview,
            team=team,
        )
        draw_text(skin["name"], 18, TEXT_COLOR, (card.centerx, card.y + 116), bold=True)
        draw_text(
            team["short"] + "角色",
            13,
            team_ui_color(team),
            (card.centerx, card.y + 136),
        )
        if selected:
            draw_text("已选择", 14, team_ui_color(team), (card.centerx, card.y + 152), bold=True)
        else:
            draw_text("点击选择", 14, MUTED_TEXT, (card.centerx, card.y + 152))

    start_rect = pygame.Rect(411, 520, 170, 56)
    back_rect = pygame.Rect(601, 520, 150, 56)
    draw_button(start_rect, "开始比赛", mouse_pos)
    draw_button(
        back_rect,
        "返回队伍",
        mouse_pos,
        color=(86, 112, 132),
        text_color=TEXT_COLOR,
    )
    return cards, start_rect, [top_back_rect, back_rect]


def draw_team_results(game, mouse_pos):
    if game.results is None:
        game.finish_match()
    draw_menu_background()
    draw_text("团 队 赛 结 束", 48, TEXT_COLOR, (WIDTH // 2, 42), bold=True)
    results = game.results
    winner = results["winner"]
    winner_team = TEAMS[winner]
    winner_text = f"获胜队伍：{winner_team['name']}"
    if len(results["tied"]) > 1:
        winner_text += "（同分，按最高个人分判定）"
    draw_text(
        winner_text,
        28,
        team_ui_color(winner_team),
        (WIDTH // 2, 94),
        bold=True,
    )

    left = pygame.Rect(30, 126, 720, 498)
    right = pygame.Rect(770, 126, 350, 498)
    pygame.draw.rect(SCREEN, (20, 35, 50), left, border_radius=18)
    pygame.draw.rect(SCREEN, PANEL_BORDER, left, 2, border_radius=18)
    pygame.draw.rect(SCREEN, (20, 35, 50), right, border_radius=18)
    pygame.draw.rect(SCREEN, PANEL_BORDER, right, 2, border_radius=18)

    draw_text(
        "各队总分与前三名",
        21,
        TEXT_COLOR,
        (left.centerx, left.y + 24),
        bold=True,
    )
    order = sorted(
        range(len(TEAMS)),
        key=lambda index: (-results["totals"][index], index),
    )
    for row, team_index in enumerate(order):
        team = TEAMS[team_index]
        row_y = left.y + 52 + row * 86
        row_rect = pygame.Rect(left.x + 14, row_y, left.w - 28, 76)
        if team_index == winner:
            pygame.draw.rect(SCREEN, (38, 82, 66), row_rect, border_radius=12)
        pygame.draw.rect(SCREEN, team_ui_color(team), row_rect, 2, border_radius=12)
        draw_left_text(
            f"{row + 1}. {team['name']}",
            19,
            team_ui_color(team),
            (row_rect.x + 14, row_y + 8),
            bold=True,
        )
        draw_left_text(
            f"总分 {results['totals'][team_index]}",
            19,
            TEXT_COLOR,
            (row_rect.x + 330, row_y + 8),
            bold=True,
        )
        top_text = "   ".join(
            f"{index + 1}.{name} {score}"
            for index, (name, score) in enumerate(results["team_top"][team_index])
        )
        draw_left_text(
            top_text or "暂无得分",
            16,
            (205, 219, 225),
            (row_rect.x + 14, row_y + 42),
        )

    draw_text(
        "获胜队 TOP 5",
        22,
        team_ui_color(winner_team),
        (right.centerx, right.y + 24),
        bold=True,
    )
    for index, (name, score) in enumerate(results["winner_top5"]):
        row_y = right.y + 64 + index * 58
        row_rect = pygame.Rect(right.x + 18, row_y, right.w - 36, 48)
        pygame.draw.rect(SCREEN, (30, 50, 66), row_rect, border_radius=10)
        draw_text(
            f"{index + 1}",
            18,
            team_ui_color(winner_team),
            (row_rect.x + 18, row_rect.centery),
            bold=True,
        )
        draw_text(
            name,
            18,
            TEXT_COLOR,
            (row_rect.centerx - 20, row_rect.centery),
            bold=True,
        )
        draw_text(
            str(score),
            18,
            (255, 226, 145),
            (row_rect.right - 36, row_rect.centery),
            bold=True,
        )
    if not results["winner_top5"]:
        draw_text(
            "暂无得分",
            18,
            MUTED_TEXT,
            (right.centerx, right.y + 100),
        )

    replay_rect = pygame.Rect(411, 642, 170, 50)
    home_rect = pygame.Rect(601, 642, 150, 50)
    draw_button(replay_rect, "再来一局", mouse_pos)
    draw_button(
        home_rect,
        "返回主页",
        mouse_pos,
        color=(86, 112, 132),
        text_color=TEXT_COLOR,
    )
    return replay_rect, home_rect


def draw_game_over(game, scores, current_entry, rank, mouse_pos):
    draw_menu_background()
    panel = pygame.Rect(126, 32, 900, 540)
    pygame.draw.rect(SCREEN, (20, 35, 50), panel, border_radius=22)
    pygame.draw.rect(SCREEN, PANEL_BORDER, panel, 2, border_radius=22)

    draw_text("游 戏 结 束", 44, (255, 124, 117), (WIDTH // 2, 72), bold=True)
    draw_text(game.dead_reason, 21, MUTED_TEXT, (WIDTH // 2, 110))

    summary = (
        f"本局分数：{game.score}    "
        f"身体长度：{len(game.snake) + 1}    "
        f"小蛇倒下：{game.small_deaths}    "
        f"排名：第 {rank} 名"
    )
    draw_text(summary, 21, (255, 226, 145), (WIDTH // 2, 147), bold=True)
    if rank == 1 and game.score > 0:
        draw_text("新纪录！", 20, ACCENT, (WIDTH // 2, 177), bold=True)

    draw_text("本地排行榜 TOP 5", 22, TEXT_COLOR, (WIDTH // 2, 207), bold=True)
    draw_left_text("名次", 17, MUTED_TEXT, (panel.x + 50, 235), bold=True)
    draw_left_text("分数", 17, MUTED_TEXT, (panel.x + 130, 235), bold=True)
    draw_left_text("长度", 17, MUTED_TEXT, (panel.x + 220, 235), bold=True)
    draw_left_text("难度", 17, MUTED_TEXT, (panel.x + 310, 235), bold=True)
    draw_left_text("皮肤", 17, MUTED_TEXT, (panel.x + 405, 235), bold=True)
    draw_left_text("时间", 17, MUTED_TEXT, (panel.x + 525, 235), bold=True)

    top_scores = scores[:5]
    for index, item in enumerate(top_scores):
        row_rect = pygame.Rect(panel.x + 40, 262 + index * 39, panel.w - 80, 32)
        is_current = item == current_entry
        if is_current:
            pygame.draw.rect(SCREEN, (41, 91, 75), row_rect, border_radius=8)

        row_color = TEXT_COLOR if is_current else (205, 219, 225)
        row_y = row_rect.centery - 9
        draw_left_text(str(index + 1), 18, row_color, (panel.x + 60, row_y))
        draw_left_text(str(item["score"]), 18, row_color, (panel.x + 135, row_y))
        draw_left_text(str(item["length"]), 18, row_color, (panel.x + 227, row_y))
        draw_left_text(item["difficulty"], 18, row_color, (panel.x + 310, row_y))
        draw_left_text(item["skin"], 18, row_color, (panel.x + 405, row_y))
        draw_left_text(item["date"][5:], 18, row_color, (panel.x + 525, row_y))

    if not top_scores:
        draw_text("暂无记录", 19, MUTED_TEXT, (WIDTH // 2, 325))

    replay_rect = pygame.Rect(411, 605, 160, 58)
    home_rect = pygame.Rect(591, 605, 160, 58)
    draw_button(replay_rect, "再来一局", mouse_pos)
    draw_button(home_rect, "返回主页", mouse_pos, color=(86, 112, 132), text_color=TEXT_COLOR)
    return replay_rect, home_rect


def main():
    running = True
    state = "home"
    selected_index = 0
    selected_group_index = 0
    selected_difficulty_index = 1
    selected_team_index = 0
    selected_team_skin_index = 0
    game = None
    scores = load_scores()
    current_entry = None
    current_rank = 0

    def group_index_for_skin(skin):
        for index, group in enumerate(SKIN_GROUPS):
            if any(candidate is skin for candidate in group["skins"]):
                return index
        return 0

    def launch_new_game():
        start_background_music()
        return SnakeGame(
            ALL_SKINS[selected_index],
            DIFFICULTIES[selected_difficulty_index],
        )

    def launch_team_game():
        start_background_music()
        return TeamGame(selected_team_index, selected_team_skin_index)

    key_directions = {
        pygame.K_UP: "up",
        pygame.K_w: "up",
        pygame.K_DOWN: "down",
        pygame.K_s: "down",
        pygame.K_LEFT: "left",
        pygame.K_a: "left",
        pygame.K_RIGHT: "right",
        pygame.K_d: "right",
        pygame.K_q: "up-left",
        pygame.K_e: "up-right",
        pygame.K_z: "down-left",
        pygame.K_c: "down-right",
    }

    while running:
        mouse_pos = pygame.mouse.get_pos()

        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                running = False
                continue

            if state == "home":
                if event.type == pygame.MOUSEBUTTONDOWN and event.button == 1:
                    start_rect, team_rect, skin_rect, difficulty_rect = draw_home(
                        ALL_SKINS[selected_index],
                        DIFFICULTIES[selected_difficulty_index],
                        scores,
                        mouse_pos,
                    )
                    if start_rect.collidepoint(event.pos):
                        game = launch_new_game()
                        state = "playing"
                    elif team_rect.collidepoint(event.pos):
                        state = "team_select"
                    elif skin_rect.collidepoint(event.pos):
                        selected_group_index = group_index_for_skin(
                            ALL_SKINS[selected_index]
                        )
                        state = "skins"
                    elif difficulty_rect.collidepoint(event.pos):
                        state = "difficulty"

            elif state == "skins":
                if event.type == pygame.MOUSEBUTTONDOWN and event.button == 1:
                    cards, tab_rects, start_rect, back_rect = draw_skin_page(
                        selected_index,
                        selected_group_index,
                        mouse_pos,
                    )
                    clicked_tab = False
                    for index, tab in enumerate(tab_rects):
                        if tab.collidepoint(event.pos):
                            selected_group_index = index
                            clicked_tab = True
                            break
                    if not clicked_tab:
                        group = SKIN_GROUPS[selected_group_index]
                        for card, skin in zip(cards, group["skins"]):
                            if card.collidepoint(event.pos):
                                for global_index, candidate in enumerate(ALL_SKINS):
                                    if candidate is skin:
                                        selected_index = global_index
                                        break
                                break
                    if start_rect.collidepoint(event.pos):
                        game = launch_new_game()
                        state = "playing"
                    elif back_rect.collidepoint(event.pos):
                        state = "home"
                elif event.type == pygame.KEYDOWN and event.key == pygame.K_ESCAPE:
                    state = "home"

            elif state == "difficulty":
                if event.type == pygame.MOUSEBUTTONDOWN and event.button == 1:
                    cards, start_rect, back_rect = draw_difficulty_page(
                        selected_difficulty_index,
                        mouse_pos,
                    )
                    for index, card in enumerate(cards):
                        if card.collidepoint(event.pos):
                            selected_difficulty_index = index
                            break
                    if start_rect.collidepoint(event.pos):
                        game = launch_new_game()
                        state = "playing"
                    elif back_rect.collidepoint(event.pos):
                        state = "home"
                elif event.type == pygame.KEYDOWN and event.key == pygame.K_ESCAPE:
                    state = "home"

            elif state == "team_select":
                if event.type == pygame.MOUSEBUTTONDOWN and event.button == 1:
                    cards, back_rects = draw_team_select(mouse_pos)
                    for index, card in enumerate(cards):
                        if card.collidepoint(event.pos):
                            selected_team_index = index
                            selected_team_skin_index = 0
                            state = "team_skins"
                            break
                    if any(rect.collidepoint(event.pos) for rect in back_rects):
                        state = "home"
                elif event.type == pygame.KEYDOWN and event.key == pygame.K_ESCAPE:
                    state = "home"

            elif state == "team_skins":
                if event.type == pygame.MOUSEBUTTONDOWN and event.button == 1:
                    cards, start_rect, back_rects = draw_team_skin_page(
                        selected_team_index,
                        selected_team_skin_index,
                        mouse_pos,
                    )
                    for index, card in enumerate(cards):
                        if card.collidepoint(event.pos):
                            selected_team_skin_index = index
                            break
                    if start_rect.collidepoint(event.pos):
                        game = launch_team_game()
                        state = "playing"
                    elif any(rect.collidepoint(event.pos) for rect in back_rects):
                        state = "team_select"
                elif event.type == pygame.KEYDOWN and event.key == pygame.K_ESCAPE:
                    state = "team_select"

            elif state == "playing":
                if event.type == pygame.KEYDOWN:
                    if event.key == pygame.K_ESCAPE:
                        stop_background_music()
                        state = "home"
                    elif event.key in (pygame.K_p, pygame.K_SPACE):
                        game.set_paused(not game.paused)
                    elif game.paused:
                        continue
                    elif event.key in key_directions:
                        game.turn(key_directions[event.key])
                elif event.type == pygame.MOUSEBUTTONDOWN and event.button == 1:
                    if game.paused:
                        if (
                            game.pause_resume_rect is not None
                            and game.pause_resume_rect.collidepoint(event.pos)
                        ) or RESUME_BUTTON_RECT.collidepoint(event.pos):
                            game.set_paused(False)
                        elif (
                            game.pause_exit_rect is not None
                            and game.pause_exit_rect.collidepoint(event.pos)
                        ):
                            stop_background_music()
                            state = "home"
                    elif PAUSE_BUTTON_RECT.collidepoint(event.pos):
                        game.set_paused(True)

            elif state == "game_over":
                if event.type == pygame.KEYDOWN and event.key in (
                    pygame.K_RETURN,
                    pygame.K_SPACE,
                ):
                    game = launch_new_game()
                    state = "playing"
                elif event.type == pygame.KEYDOWN and event.key == pygame.K_ESCAPE:
                    state = "home"
                elif event.type == pygame.MOUSEBUTTONDOWN and event.button == 1:
                    replay_rect, home_rect = draw_game_over(
                        game,
                        scores,
                        current_entry,
                        current_rank,
                        mouse_pos,
                    )
                    if replay_rect.collidepoint(event.pos):
                        game = launch_new_game()
                        state = "playing"
                    elif home_rect.collidepoint(event.pos):
                        state = "home"

            elif state == "team_results":
                if event.type == pygame.KEYDOWN and event.key in (
                    pygame.K_RETURN,
                    pygame.K_SPACE,
                ):
                    game = launch_team_game()
                    state = "playing"
                elif event.type == pygame.KEYDOWN and event.key == pygame.K_ESCAPE:
                    state = "home"
                elif event.type == pygame.MOUSEBUTTONDOWN and event.button == 1:
                    replay_rect, home_rect = draw_team_results(game, mouse_pos)
                    if replay_rect.collidepoint(event.pos):
                        game = launch_team_game()
                        state = "playing"
                    elif home_rect.collidepoint(event.pos):
                        state = "home"

        if state == "playing" and not game.paused:
            game.update_pointer(mouse_pos)
            now = pygame.time.get_ticks()
            if now - game.last_move >= game.difficulty["interval"]:
                game.last_move = now
                dead_reason = game.update()
                if game.mode == "classic":
                    if dead_reason:
                        game.dead_reason = dead_reason
                        scores, current_entry, current_rank = record_score(game)
                        stop_background_music()
                        play_sound(DEATH_SOUND)
                        state = "game_over"
                elif game.time_left_ms() <= 0:
                    game.finish_match()
                    stop_background_music()
                    play_sound(DEATH_SOUND)
                    state = "team_results"

        if state == "home":
            draw_home(
                ALL_SKINS[selected_index],
                DIFFICULTIES[selected_difficulty_index],
                scores,
                mouse_pos,
            )
        elif state == "skins":
            draw_skin_page(
                selected_index,
                selected_group_index,
                mouse_pos,
            )
        elif state == "difficulty":
            draw_difficulty_page(selected_difficulty_index, mouse_pos)
        elif state == "team_select":
            draw_team_select(mouse_pos)
        elif state == "team_skins":
            draw_team_skin_page(
                selected_team_index,
                selected_team_skin_index,
                mouse_pos,
            )
        elif state == "playing":
            game.draw()
        elif state == "game_over":
            draw_game_over(
                game,
                scores,
                current_entry,
                current_rank,
                mouse_pos,
            )
        elif state == "team_results":
            draw_team_results(game, mouse_pos)

        pygame.display.flip()
        CLOCK.tick(60)

    pygame.quit()


if __name__ == "__main__":
    main()
