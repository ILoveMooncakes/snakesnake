import pygame, random, sys

pygame.init()
w, h, s = 400, 400, 20
screen= pygame.display.set_mode((w,h))
clock = pygame.time.Clock()

snake = [(100, 100),(80,100), (60,100)]
food = (random.randrange(0, w, s), random.randrange(0, h, s))
direction = (s,0)
score = 0

while true:
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            pygame.quit()
            sys.exit()
        elif event.type == pygame.KEYDOWN:
            if event.key == pygame.K_UP and direction != (0, s):
                direction == (0, -s)
            elif event.key == pygame.K_DOWN and direction != (0, -s):
                direction = (0, -s)
            elif event.key == pygame.K_LEFT and direction != (s, 0):
                direction = (s, 0)
            elif event.key == pygame.K_RIGHT and direction != (-s, 0):
                direction = (s, 0)

    new_head = (snake[0][0]+ direction[0], snake[0][1]+ direction[1])
    snake.insert(0, new_head)

    if new_head == food:
        food = (random.randrange(0, w, s))
        score += 1
    else:
        snake.pop()
        
    if new_head[0] < 0 or new_head[0] >= w or new_head[1] < 0 or new_head[1] >= h or new_head in snake [1]:
        print(f"GAME OVER   
              score: {score}")
              pygame.quit()
              sys.exit()

              screen.fill((0 ,0 ,0))
    for segment in snake:
        pygame.draw.rect(screen, (0, 255, 0), pygame.Rect(segment[0], segment[1], s, s))
        pygame.draw.rect(screen, (255, 0, 0), pygame.Rect(food[0], food[1], s, s))
        pygame.display.flip()
        clock.tick(10)
