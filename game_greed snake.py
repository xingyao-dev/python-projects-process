import json
import math
import random
from collections import deque
from datetime import datetime
from pathlib import Path

import pygame


WIDTH = 1280
HEIGHT = 860
HUD_HEIGHT = 60
GRID_ROWS = 50
GRID_COLS = 80
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

SKINS = [
    {
        "name": "红蛇",
        "body": (225, 69, 73),
        "head": (184, 35, 42),
        "outline": (105, 24, 29),
    },
    {
        "name": "黄蛇",
        "body": (246, 199, 63),
        "head": (218, 160, 27),
        "outline": (128, 91, 15),
    },
    {
        "name": "蓝蛇",
        "body": (61, 139, 235),
        "head": (35, 104, 202),
        "outline": (22, 63, 125),
    },
    {
        "name": "绿蛇",
        "body": (63, 187, 105),
        "head": (33, 144, 74),
        "outline": (20, 83, 44),
    },
    {
        "name": "黑蛇",
        "body": (44, 49, 57),
        "head": (18, 21, 25),
        "outline": (0, 0, 0),
    },
]

pygame.init()
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


def draw_button(rect, label, mouse_pos, color=ACCENT, text_color=(10, 33, 26)):
    hovered = rect.collidepoint(mouse_pos)
    button_color = lighten(color, 24) if hovered else color
    shadow_rect = rect.move(0, 5)
    pygame.draw.rect(SCREEN, (9, 20, 28), shadow_rect, border_radius=14)
    pygame.draw.rect(SCREEN, button_color, rect, border_radius=14)
    pygame.draw.rect(SCREEN, lighten(color, 45), rect, 2, border_radius=14)
    draw_text(label, 25, text_color, rect.center, bold=True)


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
    center_x, center_y = center
    span = spacing * (length - 1)
    points = []
    for index in range(length):
        x = center_x - span / 2 + index * spacing
        y = center_y + math.sin(index * 0.72) * amplitude
        points.append((int(x), int(y)))

    for index, point in enumerate(points[:-1]):
        pygame.draw.circle(
            SCREEN,
            skin["outline"],
            point,
            radius + 3,
        )
        pygame.draw.circle(
            SCREEN,
            skin["body"] if index % 2 == 0 else lighten(skin["body"], 12),
            point,
            radius,
        )

    head_x, head_y = points[-1]
    pygame.draw.circle(SCREEN, skin["outline"], (head_x, head_y), radius + 6)
    pygame.draw.circle(SCREEN, skin["head"], (head_x, head_y), radius + 3)
    pygame.draw.circle(SCREEN, TEXT_COLOR, (head_x + 5, head_y - 5), 3)
    pygame.draw.circle(SCREEN, TEXT_COLOR, (head_x + 5, head_y + 5), 3)


def initial_walls():
    walls = set()
    blocks = [
        (6, 18, 16, 2),
        (29, 18, 15, 2),
        (6, 60, 16, 2),
        (29, 60, 15, 2),
        (17, 28, 2, 14),
        (33, 38, 2, 14),
    ]
    for start_row, start_col, height, width in blocks:
        for row in range(start_row, start_row + height):
            for col in range(start_col, start_col + width):
                walls.add((row, col))
    return walls


