import os
import random
import sys

import pygame

WIDTH = 400
HEIGHT = 400
CELL = 20
FPS = 10

STATE_START = "start"
STATE_CONTROLS = "controls"
STATE_SKIN_SELECT = "skin_select"
STATE_PLAYING = "playing"
STATE_GAME_OVER = "game_over"

BACKGROUND_FILES = {
    STATE_START: "start_background.png",
    STATE_CONTROLS: "controls_background.png",
    STATE_SKIN_SELECT: "skin_background.png",
    STATE_PLAYING: "game_background.png",
    STATE_GAME_OVER: "game_over_background.png",
}

COLOR_PRESETS = [
    {"name": "Emerald", "color": (34, 177, 76), "accent": (0, 100, 0)},
    {"name": "Sunset", "color": (255, 127, 39), "accent": (200, 80, 0)},
    {"name": "Ocean", "color": (0, 162, 232), "accent": (0, 90, 160)},
    {"name": "Violet", "color": (163, 73, 164), "accent": (120, 20, 120)},
    {"name": "Gold", "color": (255, 201, 14), "accent": (180, 140, 0)},
]

PLAYER_CONTROLS = {
    1: {
        pygame.K_w: (0, -CELL),
        pygame.K_s: (0, CELL),
        pygame.K_a: (-CELL, 0),
        pygame.K_d: (CELL, 0),
    },
    2: {
        pygame.K_UP: (0, -CELL),
        pygame.K_DOWN: (0, CELL),
        pygame.K_LEFT: (-CELL, 0),
        pygame.K_RIGHT: (CELL, 0),
    },
}


def resource_path(filename):
    base = os.path.dirname(os.path.abspath(__file__))
    return os.path.join(base, filename)


def load_background(filename, fallback_color):
    path = resource_path(filename)
    if os.path.isfile(path):
        image = pygame.image.load(path).convert()
        return pygame.transform.scale(image, (WIDTH, HEIGHT))
    surface = pygame.Surface((WIDTH, HEIGHT))
    surface.fill(fallback_color)
    return surface


def draw_text(surface, text, size, position, color=(255, 255, 255), center=False):
    font = pygame.font.SysFont(None, size)
    rendered = font.render(text, True, color)
    rect = rendered.get_rect()
    if center:
        rect.center = position
    else:
        rect.topleft = position
    surface.blit(rendered, rect)


class Snake:
    def __init__(self, body, direction, skin_index=0):
        self.body = list(body)
        self.direction = direction
        self.grow_pending = 0
        self.skin_index = skin_index

    def head(self):
        return self.body[0]

    def update_direction(self, new_direction):
        if (new_direction[0] * -1, new_direction[1] * -1) != self.direction:
            self.direction = new_direction

    def move(self):
        new_head = (self.head()[0] + self.direction[0], self.head()[1] + self.direction[1])
        self.body.insert(0, new_head)
        if self.grow_pending > 0:
            self.grow_pending -= 1
        else:
            self.body.pop()

    def grow(self):
        self.grow_pending += 1

    def collides_with_self(self):
        return self.head() in self.body[1:]

    def collides_with_point(self, point):
        return point in self.body

    def draw(self, surface):
        preset = COLOR_PRESETS[self.skin_index % len(COLOR_PRESETS)]
        body_color = preset["color"]
        accent_color = preset["accent"]
        for index, segment in enumerate(self.body):
            color = accent_color if index == 0 else body_color
            pygame.draw.rect(surface, color, pygame.Rect(segment[0], segment[1], CELL, CELL))
            pygame.draw.rect(surface, (0, 0, 0), pygame.Rect(segment[0], segment[1], CELL, CELL), 1)


def random_food_position(snakes):
    positions = {segment for snake in snakes for segment in snake.body}
    while True:
        position = (random.randrange(0, WIDTH, CELL), random.randrange(0, HEIGHT, CELL))
        if position not in positions:
            return position


