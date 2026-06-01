import random
import sys
from pathlib import Path

import pygame

# colors
COLOR_PRESETS = [
    ((34, 177, 76), (0, 100, 0)),
    ((255, 127, 39), (200, 80, 0)),
    ((0, 162, 232), (0, 90, 160)),
    ((163, 73, 164), (120, 20, 120)),
    ((255, 201, 14), (180, 140, 0)),
]

CELL = 20
W, H = 1200, 640
SCREEN_SIZE = (W, H)

ASSETS_DIR = Path(__file__).resolve().parent / "bilder"


def resource_path(filename):
    return ASSETS_DIR / filename


def load_scaled_image(filename):
    return pygame.transform.scale(pygame.image.load(resource_path(filename)).convert(), SCREEN_SIZE)


def random_cell_position(margin=CELL):
    return (random.randrange(margin, W - margin, CELL), random.randrange(margin, H - margin, CELL))


def add_positions(a, b):
    return a[0] + b[0], a[1] + b[1]


def is_out_of_bounds(position):
    return position[0] < 0 or position[0] >= W or position[1] < 0 or position[1] >= H


def show_menu(screen, clock):
    menu = load_scaled_image("menu.jpeg")

    while True:
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                pygame.quit()
                sys.exit()
            if event.type == pygame.KEYDOWN:
                if event.key == pygame.K_1:
                    return "color_select"
                if event.key == pygame.K_2:
                    return "controls"
                if event.key == pygame.K_3:
                    pygame.quit()
                    sys.exit()
        screen.blit(menu, (0, 0))
        pygame.display.flip()
        clock.tick(30)


def show_controls(screen, clock):
    controls = load_scaled_image("controls.jpeg")

    while True:
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                pygame.quit()
                sys.exit()
            if event.type == pygame.KEYDOWN:
                return
        screen.blit(controls, (0, 0))
        pygame.display.flip()
        clock.tick(30)


