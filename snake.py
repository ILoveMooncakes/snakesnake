import pygame
{
    "python.analysis.extraPaths": ["./src", "./lib"]
}
import random
import sys

#some comments

def main():
    pygame.init()
    w, h, s = 400, 400, 20
    screen = pygame.display.set_mode((w, h))
    clock = pygame.time.Clock()

    snake1 = [(100, 100), (80, 100), (60, 100)]
    snake2 = [(300, 100), (320, 100), (340, 100)]
    food = (random.randrange(0, w, s), random.randrange(0, h, s))
    direction1 = (s, 0)
    direction2 = (-s, 0)
    score1 = 0
    score2 = 0

    while True:
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                pygame.quit()
                sys.exit()
            elif event.type == pygame.KEYDOWN:
                if event.key == pygame.K_UP and direction1 != (0, s):
                    direction1 = (0, -s)
                elif event.key == pygame.K_DOWN and direction1 != (0, -s):
                    direction1 = (0, s)
                elif event.key == pygame.K_LEFT and direction1 != (s, 0):
                    direction1 = (-s, 0)
                elif event.key == pygame.K_RIGHT and direction1 != (-s, 0):
                    direction1 = (s, 0)
                elif event.key == pygame.K_w and direction2 != (0, s):
                    direction2 = (0, -s)
                elif event.key == pygame.K_s and direction2 != (0, -s):
                    direction2 = (0, s)
                elif event.key == pygame.K_a and direction2 != (s, 0):
                    direction2 = (-s, 0)
                elif event.key == pygame.K_d and direction2 != (-s, 0):
                    direction2 = (s, 0)

        new_head1 = (snake1[0][0] + direction1[0], snake1[0][1] + direction1[1])
        snake1.insert(0, new_head1)

        new_head2 = (snake2[0][0] + direction2[0], snake2[0][1] + direction2[1])
        snake2.insert(0, new_head2)

        if new_head1 == food:
            food = (random.randrange(0, w, s), random.randrange(0, h, s))
            score1 += 1
        else:
            snake1.pop()

        if new_head2 == food:
            food = (random.randrange(0, w, s), random.randrange(0, h, s))
            score2 += 1
        else:
            snake2.pop()

        if (
            new_head1[0] < 0
            or new_head1[0] >= w
            or new_head1[1] < 0
            or new_head1[1] >= h
            or new_head1 in snake1[1:]
            or new_head1 in snake2
        ):
            print(f"GAME OVER   Player 1 score: {score1}, Player 2 score: {score2}")
            pygame.quit()
            sys.exit()

        if (
            new_head2[0] < 0
            or new_head2[0] >= w
            or new_head2[1] < 0
            or new_head2[1] >= h
            or new_head2 in snake2[1:]
            or new_head2 in snake1
        ):
            print(f"GAME OVER   Player 1 score: {score1}, Player 2 score: {score2}")
            pygame.quit()
            sys.exit()

        screen.fill((0, 0, 0))
        for segment in snake1:
            pygame.draw.rect(
                screen, (0, 255, 0), pygame.Rect(segment[0], segment[1], s, s)
            )
        for segment in snake2:
            pygame.draw.rect(
                screen, (0, 0, 255), pygame.Rect(segment[0], segment[1], s, s)
            )
        pygame.draw.rect(screen, (255, 0, 0), pygame.Rect(food[0], food[1], s, s))
        pygame.display.flip()
        clock.tick(10)


if __name__ == "__main__":
    main()
    #bleeeeeeeeeeeeeeeeee hallo jolin