def reset_game(mode, colors):
    snake1 = Snake([(100, 100), (80, 100), (60, 100)], (CELL, 0), skin_index=colors[0])
    snakes = [snake1]
    if mode == 2:
        snake2 = Snake([(100, 300), (120, 300), (140, 300)], (-CELL, 0), skin_index=colors[1])
        snakes.append(snake2)
    food = random_food_position(snakes)
    scores = [0, 0] if mode == 2 else [0]
    return snakes, food, scores


def main():
    pygame.init()
    screen = pygame.display.set_mode((WIDTH, HEIGHT))
    pygame.display.set_caption("Snake Interface Game")
    clock = pygame.time.Clock()


    backgrounds = {
        state: load_background(filename, fallback_color)
        for state, (filename, fallback_color) in zip(
            BACKGROUND_FILES.keys(),
            [
                (BACKGROUND_FILES[STATE_START], (10, 10, 40)),
                (BACKGROUND_FILES[STATE_CONTROLS], (20, 50, 20)),
                (BACKGROUND_FILES[STATE_SKIN_SELECT], (50, 10, 50)),
                (BACKGROUND_FILES[STATE_PLAYING], (0, 0, 0)),
                (BACKGROUND_FILES[STATE_GAME_OVER], (60, 10, 10)),
            ],
        )
    }

    state = STATE_START
    selected_mode = 1
    active_color_picker = 0
    chosen_colors = [0, 1]
    snakes, food, scores = reset_game(selected_mode, chosen_colors)
    winner_text = ""

    while True:
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                pygame.quit()
                sys.exit()

            if state == STATE_START:
                if event.type == pygame.KEYDOWN:
                    if event.key in (pygame.K_1, pygame.K_KP1):
                        selected_mode = 1
                    elif event.key in (pygame.K_2, pygame.K_KP2):
                        selected_mode = 2
                    elif event.key == pygame.K_SPACE:
                        state = STATE_CONTROLS

            elif state == STATE_CONTROLS:
                if event.type == pygame.KEYDOWN and event.key == pygame.K_SPACE:
                    state = STATE_SKIN_SELECT

            elif state == STATE_SKIN_SELECT:
                if event.type == pygame.KEYDOWN:
                    if event.key == pygame.K_TAB:
                        active_color_picker = 1 - active_color_picker if selected_mode == 2 else 0
                    elif event.key in (pygame.K_LEFT, pygame.K_a):
                        chosen_colors[active_color_picker] = (
                            chosen_colors[active_color_picker] - 1
                        ) % len(COLOR_PRESETS)
                    elif event.key in (pygame.K_RIGHT, pygame.K_d):
                        chosen_colors[active_color_picker] = (
                            chosen_colors[active_color_picker] + 1
                        ) % len(COLOR_PRESETS)
                    elif event.key == pygame.K_SPACE or event.key == pygame.K_RETURN:
                        snakes, food, scores = reset_game(selected_mode, chosen_colors)
                        winner_text = ""
                        state = STATE_PLAYING

            elif state == STATE_PLAYING:
                if event.type == pygame.KEYDOWN:
                    for player_id, controls in PLAYER_CONTROLS.items():
                        if player_id > len(snakes):
                            continue
                        if event.key in controls:
                            snakes[player_id - 1].update_direction(controls[event.key])

            elif state == STATE_GAME_OVER:
                if event.type == pygame.KEYDOWN and event.key == pygame.K_SPACE:
                    state = STATE_START

        screen.blit(backgrounds[state], (0, 0))

        if state == STATE_START:
            draw_text(screen, "SNAKE ARENA", 48, (WIDTH // 2, 80), center=True)
            draw_text(screen, "Press 1 for Single Player", 28, (WIDTH // 2, 160), center=True)
            draw_text(screen, "Press 2 for Two Player", 28, (WIDTH // 2, 200), center=True)
            draw_text(screen, f"Selected mode: {selected_mode}", 24, (WIDTH // 2, 250), center=True)
            draw_text(screen, "Press SPACE to continue", 24, (WIDTH // 2, 320), center=True)

        elif state == STATE_CONTROLS:
            draw_text(screen, "CONTROLS", 48, (WIDTH // 2, 50), center=True)
            draw_text(screen, "Player 1: W A S D", 30, (WIDTH // 2, 130), center=True)
            draw_text(screen, "Player 2: Arrow keys", 30, (WIDTH // 2, 180), center=True)
            draw_text(screen, "Select mode first on the start screen.", 24, (WIDTH // 2, 240), center=True)
            draw_text(screen, "Press SPACE to choose snake colors.", 24, (WIDTH // 2, 300), center=True)

        elif state == STATE_SKIN_SELECT:
            draw_text(screen, "COLOR SELECTION", 42, (WIDTH // 2, 30), center=True)
            draw_text(screen, "Use LEFT / RIGHT or A / D to change color", 22, (WIDTH // 2, 90), center=True)
            draw_text(screen, "Press TAB to switch player (two player only)", 22, (WIDTH // 2, 120), center=True)
            preview_size = 64
            preview_y = 200
            for index in range(selected_mode):
                x = WIDTH // (selected_mode + 1) * (index + 1)
                player_label = f"Player {index + 1}"
                draw_text(screen, player_label, 24, (x, preview_y - 60), center=True)
                color_index = chosen_colors[index]
                preset = COLOR_PRESETS[color_index]
                preview_rect = pygame.Rect(0, 0, preview_size, preview_size)
                preview_rect.center = (x, preview_y)
                pygame.draw.rect(screen, preset["color"], preview_rect)
                pygame.draw.rect(screen, preset["accent"], preview_rect, 4)
                if index == active_color_picker:
                    pygame.draw.rect(screen, (255, 230, 100), preview_rect.inflate(12, 12), 3)
                draw_text(screen, preset["name"], 22, (x, preview_y + 48), center=True)
            draw_text(screen, "Press SPACE to start", 24, (WIDTH // 2, 340), center=True)

        elif state == STATE_PLAYING:
            for snake in snakes:
                snake.move()

            collision = False
            if len(snakes) == 2 and snakes[0].head() == snakes[1].head():
                winner_text = "Draw!"
                collision = True
            else:
                for index, snake in enumerate(snakes):
                    head = snake.head()
                    if head[0] < 0 or head[0] >= WIDTH or head[1] < 0 or head[1] >= HEIGHT:
                        winner_text = f"Player {2 if index == 0 and len(snakes) == 2 else 1} wins!"
                        collision = True
                        break
                    if snake.collides_with_self():
                        winner_text = f"Player {2 if index == 0 and len(snakes) == 2 else 1} wins!"
                        collision = True
                        break
                    if len(snakes) == 2:
                        other = snakes[1 - index]
                        if head in other.body:
                            winner_text = f"Player {2 if index == 0 else 1} wins!"
                            collision = True
                            break

            if collision:
                state = STATE_GAME_OVER
            else:
                for snake in snakes:
                    snake.draw(screen)

                pygame.draw.rect(screen, (255, 0, 0), pygame.Rect(food[0], food[1], CELL, CELL))

                score_text = "   ".join(f"P{idx + 1}: {score}" for idx, score in enumerate(scores))
                draw_text(screen, score_text, 24, (10, 10))

                for player_index, snake in enumerate(snakes):
                    if snake.head() == food:
                        snake.grow()
                        scores[player_index] += 1
                        food = random_food_position(snakes)
                        break

        elif state == STATE_GAME_OVER:
            draw_text(screen, "GAME OVER", 54, (WIDTH // 2, 100), center=True)
            draw_text(screen, winner_text or "Game has ended.", 26, (WIDTH // 2, 180), center=True)
            draw_text(screen, "Press SPACE to return to start", 24, (WIDTH // 2, 260), center=True)
            draw_text(screen, f"Final score: {' | '.join(str(score) for score in scores)}", 24, (WIDTH // 2, 320), center=True)

        pygame.display.flip()
        clock.tick(FPS)


if __name__ == "__main__":
    main()
