import pygame
import random
import time

def run_game(screen, settings, player_name, personal_best):
    WIDTH, HEIGHT = screen.get_size()
    BLOCK = 20
    clock = pygame.time.Clock()

    
    BLACK = (0, 0, 0)
    WHITE = (255, 255, 255)
    RED = (255, 0, 0) 
    DARK_RED = (139, 0, 0) 
    GRAY = (100, 100, 100) 
    
    snake_color = tuple(settings.get("snake_color", [0, 255, 0]))
    grid_on = settings.get("grid", False)

    font = pygame.font.SysFont("Verdana", 16)

    snake_pos = [WIDTH//2, HEIGHT//2]
    snake_body = [[WIDTH//2, HEIGHT//2], [WIDTH//2-BLOCK, HEIGHT//2], [WIDTH//2-2*BLOCK, HEIGHT//2]]
    direction = 'RIGHT'
    change_to = direction

    score = 0
    level = 1
    base_fps = 8

    obstacles = []

    def get_random_pos():
        while True:
            x = random.randrange(0, WIDTH//BLOCK) * BLOCK
            y = random.randrange(0, HEIGHT//BLOCK) * BLOCK
            if [x, y] not in snake_body and [x, y] not in obstacles:
                return [x, y]

    food_pos = get_random_pos()
    poison_pos = get_random_pos() if random.random() > 0.5 else [-100, -100]

    powerup_active = False
    powerup_type = None
    powerup_pos = [-100, -100]
    powerup_spawn_time = 0
    
    active_effect = None
    effect_end_time = 0
    has_shield = False

    def generate_obstacles(lvl):
        obs = []
        if lvl >= 3:
            for _ in range(lvl * 2):
                pos = get_random_pos()
                if abs(pos[0] - snake_pos[0]) > 60 or abs(pos[1] - snake_pos[1]) > 60:
                    obs.append(pos)
        return obs

    running = True
    while running:
        current_time = pygame.time.get_ticks()

        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                return None
            if event.type == pygame.KEYDOWN:
                if event.key == pygame.K_UP and direction != 'DOWN': change_to = 'UP'
                if event.key == pygame.K_DOWN and direction != 'UP': change_to = 'DOWN'
                if event.key == pygame.K_LEFT and direction != 'RIGHT': change_to = 'LEFT'
                if event.key == pygame.K_RIGHT and direction != 'LEFT': change_to = 'RIGHT'

        direction = change_to
        if direction == 'UP': snake_pos[1] -= BLOCK
        if direction == 'DOWN': snake_pos[1] += BLOCK
        if direction == 'LEFT': snake_pos[0] -= BLOCK
        if direction == 'RIGHT': snake_pos[0] += BLOCK

        snake_body.insert(0, list(snake_pos))

        if not powerup_active and active_effect is None and random.random() < 0.01:
            powerup_active = True
            powerup_type = random.choice(['SPEED', 'SLOW', 'SHIELD'])
            powerup_pos = get_random_pos()
            powerup_spawn_time = current_time

        if powerup_active and current_time - powerup_spawn_time > 8000:
            powerup_active = False
            powerup_pos = [-100, -100]

        if active_effect in ['SPEED', 'SLOW'] and current_time > effect_end_time:
            active_effect = None

        if snake_pos == food_pos:
            score += 10
            food_pos = get_random_pos()
            poison_pos = get_random_pos() if random.random() > 0.4 else [-100, -100]
            if score // 50 >= level:
                level += 1
                base_fps += 1
                obstacles = generate_obstacles(level)
        elif snake_pos == poison_pos:
            snake_body = snake_body[:-3] if len(snake_body) > 3 else []
            poison_pos = [-100, -100]
            if len(snake_body) <= 1:
                return {"score": score, "level": level} 
        elif powerup_active and snake_pos == powerup_pos:
            active_effect = powerup_type
            if active_effect in ['SPEED', 'SLOW']:
                effect_end_time = current_time + 5000
            elif active_effect == 'SHIELD':
                has_shield = True
            powerup_active = False
            powerup_pos = [-100, -100]
            snake_body.pop()
        else:
            snake_body.pop()

        hit_wall = (snake_pos[0] < 0 or snake_pos[0] >= WIDTH or snake_pos[1] < 0 or snake_pos[1] >= HEIGHT)
        hit_self = snake_pos in snake_body[1:]
        hit_obstacle = snake_pos in obstacles

        if hit_wall or hit_self or hit_obstacle:
            if has_shield:
                has_shield = False
                snake_pos = list(snake_body[1])
                direction = change_to = 'UP' if direction == 'DOWN' else 'DOWN' if direction == 'UP' else 'LEFT' if direction == 'RIGHT' else 'RIGHT'
            else:
                return {"score": score, "level": level}

        screen.fill(BLACK)

        if grid_on:
            for x in range(0, WIDTH, BLOCK):
                pygame.draw.line(screen, (30, 30, 30), (x, 0), (x, HEIGHT))
            for y in range(0, HEIGHT, BLOCK):
                pygame.draw.line(screen, (30, 30, 30), (0, y), (WIDTH, y))

        for obs in obstacles:
            pygame.draw.rect(screen, GRAY, pygame.Rect(obs[0], obs[1], BLOCK, BLOCK))

        s_color = (0, 255, 255) if has_shield else snake_color
        for pos in snake_body:
            pygame.draw.rect(screen, s_color, pygame.Rect(pos[0], pos[1], BLOCK, BLOCK))

        pygame.draw.rect(screen, RED, pygame.Rect(food_pos[0], food_pos[1], BLOCK, BLOCK))
        if poison_pos[0] >= 0:
            pygame.draw.rect(screen, DARK_RED, pygame.Rect(poison_pos[0], poison_pos[1], BLOCK, BLOCK))

        if powerup_active:
            p_color = (255, 0, 255) if powerup_type == 'SPEED' else (0, 100, 255) if powerup_type == 'SLOW' else (255, 255, 0)
            pygame.draw.rect(screen, p_color, pygame.Rect(powerup_pos[0], powerup_pos[1], BLOCK, BLOCK))

        txt = font.render(f"User: {player_name} | Score: {score} | Lvl: {level} | PB: {personal_best}", True, WHITE)
        screen.blit(txt, (5, 5))
        
        if active_effect in ['SPEED', 'SLOW']:
            timer = (effect_end_time - current_time) // 1000
            eff_txt = font.render(f"Effect: {active_effect} ({timer}s)", True, WHITE)
            screen.blit(eff_txt, (5, 25))
        if has_shield:
            sh_txt = font.render("SHIELD ACTIVE", True, (0, 255, 255))
            screen.blit(sh_txt, (5, 45))

        pygame.display.flip()
        
        current_fps = base_fps
        if active_effect == 'SPEED': current_fps += 5
        elif active_effect == 'SLOW': current_fps = max(3, current_fps - 4)
        
        clock.tick(current_fps)

    return None