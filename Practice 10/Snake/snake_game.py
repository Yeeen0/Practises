import pygame
import random
import sys

def run_game():
    pygame.init()

    WIDTH, HEIGHT = 600, 400
    BLOCK_SIZE = 20 
    screen = pygame.display.set_mode((WIDTH, HEIGHT))
    pygame.display.set_caption("Snake - Practice 10")

    BLACK = (0, 0, 0)
    GREEN = (0, 255, 0)
    RED = (255, 0, 0)
    WHITE = (255, 255, 255)
    GRAY = (50, 50, 50)

    font = pygame.font.SysFont("Verdana", 18)

    snake_pos = [WIDTH // 2, HEIGHT // 2]
    snake_body = [
        [WIDTH // 2, HEIGHT // 2], 
        [WIDTH // 2 - BLOCK_SIZE, HEIGHT // 2], 
        [WIDTH // 2 - 2 * BLOCK_SIZE, HEIGHT // 2]
    ]

    def generate_food():
        while True:
            food_x = random.randrange(0, WIDTH // BLOCK_SIZE) * BLOCK_SIZE
            food_y = random.randrange(0, HEIGHT // BLOCK_SIZE) * BLOCK_SIZE
            if [food_x, food_y] not in snake_body:
                return [food_x, food_y]

    food_pos = generate_food()
    food_spawn = True

    direction = 'RIGHT'
    change_to = direction

    score = 0
    level = 1
    fps = 6

    clock = pygame.time.Clock()

    while True:
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                pygame.quit()
                sys.exit()
            
            if event.type == pygame.KEYDOWN:
                if event.key == pygame.K_UP and direction != 'DOWN':
                    change_to = 'UP'
                if event.key == pygame.K_DOWN and direction != 'UP':
                    change_to = 'DOWN'
                if event.key == pygame.K_LEFT and direction != 'RIGHT':
                    change_to = 'LEFT'
                if event.key == pygame.K_RIGHT and direction != 'LEFT':
                    change_to = 'RIGHT'

        direction = change_to

        if direction == 'UP':
            snake_pos[1] -= BLOCK_SIZE
        if direction == 'DOWN':
            snake_pos[1] += BLOCK_SIZE
        if direction == 'LEFT':
            snake_pos[0] -= BLOCK_SIZE
        if direction == 'RIGHT':
            snake_pos[0] += BLOCK_SIZE

        snake_body.insert(0, list(snake_pos)) 

        if snake_pos[0] == food_pos[0] and snake_pos[1] == food_pos[1]:
            score += 1
            food_spawn = False
            
            if score % 3 == 0:
                level += 1
                fps += 2 
        else:
            snake_body.pop() 

        if not food_spawn:
            food_pos = generate_food()
        food_spawn = True

        if (snake_pos[0] < 0 or snake_pos[0] > WIDTH - BLOCK_SIZE or 
            snake_pos[1] < 0 or snake_pos[1] > HEIGHT - BLOCK_SIZE):
            pygame.quit()
            sys.exit()

        for block in snake_body[1:]:
            if snake_pos[0] == block[0] and snake_pos[1] == block[1]:
                pygame.quit()
                sys.exit()

        screen.fill(BLACK)
        
        for pos in snake_body:
            pygame.draw.rect(screen, GREEN, pygame.Rect(pos[0], pos[1], BLOCK_SIZE, BLOCK_SIZE))
        
        pygame.draw.rect(screen, RED, pygame.Rect(food_pos[0], food_pos[1], BLOCK_SIZE, BLOCK_SIZE))

        score_surface = font.render(f'Score: {score} | Level: {level}', True, WHITE)
        screen.blit(score_surface, (10, 10))

        pygame.display.update()
        
        clock.tick(fps)
