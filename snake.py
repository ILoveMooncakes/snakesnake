import pygame
import os
import random
import sys

# farben
COLOR_PRESETS = [
    ((34, 177, 76), (0, 100, 0)),
    ((255, 127, 39), (200, 80, 0)),
    ((0, 162, 232), (0, 90, 160)),
    ((163, 73, 164), (120, 20, 120)),
    ((255, 201, 14), (180, 140, 0)),
]

CELL = 20
W, H = 1200, 640


def resource_path(filename):
    base = os.path.dirname(os.path.abspath(__file__))
    return os.path.join(base, "bilder", filename)


def show_menu(screen, clock):
    menu = pygame.image.load(resource_path("menu.jpeg")).convert()
    menu = pygame.transform.scale(menu, (W, H))
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
    controls = pygame.image.load(resource_path("controls.jpeg")).convert()
    controls = pygame.transform.scale(controls, (W, H))
    while True:
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                pygame.quit()
                sys.exit()
            if event.type == pygame.KEYDOWN:
                if event.key == pygame.K_ESCAPE:
                    return
                return
        screen.blit(controls, (0, 0))
        pygame.display.flip()
        clock.tick(30)


def color_selection(screen, clock):
    # color selection and bild
    bg = pygame.image.load(resource_path("play.jpeg")).convert()
    bg = pygame.transform.scale(bg, (W, H))
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
                    return (p1_index, p2_index)
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
    # colors is tuple(p1_index, p2_index)
    bg = pygame.image.load(resource_path("game.jpeg")).convert()
    bg = pygame.transform.scale(bg, (W, H))

    start_y = H // 2
    snake1 = [(W // 4, start_y), (W // 4 - CELL, start_y), (W // 4 - 2 * CELL, start_y)]
    snake2 = [(3 * W // 4, start_y), (3 * W // 4 + CELL, start_y), (3 * W // 4 + 2 * CELL, start_y)]
    food = (random.randrange(CELL, W - CELL, CELL), random.randrange(CELL, H - CELL, CELL))
    dir1 = (CELL, 0)
    dir2 = (-CELL, 0)
    score1 = 0
    score2 = 0

    p1_color = COLOR_PRESETS[colors[0]][0]
    p2_color = COLOR_PRESETS[colors[1]][0]

    running = True
    while running:
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                pygame.quit()
                sys.exit()
            if event.type == pygame.KEYDOWN:
                if event.key == pygame.K_ESCAPE:
                    return "menu"
                if event.key == pygame.K_w and dir1 != (0, CELL):
                    dir1 = (0, -CELL)
                elif event.key == pygame.K_s and dir1 != (0, -CELL):
                    dir1 = (0, CELL)
                elif event.key == pygame.K_a and dir1 != (CELL, 0):
                    dir1 = (-CELL, 0)
                elif event.key == pygame.K_d and dir1 != (-CELL, 0):
                    dir1 = (CELL, 0)
                elif event.key == pygame.K_UP and dir2 != (0, CELL):
                    dir2 = (0, -CELL)
                elif event.key == pygame.K_DOWN and dir2 != (0, -CELL):
                    dir2 = (0, CELL)
                elif event.key == pygame.K_LEFT and dir2 != (CELL, 0):
                    dir2 = (-CELL, 0)
                elif event.key == pygame.K_RIGHT and dir2 != (-CELL, 0):
                    dir2 = (CELL, 0)

        # move
        new1 = (snake1[0][0] + dir1[0], snake1[0][1] + dir1[1])
        snake1.insert(0, new1)
        new2 = (snake2[0][0] + dir2[0], snake2[0][1] + dir2[1])
        snake2.insert(0, new2)

        if new1 == food:
            food = (random.randrange(0, W, CELL), random.randrange(0, H, CELL))
            score1 += 1
        else:
            snake1.pop()

        if new2 == food:
            food = (random.randrange(0, W, CELL), random.randrange(0, H, CELL))
            score2 += 1
        else:
            snake2.pop()

        # collisions
        def out_of_bounds(p):
            return p[0] < 0 or p[0] >= W or p[1] < 0 or p[1] >= H

        p1_dead = out_of_bounds(new1) or new1 in snake1[1:] or new1 in snake2
        p2_dead = out_of_bounds(new2) or new2 in snake2[1:] or new2 in snake1
        if p1_dead and p2_dead:
            return show_game_over(screen, clock, dead=3, scores=(score1, score2))
        if p1_dead:
            return show_game_over(screen, clock, dead=1, scores=(score1, score2))
        if p2_dead:
            return show_game_over(screen, clock, dead=2, scores=(score1, score2))

        # draw
        screen.blit(bg, (0, 0))
        for seg in snake1:
            pygame.draw.rect(screen, p1_color, pygame.Rect(seg[0], seg[1], CELL, CELL))
        for seg in snake2:
            pygame.draw.rect(screen, p2_color, pygame.Rect(seg[0], seg[1], CELL, CELL))
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
    if not os.path.isfile(path):
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