import json
import math
import random
from array import array
from collections import deque
from datetime import datetime
from pathlib import Path

import pygame


WIDTH = 1152
HEIGHT = 700
HUD_HEIGHT = 60
GRID_ROWS = 40
GRID_COLS = 72
CELL_WIDTH = WIDTH / GRID_COLS
CELL_HEIGHT = (HEIGHT - HUD_HEIGHT) / GRID_ROWS
BOARD_TOP = HUD_HEIGHT
BOARD_HEIGHT = HEIGHT - HUD_HEIGHT

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
WALL_COLOR = (83, 96, 111)
WALL_EDGE = (49, 59, 72)
PORTAL_COLOR = (74, 225, 214)
PORTAL_CORE = (11, 31, 39)
PAUSE_BUTTON_RECT = pygame.Rect(842, 10, 132, 40)
RESUME_BUTTON_RECT = pygame.Rect(986, 10, 148, 40)

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
    },
    {
        "name": "中等",
        "interval": 120,
        "speed": 8.3,
        "color": (241, 181, 57),
        "text_color": (54, 37, 3),
    },
    {
        "name": "很难",
        "interval": 70,
        "speed": 14.3,
        "color": (225, 76, 76),
        "text_color": (255, 245, 245),
    },
]

pygame.mixer.pre_init(44100, -16, 2, 512)
pygame.init()
AUDIO_ENABLED = pygame.mixer.get_init() is not None
SCREEN = pygame.display.set_mode((WIDTH, HEIGHT))
pygame.display.set_caption("贪吃蛇 - 墙体挑战")
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


class Point:
    def __init__(self, col, row):
        self.col = col
        self.row = row

    def copy(self):
        return Point(row=self.row, col=self.col)


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


def boundary_cells():
    cells = set()
    for row in range(GRID_ROWS):
        cells.add((row, 0))
        cells.add((row, GRID_COLS - 1))
    for col in range(GRID_COLS):
        cells.add((0, col))
        cells.add((GRID_ROWS - 1, col))
    return cells


def random_portal_pair():
    candidates = [
        (row, col)
        for row, col in boundary_cells()
        if not (
            row in (0, GRID_ROWS - 1)
            and col in (0, GRID_COLS - 1)
        )
    ]
    return tuple(random.sample(candidates, 2))


def portal_exit_cell(portal):
    row, col = portal
    if row == 0:
        return (1, col)
    if row == GRID_ROWS - 1:
        return (GRID_ROWS - 2, col)
    if col == 0:
        return (row, 1)
    return (row, GRID_COLS - 2)


def portal_entry_direction(portal):
    row, col = portal
    if row == 0:
        return "down"
    if row == GRID_ROWS - 1:
        return "up"
    if col == 0:
        return "right"
    return "left"


def initial_walls(portals):
    walls = boundary_cells()
    blocks = [
        (5, 14, 12, 2),
        (23, 14, 11, 2),
        (5, 52, 12, 2),
        (23, 52, 11, 2),
        (14, 23, 2, 12),
        (27, 32, 2, 12),
    ]
    for start_row, start_col, height, width in blocks:
        for row in range(start_row, start_row + height):
            for col in range(start_col, start_col + width):
                walls.add((row, col))
    walls.difference_update(portals)
    return walls


