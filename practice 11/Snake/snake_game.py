import pygame
import random
import sys

def run_game():
    pygame.init()

    WIDTH, HEIGHT = 600, 400
    BLOCK_SIZE = 20
    screen = pygame.display.set_mode((WIDTH, HEIGHT))
    pygame.display.set_caption("Snake - Practice 11")

    BLACK = (0, 0, 0)
    GREEN = (0, 255, 0)
    RED = (255, 0, 0)
    GOLD = (255, 215, 0)
    WHITE = (255, 255, 255)

    font = pygame.font.SysFont("Verdana", 16)

    snake_pos = [WIDTH // 2, HEIGHT // 2]
    snake_body = [[WIDTH // 2, HEIGHT // 2], [WIDTH // 2 - BLOCK_SIZE, HEIGHT // 2]]

    def spawn_new_food():
        while True:
            food_x = random.randrange(0, WIDTH // BLOCK_SIZE) * BLOCK_SIZE
            food_y = random.randrange(0, HEIGHT // BLOCK_SIZE) * BLOCK_SIZE
            if [food_x, food_y] not in snake_body:
                weight = random.choice([1, 1, 1, 3]) 
                spawn_time = pygame.time.get_ticks() 
                return [food_x, food_y, weight, spawn_time]

    current_food = spawn_new_food()
    direction = 'RIGHT'
    change_to = direction

    score = 0
    level = 1
    fps = 6

    clock = pygame.time.Clock()

    while True:
        current_time = pygame.time.get_ticks()

        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                pygame.quit()
                sys.exit()
            if event.type == pygame.KEYDOWN:
                if event.key == pygame.K_UP and direction != 'DOWN': change_to = 'UP'
                if event.key == pygame.K_DOWN and direction != 'UP': change_to = 'DOWN'
                if event.key == pygame.K_LEFT and direction != 'RIGHT': change_to = 'LEFT'
                if event.key == pygame.K_RIGHT and direction != 'LEFT': change_to = 'RIGHT'

        direction = change_to

        if direction == 'UP': snake_pos[1] -= BLOCK_SIZE
        if direction == 'DOWN': snake_pos[1] += BLOCK_SIZE
        if direction == 'LEFT': snake_pos[0] -= BLOCK_SIZE
        if direction == 'RIGHT': snake_pos[0] += BLOCK_SIZE

        snake_body.insert(0, list(snake_pos))

        if current_time - current_food[3] > 6000:
            current_food = spawn_new_food()

        if snake_pos[0] == current_food[0] and snake_pos[1] == current_food[1]:
            score += current_food[2] 
            if score // 5 >= level: 
                level += 1
                fps += 1
            current_food = spawn_new_food()
        else:
            snake_body.pop() 

        if (snake_pos[0] < 0 or snake_pos[0] >= WIDTH or 
            snake_pos[1] < 0 or snake_pos[1] >= HEIGHT):
            pygame.quit(); sys.exit()

        for block in snake_body[1:]:
            if snake_pos[0] == block[0] and snake_pos[1] == block[1]:
                pygame.quit(); sys.exit()

        screen.fill(BLACK)
        
        for pos in snake_body:
            pygame.draw.rect(screen, GREEN, pygame.Rect(pos[0], pos[1], BLOCK_SIZE, BLOCK_SIZE))
        
        food_color = RED if current_food[2] == 1 else GOLD
        pygame.draw.rect(screen, food_color, pygame.Rect(current_food[0], current_food[1], BLOCK_SIZE, BLOCK_SIZE))

        time_left = max(0, 6000 - (current_time - current_food[3])) // 1000
        status_text = f'Score: {score} | Lvl: {level} | Timer: {time_left}s'
        screen.blit(font.render(status_text, True, WHITE), (10, 10))

        pygame.display.update()
        clock.tick(fps)