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
GRID_ROWS = 96
GRID_COLS = 96
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
JOYSTICK_RADIUS = 110
JOYSTICK_DEADZONE = 16

SCORE_FILE = Path(__file__).resolve().with_name("snake_scores.json")

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

FOOD_TARGET = 36
CLEAR_RADIUS = 10
CLEAR_COOLDOWN_MS = 7000
MAX_EXTRA_SNAKES = 2
CLEAR_SCORE = 20
FULL_CLEAR_SCORE = 100
REINFORCEMENT_THICKNESS = 8.0

DIRECTION_STEPS = {
    "up": (0, -1),
    "down": (0, 1),
    "left": (-1, 0),
    "right": (1, 0),
}
OPPOSITE = {
    "up": "down",
    "down": "up",
    "left": "right",
    "right": "left",
}

SKINS = [
    {
        "name": "红蛇",
        "body": (238, 91, 91),
        "body_dark": (190, 48, 58),
        "head": (213, 60, 66),
        "outline": (91, 29, 36),
        "highlight": (255, 177, 162),
        "belly": (255, 210, 188),
        "tongue": (255, 104, 124),
    },
    {
        "name": "黄蛇",
        "body": (248, 207, 83),
        "body_dark": (218, 151, 39),
        "head": (232, 174, 47),
        "outline": (104, 72, 13),
        "highlight": (255, 245, 177),
        "belly": (255, 239, 188),
        "tongue": (238, 94, 105),
    },
    {
        "name": "蓝蛇",
        "body": (77, 161, 244),
        "body_dark": (42, 104, 199),
        "head": (51, 132, 224),
        "outline": (20, 59, 113),
        "highlight": (169, 220, 255),
        "belly": (197, 229, 255),
        "tongue": (255, 117, 143),
    },
    {
        "name": "绿蛇",
        "body": (82, 201, 123),
        "body_dark": (41, 146, 82),
        "head": (55, 177, 101),
        "outline": (18, 76, 43),
        "highlight": (181, 249, 199),
        "belly": (211, 247, 211),
        "tongue": (255, 120, 143),
    },
    {
        "name": "黑蛇",
        "body": (66, 73, 83),
        "body_dark": (31, 36, 44),
        "head": (49, 55, 64),
        "outline": (7, 9, 12),
        "highlight": (159, 176, 188),
        "belly": (188, 201, 209),
        "tongue": (246, 94, 119),
    },
]

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

pygame.mixer.pre_init(44100, -16, 2, 512)
pygame.init()
AUDIO_ENABLED = pygame.mixer.get_init() is not None
SCREEN = pygame.display.set_mode((WIDTH, HEIGHT))
pygame.display.set_caption("贪吃蛇 - 蛇群争食")
CLOCK = pygame.time.Clock()

FONT_PATHS = [
    Path("C:/Windows/Fonts/msyh.ttc"),
    Path("C:/Windows/Fonts/simhei.ttf"),
    Path("C:/Windows/Fonts/simsun.ttc"),
]
FONT_PATH = next((path for path in FONT_PATHS if path.exists()), None)
FONT_CACHE = {}


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


def wrapped_distance(first, second):
    dx = wrapped_delta(first.col - second.col, GRID_COLS)
    dy = wrapped_delta(first.row - second.row, GRID_ROWS)
    return abs(dx) + abs(dy)


class Point:
    __slots__ = ("col", "row")

    def __init__(self, col, row):
        self.col = col
        self.row = row

    def copy(self):
        return Point(row=self.row, col=self.col)