class SnakeGame:
    def __init__(self, skin):
        self.skin = skin
        self.walls = initial_walls()
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
        self.walls_changed_at = None
        self.dead_reason = ""

    def create_food(self):
        occupied = {(self.head.row, self.head.col)}
        occupied.update((body.row, body.col) for body in self.snake)
        occupied.update(self.walls)
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

    def food_is_reachable(self, walls):
        if self.food is None:
            return False

        target = (self.food.row, self.food.col)
        start = (self.head.row, self.head.col)
        queue = deque([start])
        visited = {start}
        directions = ((1, 0), (-1, 0), (0, 1), (0, -1))

        while queue:
            row, col = queue.popleft()
            if (row, col) == target:
                return True
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
            candidate = set()
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
                if block.isdisjoint(protected):
                    candidate.update(block)

            if 80 <= len(candidate) <= 300 and self.food_is_reachable(candidate):
                self.walls = candidate
                self.walls_changed_at = pygame.time.get_ticks()
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
            self.score += 10
            self.food_eaten += 1
            self.food = self.create_food()
            if self.food is None:
                return "你填满了整个地图！"
            if self.food_eaten % 5 == 0:
                self.regenerate_walls()
        return ""

    def draw(self):
        SCREEN.fill((18, 31, 42))
        pygame.draw.rect(
            SCREEN,
            BOARD_COLOR,
            (0, BOARD_TOP, WIDTH, BOARD_HEIGHT),
        )
        pygame.draw.rect(
            SCREEN,
            WALL_EDGE,
            (0, BOARD_TOP, WIDTH, BOARD_HEIGHT),
            4,
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

        if self.food is not None:
            center = (
                int((self.food.col + 0.5) * CELL_WIDTH),
                int(BOARD_TOP + (self.food.row + 0.5) * CELL_HEIGHT),
            )
            pygame.draw.circle(SCREEN, (126, 78, 14), center, 7)
            pygame.draw.circle(SCREEN, FOOD_COLOR, center, 6)

        self.draw_snake()
        self.draw_hud()

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
            pygame.draw.line(
                SCREEN,
                self.skin["outline"],
                centers[index],
                centers[index + 1],
                thickness + 4,
            )
        for index in range(len(centers) - 1):
            pygame.draw.line(
                SCREEN,
                self.skin["body"],
                centers[index],
                centers[index + 1],
                thickness,
            )

        for index, center in enumerate(centers[1:]):
            radius = max(3, thickness // 2)
            pygame.draw.circle(SCREEN, self.skin["outline"], center, radius + 2)
            body_color = (
                lighten(self.skin["body"], 12)
                if index % 2 == 0
                else self.skin["body"]
            )
            pygame.draw.circle(SCREEN, body_color, center, radius)

        head_size = min(int(CELL_WIDTH) - 2, thickness + 4)
        head_rect = pygame.Rect(0, 0, head_size, head_size)
        head_rect.center = centers[0]
        pygame.draw.rect(
            SCREEN,
            self.skin["outline"],
            head_rect.inflate(4, 4),
            border_radius=6,
        )
        pygame.draw.rect(
            SCREEN,
            self.skin["head"],
            head_rect,
            border_radius=5,
        )

        center_x, center_y = head_rect.center
        eye_offset = max(2, head_size // 5)
        eye_radius = max(1, head_size // 8)
        eye_color = (245, 249, 250)
        if self.direction == "left":
            eyes = (
                (center_x - eye_offset, center_y - eye_offset),
                (center_x - eye_offset, center_y + eye_offset),
            )
        elif self.direction == "right":
            eyes = (
                (center_x + eye_offset, center_y - eye_offset),
                (center_x + eye_offset, center_y + eye_offset),
            )
        elif self.direction == "up":
            eyes = (
                (center_x - eye_offset, center_y - eye_offset),
                (center_x + eye_offset, center_y - eye_offset),
            )
        else:
            eyes = (
                (center_x - eye_offset, center_y + eye_offset),
                (center_x + eye_offset, center_y + eye_offset),
            )
        for eye in eyes:
            pygame.draw.circle(SCREEN, eye_color, eye, eye_radius)

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
            (620, 19),
        )

        if self.walls_changed_at is not None:
            elapsed = pygame.time.get_ticks() - self.walls_changed_at
            if elapsed < 1800:
                message = pygame.Surface((242, 42), pygame.SRCALPHA)
                message.fill((22, 126, 92, 225))
                SCREEN.blit(message, (WIDTH - 258, 9))
                pygame.draw.rect(
                    SCREEN,
                    (100, 230, 188),
                    (WIDTH - 258, 9, 242, 42),
                    1,
                    border_radius=10,
                )
                draw_text(
                    "墙体已随机变化！",
                    20,
                    TEXT_COLOR,
                    (WIDTH - 137, 30),
                    bold=True,
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


def draw_home(selected_skin, scores, mouse_pos):
    draw_menu_background()
    draw_text("贪 吃 蛇", 78, TEXT_COLOR, (WIDTH // 2, 88), bold=True)
    draw_text("撞墙即死亡 · 每吃 5 个食物墙体随机变化", 24, MUTED_TEXT, (WIDTH // 2, 148))

    draw_snake_art(
        (WIDTH // 2, 320),
        selected_skin,
        length=16,
        spacing=24,
        radius=16,
        amplitude=23,
    )

    selected_label = f"当前皮肤：{selected_skin['name']}"
    draw_text(selected_label, 23, MUTED_TEXT, (WIDTH // 2, 422))

    start_rect = pygame.Rect(430, 476, 200, 68)
    skin_rect = pygame.Rect(650, 476, 200, 68)
    draw_button(start_rect, "开始游戏", mouse_pos)
    draw_button(skin_rect, "换皮肤", mouse_pos, color=(77, 135, 197), text_color=(244, 249, 252))

    if scores:
        high_score = scores[0]["score"]
        draw_text(f"历史最高分：{high_score}", 24, (255, 226, 145), (WIDTH // 2, 598))
    else:
        draw_text("还没有游戏记录，来创造第一条成绩吧", 21, MUTED_TEXT, (WIDTH // 2, 598))

    draw_text("方向键控制 · ESC 返回主页", 20, MUTED_TEXT, (WIDTH // 2, 810))
    return start_rect, skin_rect


def skin_card_rects():
    card_width = 190
    gap = 24
    total_width = len(SKINS) * card_width + (len(SKINS) - 1) * gap
    start_x = (WIDTH - total_width) // 2
    return [
        pygame.Rect(start_x + index * (card_width + gap), 155, card_width, 355)
        for index in range(len(SKINS))
    ]


def draw_skin_page(selected_index, mouse_pos):
    draw_menu_background()
    draw_text("选择蛇的皮肤", 58, TEXT_COLOR, (WIDTH // 2, 75), bold=True)
    draw_text("点击卡片切换颜色", 22, MUTED_TEXT, (WIDTH // 2, 122))

    cards = skin_card_rects()
    for index, (card, skin) in enumerate(zip(cards, SKINS)):
        selected = index == selected_index
        hovered = card.collidepoint(mouse_pos)
        card_color = (37, 62, 83) if hovered else PANEL_COLOR
        border_color = ACCENT if selected else PANEL_BORDER
        pygame.draw.rect(SCREEN, card_color, card, border_radius=16)
        pygame.draw.rect(SCREEN, border_color, card, 4 if selected else 2, border_radius=16)

        draw_snake_art(
            (card.centerx, card.y + 112),
            skin,
            length=10,
            spacing=12,
            radius=8,
            amplitude=9,
        )
        draw_text(skin["name"], 30, TEXT_COLOR, (card.centerx, card.y + 236), bold=True)
        if selected:
            draw_text("已选择", 22, ACCENT, (card.centerx, card.y + 290), bold=True)
        else:
            draw_text("点击选择", 21, MUTED_TEXT, (card.centerx, card.y + 290))

    start_rect = pygame.Rect(475, 575, 170, 66)
    back_rect = pygame.Rect(665, 575, 140, 66)
    draw_button(start_rect, "开始游戏", mouse_pos)
    draw_button(back_rect, "返回", mouse_pos, color=(86, 112, 132), text_color=TEXT_COLOR)
    return cards, start_rect, back_rect


def draw_game_over(game, scores, current_entry, rank, mouse_pos):
    draw_menu_background()
    panel = pygame.Rect(160, 55, 960, 650)
    pygame.draw.rect(SCREEN, (20, 35, 50), panel, border_radius=22)
    pygame.draw.rect(SCREEN, PANEL_BORDER, panel, 2, border_radius=22)

    draw_text("游 戏 结 束", 52, (255, 124, 117), (WIDTH // 2, 105), bold=True)
    draw_text(game.dead_reason, 24, MUTED_TEXT, (WIDTH // 2, 151))

    summary = f"本局分数：{game.score}    身体长度：{len(game.snake) + 1}    排名：第 {rank} 名"
    draw_text(summary, 27, (255, 226, 145), (WIDTH // 2, 194), bold=True)
    if rank == 1 and game.score > 0:
        draw_text("新纪录！", 22, ACCENT, (WIDTH // 2, 230), bold=True)

    draw_text("本地排行榜 TOP 5", 25, TEXT_COLOR, (WIDTH // 2, 268), bold=True)
    draw_left_text("名次", 19, MUTED_TEXT, (panel.x + 75, 300), bold=True)
    draw_left_text("分数", 19, MUTED_TEXT, (panel.x + 185, 300), bold=True)
    draw_left_text("长度", 19, MUTED_TEXT, (panel.x + 315, 300), bold=True)
    draw_left_text("皮肤", 19, MUTED_TEXT, (panel.x + 445, 300), bold=True)
    draw_left_text("时间", 19, MUTED_TEXT, (panel.x + 600, 300), bold=True)

    top_scores = scores[:5]
    for index, item in enumerate(top_scores):
        row_rect = pygame.Rect(panel.x + 55, 335 + index * 48, panel.w - 110, 39)
        is_current = item == current_entry
        if is_current:
            pygame.draw.rect(SCREEN, (41, 91, 75), row_rect, border_radius=8)

        row_color = TEXT_COLOR if is_current else (205, 219, 225)
        row_y = row_rect.centery - 11
        draw_left_text(str(index + 1), 20, row_color, (panel.x + 86, row_y))
        draw_left_text(str(item["score"]), 20, row_color, (panel.x + 190, row_y))
        draw_left_text(str(item["length"]), 20, row_color, (panel.x + 322, row_y))
        draw_left_text(item["skin"], 20, row_color, (panel.x + 445, row_y))
        draw_left_text(item["date"][5:], 20, row_color, (panel.x + 600, row_y))

    if not top_scores:
        draw_text("暂无记录", 21, MUTED_TEXT, (WIDTH // 2, 415))

    replay_rect = pygame.Rect(455, 742, 170, 62)
    home_rect = pygame.Rect(655, 742, 170, 62)
    draw_button(replay_rect, "再来一局", mouse_pos)
    draw_button(home_rect, "返回主页", mouse_pos, color=(86, 112, 132), text_color=TEXT_COLOR)
    return replay_rect, home_rect


def main():
    running = True
    state = "home"
    selected_index = 0
    game = None
    scores = load_scores()
    current_entry = None
    current_rank = 0

    while running:
        mouse_pos = pygame.mouse.get_pos()

        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                running = False
                continue

            if state == "home":
                if event.type == pygame.MOUSEBUTTONDOWN and event.button == 1:
                    start_rect, skin_rect = draw_home(
                        SKINS[selected_index], scores, mouse_pos
                    )
                    if start_rect.collidepoint(event.pos):
                        game = SnakeGame(SKINS[selected_index])
                        state = "playing"
                    elif skin_rect.collidepoint(event.pos):
                        state = "skins"

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
                        game = SnakeGame(SKINS[selected_index])
                        state = "playing"
                    elif back_rect.collidepoint(event.pos):
                        state = "home"
                elif event.type == pygame.KEYDOWN and event.key == pygame.K_ESCAPE:
                    state = "home"

            elif state == "playing":
                if event.type == pygame.KEYDOWN:
                    if event.key == pygame.K_ESCAPE:
                        state = "home"
                    elif event.key == pygame.K_UP:
                        game.turn("up")
                    elif event.key == pygame.K_DOWN:
                        game.turn("down")
                    elif event.key == pygame.K_LEFT:
                        game.turn("left")
                    elif event.key == pygame.K_RIGHT:
                        game.turn("right")

            elif state == "game_over":
                if event.type == pygame.KEYDOWN and event.key in (
                    pygame.K_RETURN,
                    pygame.K_SPACE,
                ):
                    game = SnakeGame(SKINS[selected_index])
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
                        game = SnakeGame(SKINS[selected_index])
                        state = "playing"
                    elif home_rect.collidepoint(event.pos):
                        state = "home"

        if state == "playing":
            now = pygame.time.get_ticks()
            if now - game.last_move >= 180:
                game.last_move = now
                dead_reason = game.update()
                if dead_reason:
                    game.dead_reason = dead_reason
                    scores, current_entry, current_rank = record_score(game)
                    state = "game_over"

        if state == "home":
            draw_home(SKINS[selected_index], scores, mouse_pos)
        elif state == "skins":
            draw_skin_page(selected_index, mouse_pos)
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