class SnakeGame:
    def __init__(self, skin, difficulty):
        self.skin = skin
        self.difficulty = difficulty
        self.portals = random_portal_pair()
        self.walls = initial_walls(self.portals)
        self.head = Point(row=GRID_ROWS // 2, col=GRID_COLS // 2)
        self.snake = [
            Point(row=self.head.row, col=self.head.col + 1),
            Point(row=self.head.row, col=self.head.col + 2),
            Point(row=self.head.row, col=self.head.col + 3),
        ]
        self.direction = "left"
        self.next_direction = "left"
        self.score = 0
        self.food_eaten = 0
        self.food = self.create_food()
        self.last_move = pygame.time.get_ticks()
        self.dead_reason = ""
        self.notice_message = ""
        self.notice_started_at = 0
        self.notice_duration = 0
        self.notice_color = ACCENT
        self.paused = False
        self.show_notice("游戏开始！方向键控制移动", ACCENT, 2400)

    def show_notice(self, message, color=ACCENT, duration=1800):
        self.notice_message = message
        self.notice_color = color
        self.notice_started_at = pygame.time.get_ticks()
        self.notice_duration = duration

    def create_food(self):
        occupied = {(self.head.row, self.head.col)}
        occupied.update((body.row, body.col) for body in self.snake)
        occupied.update(self.walls)
        occupied.update(self.portals)
        occupied.update(portal_exit_cell(portal) for portal in self.portals)
        free_cells = [
            (row, col)
            for row in range(GRID_ROWS)
            for col in range(GRID_COLS)
            if (row, col) not in occupied
        ]
        if not free_cells:
            return None
        row, col = random.choice(free_cells)
        return Point(row=row, col=col)

    def turn(self, direction):
        if self.next_direction != self.direction:
            return
        opposite = {
            "up": "down",
            "down": "up",
            "left": "right",
            "right": "left",
        }
        if direction != opposite[self.direction]:
            self.next_direction = direction

    def set_paused(self, paused):
        if self.paused == paused:
            return
        self.paused = paused
        if not paused:
            self.last_move = pygame.time.get_ticks()

    def food_is_reachable(self, walls, portals=None):
        if self.food is None:
            return False

        portals = portals or self.portals
        portal_exits = [portal_exit_cell(portal) for portal in portals]
        target = (self.food.row, self.food.col)
        start = (self.head.row, self.head.col)
        queue = deque([start])
        visited = {start}
        directions = ((1, 0), (-1, 0), (0, 1), (0, -1))

        while queue:
            row, col = queue.popleft()
            if (row, col) == target:
                return True
            if (row, col) == portal_exits[0] and portal_exits[1] not in visited:
                visited.add(portal_exits[1])
                queue.append(portal_exits[1])
            elif (row, col) == portal_exits[1] and portal_exits[0] not in visited:
                visited.add(portal_exits[0])
                queue.append(portal_exits[0])
            for row_delta, col_delta in directions:
                next_row = row + row_delta
                next_col = col + col_delta
                next_cell = (next_row, next_col)
                if (
                    0 <= next_row < GRID_ROWS
                    and 0 <= next_col < GRID_COLS
                    and next_cell not in walls
                    and next_cell not in visited
                ):
                    visited.add(next_cell)
                    queue.append(next_cell)
        return False

    def regenerate_walls(self):
        protected = {(self.head.row, self.head.col)}
        protected.update((body.row, body.col) for body in self.snake)
        if self.food is not None:
            protected.add((self.food.row, self.food.col))

        for row in range(self.head.row - 2, self.head.row + 3):
            for col in range(self.head.col - 2, self.head.col + 3):
                protected.add((row, col))

        for _ in range(120):
            candidate_portals = random_portal_pair()
            portal_safe = set(candidate_portals)
            portal_safe.update(
                portal_exit_cell(portal) for portal in candidate_portals
            )
            if self.food is not None and (self.food.row, self.food.col) in portal_safe:
                continue

            candidate = boundary_cells()
            candidate.difference_update(candidate_portals)
            interior_count = 0
            for _ in range(random.randint(8, 11)):
                height = random.randint(2, 5)
                width = random.randint(4, 16)
                start_row = random.randint(2, GRID_ROWS - height - 3)
                start_col = random.randint(2, GRID_COLS - width - 3)
                block = {
                    (row, col)
                    for row in range(start_row, start_row + height)
                    for col in range(start_col, start_col + width)
                }
                if block.isdisjoint(protected | portal_safe):
                    previous_count = len(candidate)
                    candidate.update(block)
                    interior_count += len(candidate) - previous_count

            if 80 <= interior_count <= 300 and self.food_is_reachable(
                candidate,
                candidate_portals,
            ):
                self.portals = candidate_portals
                self.walls = candidate
                return

    def update(self):
        self.direction = self.next_direction
        next_head = self.head.copy()
        if self.direction == "left":
            next_head.col -= 1
        elif self.direction == "right":
            next_head.col += 1
        elif self.direction == "up":
            next_head.row -= 1
        elif self.direction == "down":
            next_head.row += 1

        next_cell = (next_head.row, next_head.col)
        if next_cell in self.portals:
            portal_index = self.portals.index(next_cell)
            exit_portal = self.portals[1 - portal_index]
            exit_row, exit_col = portal_exit_cell(exit_portal)
            next_head = Point(row=exit_row, col=exit_col)
            exit_direction = portal_entry_direction(exit_portal)
            self.direction = exit_direction
            self.next_direction = exit_direction

        eat = (
            self.food is not None
            and next_head.row == self.food.row
            and next_head.col == self.food.col
        )
        body_to_check = self.snake if eat else self.snake[:-1]

        if not (0 <= next_head.col < GRID_COLS and 0 <= next_head.row < GRID_ROWS):
            return "撞到了边界墙！"
        if (next_head.row, next_head.col) in self.walls:
            return "撞到了墙体！"
        if any(
            body.row == next_head.row and body.col == next_head.col
            for body in body_to_check
        ):
            return "撞到了自己的身体！"

        self.snake.insert(0, self.head.copy())
        if not eat:
            self.snake.pop()
        self.head = next_head

        if eat:
            play_sound(EAT_SOUND)
            self.score += 10
            self.food_eaten += 1
            self.food = self.create_food()
            if self.food is None:
                return "你填满了整个地图！"
            if self.food_eaten % 5 == 0:
                self.regenerate_walls()
                self.show_notice(
                    "身体变大！墙体与传送口已变化！",
                    (244, 179, 65),
                    2900,
                )
            else:
                self.show_notice(
                    "吃到食物！身体变大，长度 +1",
                    (82, 213, 160),
                    2100,
                )
        return ""

    def draw(self):
        SCREEN.fill((18, 31, 42))
        pygame.draw.rect(
            SCREEN,
            BOARD_COLOR,
            (0, BOARD_TOP, WIDTH, BOARD_HEIGHT),
        )
        for row, col in self.walls:
            rect = pygame.Rect(
                int(col * CELL_WIDTH),
                int(BOARD_TOP + row * CELL_HEIGHT),
                math.ceil(CELL_WIDTH),
                math.ceil(CELL_HEIGHT),
            )
            pygame.draw.rect(SCREEN, WALL_COLOR, rect)
            pygame.draw.rect(SCREEN, WALL_EDGE, rect, 1)

        for portal in self.portals:
            row, col = portal
            rect = pygame.Rect(
                int(col * CELL_WIDTH),
                int(BOARD_TOP + row * CELL_HEIGHT),
                math.ceil(CELL_WIDTH),
                math.ceil(CELL_HEIGHT),
            )
            center = rect.center
            pygame.draw.rect(SCREEN, PORTAL_CORE, rect)
            pygame.draw.circle(SCREEN, PORTAL_COLOR, center, 7)
            pygame.draw.circle(SCREEN, PORTAL_CORE, center, 4)

        if self.food is not None:
            center = (
                int((self.food.col + 0.5) * CELL_WIDTH),
                int(BOARD_TOP + (self.food.row + 0.5) * CELL_HEIGHT),
            )
            pygame.draw.circle(SCREEN, (126, 78, 14), center, 7)
            pygame.draw.circle(SCREEN, FOOD_COLOR, center, 6)

        self.draw_snake()
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

        center = (WIDTH // 2, BOARD_TOP + BOARD_HEIGHT // 2)
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
            "点击右上角“继续游戏”或按空格键继续",
            18,
            MUTED_TEXT,
            (WIDTH // 2, panel.y + 104),
        )

    def body_thickness(self):
        minimum = 8.0
        maximum = min(CELL_WIDTH, CELL_HEIGHT) - 2
        growth = min(1.0, self.food_eaten / 15)
        return minimum + (maximum - minimum) * growth

    def draw_snake(self):
        thickness = int(round(self.body_thickness()))
        centers = [
            (
                int((self.head.col + 0.5) * CELL_WIDTH),
                int(BOARD_TOP + (self.head.row + 0.5) * CELL_HEIGHT),
            )
        ]
        centers.extend(
            (
                int((body.col + 0.5) * CELL_WIDTH),
                int(BOARD_TOP + (body.row + 0.5) * CELL_HEIGHT),
            )
            for body in self.snake
        )

        for index in range(len(centers) - 1):
            first = centers[index]
            second = centers[index + 1]
            if abs(first[0] - second[0]) + abs(first[1] - second[1]) > CELL_WIDTH * 1.5:
                continue
            pygame.draw.line(
                SCREEN,
                self.skin["outline"],
                first,
                second,
                thickness + 4,
            )
        for index in range(len(centers) - 1):
            first = centers[index]
            second = centers[index + 1]
            if abs(first[0] - second[0]) + abs(first[1] - second[1]) > CELL_WIDTH * 1.5:
                continue
            pygame.draw.line(
                SCREEN,
                mix_color(self.skin["body_dark"], self.skin["body"], 0.7),
                first,
                second,
                thickness,
            )

        radius = max(3, thickness // 2)
        for index, center in enumerate(centers[1:]):
            band = (index % 4) / 3
            body_color = mix_color(
                self.skin["body_dark"],
                self.skin["body"],
                0.55 + band * 0.45,
            )
            pygame.draw.circle(SCREEN, body_color, center, radius)
            highlight_center = (
                center[0] - max(1, radius // 3),
                center[1] - max(1, radius // 3),
            )
            pygame.draw.circle(
                SCREEN,
                self.skin["highlight"],
                highlight_center,
                max(1, radius // 4),
            )

        tail = centers[-1]
        pygame.draw.circle(SCREEN, self.skin["outline"], tail, radius + 2)
        pygame.draw.circle(
            SCREEN,
            mix_color(self.skin["body_dark"], self.skin["body"], 0.35),
            tail,
            radius,
        )

        head_long = min(int(CELL_WIDTH) + 2, thickness + 7)
        head_short = min(int(CELL_HEIGHT) - 2, thickness + 3)
        if self.direction in ("left", "right"):
            head_rect = pygame.Rect(0, 0, head_long, head_short)
        else:
            head_rect = pygame.Rect(0, 0, head_short, head_long)
        head_rect.center = centers[0]
        pygame.draw.ellipse(
            SCREEN,
            self.skin["outline"],
            head_rect.inflate(5, 5),
        )
        pygame.draw.ellipse(
            SCREEN,
            self.skin["head"],
            head_rect,
        )
        snout_rect = head_rect.inflate(-max(2, head_rect.w // 3), -max(2, head_rect.h // 3))
        snout_rect.center = (
            head_rect.centerx + (
                2 if self.direction == "right"
                else -2 if self.direction == "left"
                else 0
            ),
            head_rect.centery + (
                2 if self.direction == "down"
                else -2 if self.direction == "up"
                else 0
            ),
        )
        pygame.draw.ellipse(
            SCREEN,
            mix_color(self.skin["head"], self.skin["highlight"], 0.24),
            snout_rect,
        )

        center_x, center_y = head_rect.center
        eye_offset = max(2, head_short // 5)
        eye_radius = max(2, head_short // 5)
        pupil_radius = max(1, eye_radius // 2)
        if self.direction == "left":
            eyes = (
                (center_x - eye_offset, center_y - eye_offset),
                (center_x - eye_offset, center_y + eye_offset),
            )
            pupil_shift = (-1, 0)
        elif self.direction == "right":
            eyes = (
                (center_x + eye_offset, center_y - eye_offset),
                (center_x + eye_offset, center_y + eye_offset),
            )
            pupil_shift = (1, 0)
        elif self.direction == "up":
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
        if self.direction == "left":
            tongue_start = (head_rect.left, center_y)
            tongue_tip = (tongue_start[0] - tongue_length, center_y)
            forks = (
                (tongue_tip[0] - 2, tongue_tip[1] - 2),
                (tongue_tip[0] - 2, tongue_tip[1] + 2),
            )
        elif self.direction == "right":
            tongue_start = (head_rect.right, center_y)
            tongue_tip = (tongue_start[0] + tongue_length, center_y)
            forks = (
                (tongue_tip[0] + 2, tongue_tip[1] - 2),
                (tongue_tip[0] + 2, tongue_tip[1] + 2),
            )
        elif self.direction == "up":
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
        pygame.draw.line(SCREEN, self.skin["tongue"], tongue_start, tongue_tip, 2)
        pygame.draw.line(SCREEN, self.skin["tongue"], tongue_tip, forks[0], 1)
        pygame.draw.line(SCREEN, self.skin["tongue"], tongue_tip, forks[1], 1)

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
        draw_left_text(
            f"身体长度 {len(self.snake) + 1}  ·  体型 {self.food_eaten + 1} 级",
            21,
            TEXT_COLOR,
            (230, 18),
            bold=True,
        )
        draw_left_text(
            f"皮肤：{self.skin['name']}",
            19,
            MUTED_TEXT,
            (470, 19),
        )
        draw_left_text(
            f"难度：{self.difficulty['name']}",
            19,
            self.difficulty["color"],
            (650, 19),
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
    draw_text("边界墙体 · 双向传送口 · 每 5 个食物随机换墙", 21, MUTED_TEXT, (WIDTH // 2, 118))

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

    draw_text("方向键控制 · ESC 返回主页", 18, MUTED_TEXT, (WIDTH // 2, 660))
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
    draw_text("难度越高，蛇移动速度越快", 20, MUTED_TEXT, (WIDTH // 2, 101))

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

        bar_left = card.x + 38
        bar_top = card.y + 180
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
            draw_text("已选择", 20, difficulty["color"], (card.centerx, card.y + 235), bold=True)
        else:
            draw_text("点击选择", 19, MUTED_TEXT, (card.centerx, card.y + 235))

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
        f"难度：{game.difficulty['name']}    "
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
                    elif event.key == pygame.K_UP:
                        game.turn("up")
                    elif event.key == pygame.K_DOWN:
                        game.turn("down")
                    elif event.key == pygame.K_LEFT:
                        game.turn("left")
                    elif event.key == pygame.K_RIGHT:
                        game.turn("right")
                elif event.type == pygame.MOUSEBUTTONDOWN and event.button == 1:
                    if (
                        not game.paused
                        and PAUSE_BUTTON_RECT.collidepoint(event.pos)
                    ):
                        game.set_paused(True)
                    elif (
                        game.paused
                        and RESUME_BUTTON_RECT.collidepoint(event.pos)
                    ):
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