class Snake:
    def __init__(self, body, direction, skin, thickness, is_player=False):
        self.body = [part.copy() for part in body]
        self.direction = direction
        self.skin = skin
        self.thickness = thickness
        self.is_player = is_player
        self.eaten = 0
        self.grow_pending = 0

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
    head_width = int(body_radius * 2.9)
    head_height = int(body_radius * 2.35)
    head_rect = pygame.Rect(0, 0, head_width, head_height)
    head_rect.center = (head_x + body_radius // 2, head_y)
    pygame.draw.ellipse(
        preview,
        skin["outline"],
        head_rect.inflate(6 * render_scale, 6 * render_scale),
    )
    pygame.draw.ellipse(preview, skin["head"], head_rect)
    pygame.draw.ellipse(
        preview,
        mix_color(skin["head"], skin["highlight"], 0.28),
        pygame.Rect(
            head_rect.x + head_width // 5,
            head_rect.y + head_height // 6,
            max(4, head_width // 2),
            max(3, head_height // 5),
        ),
    )

    eye_radius = max(3, body_radius // 3)
    eye_x = head_rect.right - head_width // 4
    eye_top = head_rect.centery - head_height // 5
    eye_bottom = head_rect.centery + head_height // 5
    for eye_y in (eye_top, eye_bottom):
        pygame.draw.circle(preview, (248, 252, 251), (eye_x, eye_y), eye_radius)
        pygame.draw.circle(
            preview,
            (20, 28, 31),
            (eye_x + max(1, eye_radius // 3), eye_y),
            max(1, eye_radius // 2),
        )

    tongue_start = (head_rect.right - 2, head_rect.centery)
    tongue_end = (head_rect.right + body_radius // 2, head_rect.centery)
    pygame.draw.line(
        preview,
        skin["tongue"],
        tongue_start,
        tongue_end,
        max(2, render_scale),
    )
    pygame.draw.line(
        preview,
        skin["tongue"],
        tongue_end,
        (tongue_end[0] + body_radius // 4, tongue_end[1] - body_radius // 5),
        max(2, render_scale),
    )
    pygame.draw.line(
        preview,
        skin["tongue"],
        tongue_end,
        (tongue_end[0] + body_radius // 4, tongue_end[1] + body_radius // 5),
        max(2, render_scale),
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
        self.skin = skin
        self.difficulty = difficulty
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

        start_row = GRID_ROWS // 2
        start_col = GRID_COLS // 2
        body = [Point(col=start_col + index, row=start_row) for index in range(5)]
        self.player = Snake(body, "left", skin, PLAYER_START_THICKNESS, True)
        self.next_direction = "left"
        self.last_move = pygame.time.get_ticks()
        head = self.player.head
        self.cam_x = (head.col + 0.5) * CELL_WIDTH
        self.cam_y = (head.row + 0.5) * CELL_HEIGHT

        for _ in range(difficulty["small_snakes"]):
            self.spawn_small_snake(initial=True)
        self.spawn_food(FOOD_TARGET)
        self.show_notice("无墙穿屏 · 清空周围食物会引来小蛇", ACCENT, 2800)

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
        if len(self.foods) >= FOOD_TARGET + 8:
            return
        for _ in range(amount):
            for _attempt in range(500):
                if near is not None:
                    angle = random.uniform(0.0, math.tau)
                    radius = random.uniform(min_radius, max_radius)
                    col = int(round(near.col + math.cos(angle) * radius))
                    row = int(round(near.row + math.sin(angle) * radius))
                else:
                    col = random.randrange(GRID_COLS)
                    row = random.randrange(GRID_ROWS)
                col %= GRID_COLS
                row %= GRID_ROWS
                if not self.cell_is_free(col, row):
                    continue
                if wrapped_distance(Point(col, row), self.player.head) < 4:
                    continue
                self.foods.append(Point(col=col, row=row))
                break

    def spawn_small_snake(self, initial=False, thickness=SMALL_START_THICKNESS):
        palettes = [skin for skin in SKINS if skin is not self.skin] or SKINS
        for _attempt in range(400):
            direction = random.choice(list(DIRECTION_STEPS))
            step_col, step_row = DIRECTION_STEPS[direction]
            head_col = random.randrange(GRID_COLS)
            head_row = random.randrange(GRID_ROWS)
            body = []
            valid = True
            length = random.randint(4, 6)
            for index in range(length):
                col = (head_col - step_col * index) % GRID_COLS
                row = (head_row - step_row * index) % GRID_ROWS
                if not self.cell_is_free(col, row):
                    valid = False
                    break
                body.append(Point(col=col, row=row))
            if not valid:
                continue
            distance = wrapped_distance(body[0], self.player.head)
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
            distance = wrapped_distance(point, food)
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
            for part in other.body:
                danger.add((part.row, part.col))
            heads.append(other.head)

        options = []
        for direction, (step_col, step_row) in DIRECTION_STEPS.items():
            if direction == OPPOSITE[snake.direction]:
                continue
            col = (head.col + step_col) % GRID_COLS
            row = (head.row + step_row) % GRID_ROWS
            score = random.random() * 0.35
            if (row, col) in danger:
                score += 80
            if target is not None:
                score += wrapped_distance(Point(col, row), target)
            for other_head in heads:
                if other_head is head:
                    continue
                if wrapped_distance(Point(col, row), other_head) <= 1:
                    score += 7
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
                col=(head.col + step_col) % GRID_COLS,
                row=(head.row + step_row) % GRID_ROWS,
            )
            new_heads[snake] = new_head
            eating[snake] = any(
                food.col == new_head.col and food.row == new_head.row
                for food in self.foods
            )

        after_cells = {}
        for snake in snakes:
            cells = {(part.row, part.col) for part in snake.body}
            if not eating[snake] and snake.grow_pending <= 0:
                tail = snake.body[-1]
                cells.discard((tail.row, tail.col))
            after_cells[snake] = cells

        deaths = {}
        for snake in snakes:
            cell = (new_heads[snake].row, new_heads[snake].col)
            for other in snakes:
                if other is snake:
                    continue
                if cell in after_cells[other]:
                    if other.is_player:
                        deaths[snake] = "撞到了大蛇的身体！"
                    else:
                        deaths[snake] = "撞到了小蛇的身体！"
                    break
            if snake not in deaths and cell in after_cells[snake]:
                deaths[snake] = "撞到了自己的身体！"

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
            if eating[snake]:
                if snake.is_player:
                    snake.grow_pending += 1
            elif snake.grow_pending > 0:
                snake.grow_pending -= 1
            else:
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
            if len(self.foods) >= FOOD_TARGET + 12:
                break
            if self.cell_is_free(part.col, part.row):
                self.foods.append(part.copy())
        self.respawn_at.append(now + self.difficulty["respawn"])
        if len(self.foods) > FOOD_TARGET + 2:
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
                wrapped_distance(food, self.head) <= CLEAR_RADIUS
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
            (head.col + 0.5) * CELL_WIDTH,
            (head.row + 0.5) * CELL_HEIGHT,
        )

    def to_screen(self, x, y):
        delta_x = wrapped_delta(x - self.cam_x, WORLD_WIDTH)
        delta_y = wrapped_delta(y - self.cam_y, WORLD_HEIGHT)
        return (
            int(VIEW_CENTER_X + delta_x),
            int(VIEW_CENTER_Y + delta_y),
        )

    def cell_screen(self, part):
        return self.to_screen(
            (part.col + 0.5) * CELL_WIDTH,
            (part.row + 0.5) * CELL_HEIGHT,
        )

    def draw_line(self, color, start, end, width):
        pygame.draw.line(SCREEN, color, start, end, width)

    def draw_circle(self, color, center, radius):
        pygame.draw.circle(SCREEN, color, center, radius)

    def draw_head(self, snake, center, thickness):
        skin = snake.skin
        direction = snake.direction
        head_long = min(int(CELL_WIDTH) + 2, thickness + 7)
        head_short = min(int(CELL_HEIGHT) - 2, thickness + 3)
        if direction in ("left", "right"):
            head_rect = pygame.Rect(0, 0, head_long, head_short)
        else:
            head_rect = pygame.Rect(0, 0, head_short, head_long)
        head_rect.center = center

        pygame.draw.ellipse(SCREEN, skin["outline"], head_rect.inflate(5, 5))
        pygame.draw.ellipse(SCREEN, skin["head"], head_rect)
        snout_rect = head_rect.inflate(
            -max(2, head_rect.w // 3),
            -max(2, head_rect.h // 3),
        )
        snout_rect.center = (
            head_rect.centerx + (
                2 if direction == "right"
                else -2 if direction == "left"
                else 0
            ),
            head_rect.centery + (
                2 if direction == "down"
                else -2 if direction == "up"
                else 0
            ),
        )
        pygame.draw.ellipse(
            SCREEN,
            mix_color(skin["head"], skin["highlight"], 0.24),
            snout_rect,
        )

        center_x, center_y = head_rect.center
        eye_offset = max(1, head_short // 6)
        eye_radius = max(1, head_short // 7)
        pupil_radius = max(1, eye_radius // 2)
        if direction == "left":
            eyes = (
                (center_x - eye_offset, center_y - eye_offset),
                (center_x - eye_offset, center_y + eye_offset),
            )
            pupil_shift = (-1, 0)
        elif direction == "right":
            eyes = (
                (center_x + eye_offset, center_y - eye_offset),
                (center_x + eye_offset, center_y + eye_offset),
            )
            pupil_shift = (1, 0)
        elif direction == "up":
            eyes = (
                (center_x - eye_offset, center_y - eye_offset),
                (center_x + eye_offset, center_y - eye_offset),
            )
            pupil_shift = (0, -1)
        else:
            eyes = (
                (center_x - eye_offset, center_y + eye_offset),
                (center_x + eye_offset, center_y + eye_offset),
            )
            pupil_shift = (0, 1)
        for eye in eyes:
            pygame.draw.circle(SCREEN, (248, 252, 251), eye, eye_radius)
            pygame.draw.circle(
                SCREEN,
                (18, 27, 31),
                (eye[0] + pupil_shift[0], eye[1] + pupil_shift[1]),
                pupil_radius,
            )

        tongue_length = max(3, thickness // 2)
        if direction == "left":
            tongue_start = (head_rect.left, center_y)
            tongue_tip = (tongue_start[0] - tongue_length, center_y)
            forks = (
                (tongue_tip[0] - 2, tongue_tip[1] - 2),
                (tongue_tip[0] - 2, tongue_tip[1] + 2),
            )
        elif direction == "right":
            tongue_start = (head_rect.right, center_y)
            tongue_tip = (tongue_start[0] + tongue_length, center_y)
            forks = (
                (tongue_tip[0] + 2, tongue_tip[1] - 2),
                (tongue_tip[0] + 2, tongue_tip[1] + 2),
            )
        elif direction == "up":
            tongue_start = (center_x, head_rect.top)
            tongue_tip = (center_x, tongue_start[1] - tongue_length)
            forks = (
                (tongue_tip[0] - 2, tongue_tip[1] - 2),
                (tongue_tip[0] + 2, tongue_tip[1] - 2),
            )
        else:
            tongue_start = (center_x, head_rect.bottom)
            tongue_tip = (center_x, tongue_start[1] + tongue_length)
            forks = (
                (tongue_tip[0] - 2, tongue_tip[1] + 2),
                (tongue_tip[0] + 2, tongue_tip[1] + 2),
            )
        pygame.draw.line(SCREEN, skin["tongue"], tongue_start, tongue_tip, 2)
        pygame.draw.line(SCREEN, skin["tongue"], tongue_tip, forks[0], 1)
        pygame.draw.line(SCREEN, skin["tongue"], tongue_tip, forks[1], 1)

    def draw_snake(self, snake):
        thickness = max(4, int(round(snake.thickness)))
        centers = [self.cell_screen(part) for part in snake.body]

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

        tail = centers[-1]
        self.draw_circle(snake.skin["outline"], tail, radius + 2)
        self.draw_circle(
            mix_color(snake.skin["body_dark"], snake.skin["body"], 0.35),
            tail,
            radius,
        )

        self.draw_head(snake, centers[0], thickness)

    def draw_grid(self):
        for col in range(0, GRID_COLS, 4):
            screen_x = int(
                VIEW_CENTER_X
                + wrapped_delta(col * CELL_WIDTH - self.cam_x, WORLD_WIDTH)
            )
            if -CELL_WIDTH <= screen_x <= WIDTH + CELL_WIDTH:
                pygame.draw.line(
                    SCREEN,
                    GRID_COLOR,
                    (screen_x, BOARD_TOP),
                    (screen_x, HEIGHT),
                    1,
                )
        for row in range(0, GRID_ROWS, 4):
            screen_y = int(
                VIEW_CENTER_Y
                + wrapped_delta(row * CELL_HEIGHT - self.cam_y, WORLD_HEIGHT)
            )
            if BOARD_TOP - CELL_HEIGHT <= screen_y <= HEIGHT + CELL_HEIGHT:
                pygame.draw.line(
                    SCREEN,
                    GRID_COLOR,
                    (0, screen_y),
                    (WIDTH, screen_y),
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
        delta_x = mouse_pos[0] - VIEW_CENTER_X
        delta_y = mouse_pos[1] - VIEW_CENTER_Y
        if delta_x * delta_x + delta_y * delta_y > JOYSTICK_RADIUS ** 2:
            return
        if abs(delta_x) < JOYSTICK_DEADZONE and abs(delta_y) < JOYSTICK_DEADZONE:
            return
        if abs(delta_x) >= abs(delta_y):
            self.turn("right" if delta_x > 0 else "left")
        else:
            self.turn("down" if delta_y > 0 else "up")

    def draw_joystick(self):
        mouse_pos = pygame.mouse.get_pos()
        delta_x = mouse_pos[0] - VIEW_CENTER_X
        delta_y = mouse_pos[1] - VIEW_CENTER_Y
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
                int(VIEW_CENTER_X - JOYSTICK_RADIUS),
                int(VIEW_CENTER_Y - JOYSTICK_RADIUS),
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
            dot_x = rect.x + (head.col + 0.5) / GRID_COLS * rect.w
            dot_y = rect.y + (head.row + 0.5) / GRID_ROWS * rect.h
            pygame.draw.circle(
                SCREEN,
                (238, 78, 78),
                (int(dot_x), int(dot_y)),
                3,
            )

        head = self.player.head
        dot_x = rect.x + (head.col + 0.5) / GRID_COLS * rect.w
        dot_y = rect.y + (head.row + 0.5) / GRID_ROWS * rect.h
        pygame.draw.circle(SCREEN, (250, 255, 250), (int(dot_x), int(dot_y)), 5)
        pygame.draw.circle(SCREEN, (56, 232, 118), (int(dot_x), int(dot_y)), 3)

    def draw(self):
        self.cam_x, self.cam_y = self.head_world()
        SCREEN.fill((18, 31, 42))
        pygame.draw.rect(SCREEN, BOARD_COLOR, BOARD_RECT)
        self.draw_grid()
        self.draw_joystick()
        self.draw_food()
        for snake in self.small_snakes:
            self.draw_snake(snake)
        self.draw_snake(self.player)
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
        overlay.fill((8, 18, 27, 112))
        SCREEN.blit(overlay, (0, BOARD_TOP))

        panel = pygame.Rect(
            WIDTH // 2 - 230,
            BOARD_TOP + BOARD_HEIGHT // 2 - 76,
            460,
            152,
        )
        pygame.draw.rect(SCREEN, (20, 36, 50), panel, border_radius=20)
        pygame.draw.rect(SCREEN, (87, 194, 164), panel, 2, border_radius=20)
        draw_text(
            "游戏已暂停",
            34,
            TEXT_COLOR,
            (WIDTH // 2, panel.y + 52),
            bold=True,
        )
        draw_text(
            "点击右上角「继续游戏」或按空格继续",
            18,
            MUTED_TEXT,
            (WIDTH // 2, panel.y + 104),
        )

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
    draw_text("贪 吃 蛇", 66, TEXT_COLOR, (WIDTH // 2, 70), bold=True)
    draw_text(
        "无墙穿屏 · 随机食物 · 清空周围引来小蛇",
        21,
        MUTED_TEXT,
        (WIDTH // 2, 118),
    )

    draw_snake_art(
        (WIDTH // 2, 262),
        selected_skin,
        length=14,
        spacing=20,
        radius=13,
        amplitude=18,
    )

    selected_label = f"当前皮肤：{selected_skin['name']}"
    draw_text(selected_label, 21, MUTED_TEXT, (WIDTH // 2, 352))

    start_rect = pygame.Rect(291, 400, 170, 62)
    skin_rect = pygame.Rect(491, 400, 170, 62)
    difficulty_rect = pygame.Rect(691, 400, 170, 62)
    draw_button(start_rect, "开始游戏", mouse_pos)
    draw_button(skin_rect, "换皮肤", mouse_pos, color=(77, 135, 197), text_color=(244, 249, 252))
    draw_button(
        difficulty_rect,
        f"难度：{selected_difficulty['name']}",
        mouse_pos,
        color=selected_difficulty["color"],
        text_color=selected_difficulty["text_color"],
    )

    if scores:
        high_score = scores[0]["score"]
        draw_text(f"历史最高分：{high_score}", 22, (255, 226, 145), (WIDTH // 2, 515))
    else:
        draw_text("还没有游戏记录，来创造第一条成绩吧", 19, MUTED_TEXT, (WIDTH // 2, 515))

    draw_text(
        "鼠标圆盘控制方向 · 方向键 / WASD 备用 · ESC 返回主页",
        18,
        MUTED_TEXT,
        (WIDTH // 2, 660),
    )
    return start_rect, skin_rect, difficulty_rect


def skin_card_rects():
    card_width = 170
    gap = 16
    total_width = len(SKINS) * card_width + (len(SKINS) - 1) * gap
    start_x = (WIDTH - total_width) // 2
    return [
        pygame.Rect(start_x + index * (card_width + gap), 130, card_width, 300)
        for index in range(len(SKINS))
    ]


def draw_skin_page(selected_index, mouse_pos):
    draw_menu_background()
    draw_text("选择蛇的皮肤", 50, TEXT_COLOR, (WIDTH // 2, 60), bold=True)
    draw_text("点击卡片切换颜色", 20, MUTED_TEXT, (WIDTH // 2, 101))

    cards = skin_card_rects()
    for index, (card, skin) in enumerate(zip(cards, SKINS)):
        selected = index == selected_index
        hovered = card.collidepoint(mouse_pos)
        card_color = (37, 62, 83) if hovered else PANEL_COLOR
        border_color = ACCENT if selected else PANEL_BORDER
        pygame.draw.rect(SCREEN, card_color, card, border_radius=16)
        pygame.draw.rect(SCREEN, border_color, card, 4 if selected else 2, border_radius=16)

        draw_snake_art(
            (card.centerx, card.y + 90),
            skin,
            length=9,
            spacing=10,
            radius=7,
            amplitude=8,
        )
        draw_text(skin["name"], 27, TEXT_COLOR, (card.centerx, card.y + 195), bold=True)
        if selected:
            draw_text("已选择", 20, ACCENT, (card.centerx, card.y + 245), bold=True)
        else:
            draw_text("点击选择", 19, MUTED_TEXT, (card.centerx, card.y + 245))

    start_rect = pygame.Rect(419, 495, 160, 62)
    back_rect = pygame.Rect(599, 495, 140, 62)
    draw_button(start_rect, "开始游戏", mouse_pos)
    draw_button(back_rect, "返回", mouse_pos, color=(86, 112, 132), text_color=TEXT_COLOR)
    return cards, start_rect, back_rect


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
    selected_difficulty_index = 1
    game = None
    scores = load_scores()
    current_entry = None
    current_rank = 0

    def launch_new_game():
        start_background_music()
        return SnakeGame(
            SKINS[selected_index],
            DIFFICULTIES[selected_difficulty_index],
        )

    key_directions = {
        pygame.K_UP: "up",
        pygame.K_w: "up",
        pygame.K_DOWN: "down",
        pygame.K_s: "down",
        pygame.K_LEFT: "left",
        pygame.K_a: "left",
        pygame.K_RIGHT: "right",
        pygame.K_d: "right",
    }

    while running:
        mouse_pos = pygame.mouse.get_pos()

        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                running = False
                continue

            if state == "home":
                if event.type == pygame.MOUSEBUTTONDOWN and event.button == 1:
                    start_rect, skin_rect, difficulty_rect = draw_home(
                        SKINS[selected_index],
                        DIFFICULTIES[selected_difficulty_index],
                        scores,
                        mouse_pos,
                    )
                    if start_rect.collidepoint(event.pos):
                        game = launch_new_game()
                        state = "playing"
                    elif skin_rect.collidepoint(event.pos):
                        state = "skins"
                    elif difficulty_rect.collidepoint(event.pos):
                        state = "difficulty"

            elif state == "skins":
                if event.type == pygame.MOUSEBUTTONDOWN and event.button == 1:
                    cards, start_rect, back_rect = draw_skin_page(
                        selected_index, mouse_pos
                    )
                    for index, card in enumerate(cards):
                        if card.collidepoint(event.pos):
                            selected_index = index
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
                    if not game.paused and PAUSE_BUTTON_RECT.collidepoint(event.pos):
                        game.set_paused(True)
                    elif game.paused and RESUME_BUTTON_RECT.collidepoint(event.pos):
                        game.set_paused(False)

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

        if state == "playing" and not game.paused:
            game.update_pointer(mouse_pos)
            now = pygame.time.get_ticks()
            if now - game.last_move >= game.difficulty["interval"]:
                game.last_move = now
                dead_reason = game.update()
                if dead_reason:
                    game.dead_reason = dead_reason
                    scores, current_entry, current_rank = record_score(game)
                    stop_background_music()
                    play_sound(DEATH_SOUND)
                    state = "game_over"

        if state == "home":
            draw_home(
                SKINS[selected_index],
                DIFFICULTIES[selected_difficulty_index],
                scores,
                mouse_pos,
            )
        elif state == "skins":
            draw_skin_page(selected_index, mouse_pos)
        elif state == "difficulty":
            draw_difficulty_page(selected_difficulty_index, mouse_pos)
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

        pygame.display.flip()
        CLOCK.tick(60)

    pygame.quit()


if __name__ == "__main__":
    main()