def color_selection(screen, clock):
    # color selection and background image
    bg = load_scaled_image("play.jpeg")
    p1_index = 0
    p2_index = 1 if len(COLOR_PRESETS) > 1 else 0
    while True:
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                pygame.quit()
                sys.exit()
            if event.type == pygame.KEYDOWN:
                if event.key == pygame.K_a:
                    p1_index = (p1_index - 1) % len(COLOR_PRESETS)
                elif event.key == pygame.K_d:
                    p1_index = (p1_index + 1) % len(COLOR_PRESETS)
                elif event.key == pygame.K_LEFT:
                    p2_index = (p2_index - 1) % len(COLOR_PRESETS)
                elif event.key == pygame.K_RIGHT:
                    p2_index = (p2_index + 1) % len(COLOR_PRESETS)
                elif event.key == pygame.K_1:
                    return p1_index, p2_index
                elif event.key == pygame.K_ESCAPE:
                    return None

        screen.blit(bg, (0, 0))
        # lange farben
        preview_width = 96
        preview_height = 320
        x1 = W // 4
        x2 = 3 * W // 4
        y = H // 3
        pygame.draw.rect(screen, COLOR_PRESETS[p1_index][0], pygame.Rect(x1 - preview_width // 2, y - preview_height // 2, preview_width, preview_height))
        pygame.draw.rect(screen, COLOR_PRESETS[p2_index][0], pygame.Rect(x2 - preview_width // 2, y - preview_height // 2, preview_width, preview_height))

        pygame.display.flip()
        clock.tick(30)


def play_game(screen, clock, colors):
    # colors is a tuple of (player1_color_index, player2_color_index)
    bg = load_scaled_image("game.jpeg")

    start_y = H // 2
    player1_snake = [(W // 4, start_y), (W // 4 - CELL, start_y), (W // 4 - 2 * CELL, start_y)]
    player2_snake = [(3 * W // 4, start_y), (3 * W // 4 + CELL, start_y), (3 * W // 4 + 2 * CELL, start_y)]
    food = random_cell_position(CELL)
    direction1 = (CELL, 0)
    direction2 = (-CELL, 0)
    player1_score = 0
    player2_score = 0

    player1_color, player2_color = [COLOR_PRESETS[index][0] for index in colors]

    while True:
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                pygame.quit()
                sys.exit()
            if event.type == pygame.KEYDOWN:
                if event.key == pygame.K_ESCAPE:
                    return "menu"
                if event.key == pygame.K_w and direction1 != (0, CELL):
                    direction1 = (0, -CELL)
                elif event.key == pygame.K_s and direction1 != (0, -CELL):
                    direction1 = (0, CELL)
                elif event.key == pygame.K_a and direction1 != (CELL, 0):
                    direction1 = (-CELL, 0)
                elif event.key == pygame.K_d and direction1 != (-CELL, 0):
                    direction1 = (CELL, 0)
                elif event.key == pygame.K_UP and direction2 != (0, CELL):
                    direction2 = (0, -CELL)
                elif event.key == pygame.K_DOWN and direction2 != (0, -CELL):
                    direction2 = (0, CELL)
                elif event.key == pygame.K_LEFT and direction2 != (CELL, 0):
                    direction2 = (-CELL, 0)
                elif event.key == pygame.K_RIGHT and direction2 != (-CELL, 0):
                    direction2 = (CELL, 0)

        new_head1 = add_positions(player1_snake[0], direction1)
        player1_snake.insert(0, new_head1)
        new_head2 = add_positions(player2_snake[0], direction2)
        player2_snake.insert(0, new_head2)

        if new_head1 == food:
            food = random_cell_position(0)
            player1_score += 1
        else:
            player1_snake.pop()

        if new_head2 == food:
            food = random_cell_position(0)
            player2_score += 1
        else:
            player2_snake.pop()

        player1_dead = is_out_of_bounds(new_head1) or new_head1 in player1_snake[1:] or new_head1 in player2_snake
        player2_dead = is_out_of_bounds(new_head2) or new_head2 in player2_snake[1:] or new_head2 in player1_snake

        if player1_dead and player2_dead:
            return show_game_over(screen, clock, dead=3, scores=(player1_score, player2_score))
        if player1_dead:
            return show_game_over(screen, clock, dead=1, scores=(player1_score, player2_score))
        if player2_dead:
            return show_game_over(screen, clock, dead=2, scores=(player1_score, player2_score))

        # draw
        screen.blit(bg, (0, 0))
        for segment in player1_snake:
            pygame.draw.rect(screen, player1_color, pygame.Rect(segment[0], segment[1], CELL, CELL))
        for segment in player2_snake:
            pygame.draw.rect(screen, player2_color, pygame.Rect(segment[0], segment[1], CELL, CELL))
        pygame.draw.rect(screen, (255, 0, 0), pygame.Rect(food[0], food[1], CELL, CELL))
        pygame.display.flip()
        clock.tick(10)


def show_game_over(screen, clock, dead=0, scores=(0, 0)):
    # dead: 1 => player1 died, 2 => player2 died, 3 => both died.
    if dead == 3:
        filename = "gameover3.jpeg"
    elif dead == 2:
        filename = "gameover2.jpeg"
    else:
        filename = "gameover.jpeg"

    path = resource_path(filename)
    if not path.is_file():
        # fallback to default
        path = resource_path("gameover.jpeg")

    over = pygame.image.load(path).convert()
    over = pygame.transform.scale(over, (W, H))
    font = pygame.font.SysFont(None, 96)

    p1_text = f"{scores[0]}"
    p2_text = f"{scores[1]}"
    p1_surf = font.render(p1_text, True, (0, 0, 0))
    p2_surf = font.render(p2_text, True, (0, 0, 0))

    while True:
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                pygame.quit()
                sys.exit()
            if event.type == pygame.KEYDOWN:
                if event.key == pygame.K_1:
                    return "restart"
                if event.key == pygame.K_ESCAPE:
                    return "menu"
        screen.blit(over, (0, 0))
        # score
        y = (2 * H) // 3 - p1_surf.get_height() // 2 - 20
        x1 = W // 4 - p1_surf.get_width() // 2 + 90
        x2 = 3 * W // 4 - p2_surf.get_width() // 2
        screen.blit(p1_surf, (x1, y))
        screen.blit(p2_surf, (x2, y))
        pygame.display.flip()
        clock.tick(30)


def main():
    pygame.init()
    screen = pygame.display.set_mode((W, H))
    clock = pygame.time.Clock()

    while True:
        action = show_menu(screen, clock)
        if action == "controls":
            show_controls(screen, clock)
            continue
        if action == "color_select":
            colors = color_selection(screen, clock)
            if colors is None:
                continue
            # start playing loop; after a game over, either restart or go to menu
            while True:
                result = play_game(screen, clock, colors)
                if result == "menu":
                    break
                if result == "restart":
                    continue


if __name__ == "__main__":
    main()