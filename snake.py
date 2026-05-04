import pygame
import random
import sys

def handle_direction(event, direction1, direction2):
    """Handle player input for both snakes."""
    if event.type == pygame.KEYDOWN:
        # Player 1 controls (Arrow keys)
        if event.key == pygame.K_UP and direction1 != (0, 20):
            direction1 = (0, -20)
        elif event.key == pygame.K_DOWN and direction1 != (0, -20):
            direction1 = (0, 20)
        elif event.key == pygame.K_LEFT and direction1 != (20, 0):
            direction1 = (-20, 0)
        elif event.key == pygame.K_RIGHT and direction1 != (-20, 0):
            direction1 = (20, 0)
        
        # Player 2 controls (WASD)
        elif event.key == pygame.K_w and direction2 != (0, 20):
            direction2 = (0, -20)
        elif event.key == pygame.K_s and direction2 != (0, -20):
            direction2 = (0, 20)
        elif event.key == pygame.K_a and direction2 != (20, 0):
            direction2 = (-20, 0)
        elif event.key == pygame.K_d and direction2 != (-20, 0):
            direction2 = (20, 0)
    
    return direction1, direction2


def check_collision(head, snake, other_snake, w, h):
    """Check if a snake has collided with walls, itself, or the other snake."""
    return (
        head[0] < 0
        or head[0] >= w
        or head[1] < 0
        or head[1] >= h
        or head in snake[1:]
        or head in other_snake
    )


def move_snake(snake, direction):
    """Move a snake in the given direction."""
    new_head = (snake[0][0] + direction[0], snake[0][1] + direction[1])
    snake.insert(0, new_head)
    return new_head


def check_food_collision(head, food, w, h, s, score):
    """Check if snake eats food and generate new food if so."""
    if head == food:
        food = (random.randrange(0, w, s), random.randrange(0, h, s))
        score += 1
        return food, score, True
    return food, score, False


def main():
    pygame.init()
    w, h, s = 400, 400, 20
    screen = pygame.display.set_mode((w, h))
    pygame.display.set_caption("Snake Game - Player 1 (Arrows) vs Player 2 (WASD)")
    clock = pygame.time.Clock()
    font = pygame.font.Font(None, 36)
    
    # Initialize snakes and game state
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
            else:
                direction1, direction2 = handle_direction(event, direction1, direction2)

        # Move both snakes
        new_head1 = move_snake(snake1, direction1)
        new_head2 = move_snake(snake2, direction2)

        # Check food collision
        food, score1, ate1 = check_food_collision(new_head1, food, w, h, s, score1)
        if not ate1:
            snake1.pop()
        
        food, score2, ate2 = check_food_collision(new_head2, food, w, h, s, score2)
        if not ate2:
            snake2.pop()

        # Check collisions
        if check_collision(new_head1, snake1, snake2, w, h):
            print(f"GAME OVER - Player 1 Lost! Final Scores - Player 1: {score1}, Player 2: {score2}")
            pygame.quit()
            sys.exit()

        if check_collision(new_head2, snake2, snake1, w, h):
            print(f"GAME OVER - Player 2 Lost! Final Scores - Player 1: {score1}, Player 2: {score2}")
            pygame.quit()
            sys.exit()

        # Render game
        screen.fill((0, 0, 0))
        
        # Draw snakes
        for segment in snake1:
            pygame.draw.rect(screen, (0, 255, 0), pygame.Rect(segment[0], segment[1], s, s))
        for segment in snake2:
            pygame.draw.rect(screen, (0, 0, 255), pygame.Rect(segment[0], segment[1], s, s))
        
        # Draw food
        pygame.draw.rect(screen, (255, 0, 0), pygame.Rect(food[0], food[1], s, s))
        
        # Draw scores on screen
        score_text1 = font.render(f"P1: {score1}", True, (0, 255, 0))
        score_text2 = font.render(f"P2: {score2}", True, (0, 0, 255))
        screen.blit(score_text1, (10, 10))
        screen.blit(score_text2, (w - 150, 10))
        
        pygame.display.flip()
        
        # Increase speed with score
        speed = max(15, 10 + (score1 + score2) // 3)
        clock.tick(speed)


if __name__ == "__main__":
    main()
        
        # Draw scores on screen
        score_text1 = font.render(f"P1: {score1}", True, (0, 255, 0))
        score_text2 = font.render(f"P2: {score2}", True, (0, 0, 255))
        screen.blit(score_text1, (10, 10))
        screen.blit(score_text2, (w - 150, 10))
        
        pygame.display.flip()
        
        # Increase speed with score
        speed = max(15, 10 + (score1 + score2) // 3)
        clock.tick(speed)


if __name__ == "__main__":
    main()
    #bleeeeeeeeeeeeeeeeee