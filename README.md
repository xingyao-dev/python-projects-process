# python-projects-process

A Pygame snake game with a classic mode and a 5-team competition mode.

## Features

- **Classic mode**: 80x80 scrolling arena, AI rival snakes, food clearing and reinforcement rules, 10 classic avatar skins.
- **Team mode**: 5 teams x 5 snakes, 5-minute score match, larger 120x120 arena, red / blue / green / black / white team body colors.
- **Team rosters**: 12 zodiac skins, 12 Boonie Bears characters, 12 Pleasant Goat and Big Big Wolf characters, 12 GG Bond characters, 12 Ultraman characters.
- **Collision rules**: hitting your own body is safe; in team mode, teammates can pass through each other; hitting an enemy body or an enemy head-on eliminates that snake.
- **Readable selection screens**: large avatar portraits with name badges, group labels, and back buttons on every team/character page. Portraits use procedural Live2D-style idle motion (breathing, sway, blinking); optional licensed PNG portraits can be dropped into `assets/portraits/`.
- **Controls**: mouse joystick, arrow keys / WASD, Q/E/Z/C diagonals, P or Space to pause. The pause menu has resume and exit buttons; ESC also returns to the previous screen.
- **Team results**: winning team, every team's total score and top 3 players, plus the winning team's top 5 players.

## Run

```bash
pip install pygame
python "game_greed snake.py"
```

## Build

```bash
pyinstaller "game_greed snake.spec"
```
