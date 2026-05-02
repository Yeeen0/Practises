import pygame
import random
import os

def run_game(screen, settings, player_name):
    WIDTH, HEIGHT = screen.get_size()
    clock = pygame.time.Clock()
    
    CURRENT_DIR = os.path.dirname(os.path.abspath(__file__))
    ASSETS_DIR = os.path.join(CURRENT_DIR, "assets")

    pygame.mixer.init()
    try:
        pygame.mixer.music.load(os.path.join(ASSETS_DIR, "background.wav"))
        pygame.mixer.music.play(-1)
        crash_sound = pygame.mixer.Sound(os.path.join(ASSETS_DIR, "crash.wav"))
    except:
        crash_sound = None
        print("Внимание: Звуки не найдены в папке assets!")

    try:
        bg_img = pygame.image.load(os.path.join(ASSETS_DIR, "AnimatedStreet.png"))
        bg_img = pygame.transform.scale(bg_img, (WIDTH, HEIGHT))
        
        player_img = pygame.image.load(os.path.join(ASSETS_DIR, "Player.png"))
        enemy_img = pygame.image.load(os.path.join(ASSETS_DIR, "Enemy.png"))
        
        coin_img = pygame.image.load(os.path.join(ASSETS_DIR, "coin.png"))
        coin_img = pygame.transform.scale(coin_img, (30, 30))
    except Exception as e:
        print("ОШИБКА: Закинь картинки (Player, Enemy, AnimatedStreet, coin) в папку assets!")
        return None

    diff_multipliers = {"Easy": 0.8, "Normal": 1.0, "Hard": 1.5}
    diff_mult = diff_multipliers.get(settings["difficulty"], 1.0)

    score = 0
    distance = 0.0
    speed_base = 5 * diff_mult
    active_powerup = None
    powerup_timer = 0
    font = pygame.font.SysFont("Verdana", 16)
    
    bg_y1 = 0
    bg_y2 = -HEIGHT

    def get_safe_spawn(existing_sprites, w, h):
        lanes = [100, 200, 300]
        for _ in range(15):
            pos = (random.choice(lanes), random.randint(-400, -100))
            test_rect = pygame.Rect(0, 0, w, h)
            test_rect.center = pos
            
            safe_zone = test_rect.inflate(20, 100) 
            
            is_safe = True
            for sprite in existing_sprites:
                if safe_zone.colliderect(sprite.rect):
                    is_safe = False
                    break
            
            if is_safe:
                return pos
        return None 

    class Player(pygame.sprite.Sprite):
        def __init__(self):
            super().__init__()
            self.image = player_img
            self.rect = self.image.get_rect(center=(WIDTH//2, HEIGHT - 100))

        def update(self, current_speed):
            keys = pygame.key.get_pressed()
            move_speed = 5
            if active_powerup == 'Nitro': move_speed = 8
            
            if keys[pygame.K_LEFT] and self.rect.left > 40:
                self.rect.move_ip(-move_speed, 0)
            if keys[pygame.K_RIGHT] and self.rect.right < WIDTH - 40:
                self.rect.move_ip(move_speed, 0)

    class Enemy(pygame.sprite.Sprite):
        def __init__(self, pos):
            super().__init__()
            self.image = enemy_img
            self.rect = self.image.get_rect(center=pos)

        def update(self, current_speed):
            self.rect.move_ip(0, current_speed)
            if self.rect.top > HEIGHT:
                self.kill()

    class Coin(pygame.sprite.Sprite):
        def __init__(self, pos):
            super().__init__()
            self.image = coin_img
            self.rect = self.image.get_rect(center=pos)

        def update(self, current_speed):
            self.rect.move_ip(0, current_speed)
            if self.rect.top > HEIGHT:
                self.kill()

    class Obstacle(pygame.sprite.Sprite):
        def __init__(self, pos):
            super().__init__()
            self.image = pygame.Surface((40, 40))
            self.image.fill((100, 100, 100)) 
            self.rect = self.image.get_rect(center=pos)

        def update(self, current_speed):
            self.rect.move_ip(0, current_speed)
            if self.rect.top > HEIGHT:
                self.kill()

    class PowerUp(pygame.sprite.Sprite):
        def __init__(self, p_type, pos):
            super().__init__()
            self.p_type = p_type
            self.image = pygame.Surface((30, 30))
            color = (0, 255, 255) if p_type == 'Shield' else (255, 100, 0)
            if p_type == 'Repair': color = (0, 255, 0)
            self.image.fill(color)
            self.rect = self.image.get_rect(center=pos)

        def update(self, current_speed):
            self.rect.move_ip(0, current_speed)
            if self.rect.top > HEIGHT:
                self.kill()

    player = Player()
    all_sprites = pygame.sprite.Group(player)
    
    enemies = pygame.sprite.Group()
    coins = pygame.sprite.Group()
    obstacles = pygame.sprite.Group()
    powerups = pygame.sprite.Group()
    
    spawned_objects = pygame.sprite.Group()

    SPAWN_ENEMY = pygame.USEREVENT + 1
    pygame.time.set_timer(SPAWN_ENEMY, int(1500 / diff_mult))
    
    SPAWN_OBSTACLE = pygame.USEREVENT + 2
    pygame.time.set_timer(SPAWN_OBSTACLE, int(3000 / diff_mult))

    SPAWN_COIN = pygame.USEREVENT + 3
    pygame.time.set_timer(SPAWN_COIN, 2000)

    SPAWN_POWERUP = pygame.USEREVENT + 4
    pygame.time.set_timer(SPAWN_POWERUP, 10000)

    running = True
    while running:
        current_time = pygame.time.get_ticks()
        current_speed = speed_base + (distance // 500)
        
        if active_powerup == 'Nitro':
            current_speed *= 1.5 
            if current_time - powerup_timer > 4000:
                active_powerup = None

        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                pygame.mixer.music.stop()
                return None
            
            if event.type == SPAWN_ENEMY:
                pos = get_safe_spawn(spawned_objects, 40, 60) 
                if pos:
                    e = Enemy(pos)
                    enemies.add(e); spawned_objects.add(e); all_sprites.add(e)
            
            if event.type == SPAWN_OBSTACLE:
                pos = get_safe_spawn(spawned_objects, 40, 40)
                if pos:
                    o = Obstacle(pos)
                    obstacles.add(o); spawned_objects.add(o); all_sprites.add(o)
            
            if event.type == SPAWN_COIN:
                pos = get_safe_spawn(spawned_objects, 30, 30)
                if pos:
                    c = Coin(pos)
                    coins.add(c); spawned_objects.add(c); all_sprites.add(c)
            
            if event.type == SPAWN_POWERUP:
                pos = get_safe_spawn(spawned_objects, 30, 30)
                if pos:
                    p = PowerUp(random.choice(['Nitro', 'Shield', 'Repair']), pos)
                    powerups.add(p); spawned_objects.add(p); all_sprites.add(p)

        bg_y1 += current_speed
        bg_y2 += current_speed
        if bg_y1 >= HEIGHT: bg_y1 = -HEIGHT
        if bg_y2 >= HEIGHT: bg_y2 = -HEIGHT
        
        screen.blit(bg_img, (0, bg_y1))
        screen.blit(bg_img, (0, bg_y2))

        all_sprites.update(current_speed)
        all_sprites.draw(screen)

        distance += current_speed / 10

        if pygame.sprite.spritecollide(player, coins, True):
            score += 10

        hits = pygame.sprite.spritecollide(player, powerups, True)
        for h in hits:
            active_powerup = h.p_type
            powerup_timer = current_time

        hit_enemies = pygame.sprite.spritecollide(player, enemies, False)
        hit_obstacles = pygame.sprite.spritecollide(player, obstacles, False)
        
        if hit_enemies or hit_obstacles:
            if active_powerup == 'Shield':
                active_powerup = None
                if hit_enemies: hit_enemies[0].kill()
                if hit_obstacles: hit_obstacles[0].kill()
            elif active_powerup == 'Repair':
                active_powerup = None
                if hit_enemies: hit_enemies[0].kill()
                if hit_obstacles: hit_obstacles[0].kill()
            else:
                if crash_sound:
                    pygame.mixer.Sound.play(crash_sound)
                pygame.time.delay(1000)
                pygame.mixer.music.stop()
                return {"name": player_name, "score": int(score + distance), "distance": int(distance)}

        txt = font.render(f"Dist: {int(distance)} | Score: {score} | P-Up: {active_powerup}", True, (0, 0, 0))
        screen.blit(txt, (10, 10))

        pygame.display.flip()
        clock.tick(60)

    return None