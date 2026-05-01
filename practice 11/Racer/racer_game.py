import pygame
import random
import sys
import os

def run_game():
    pygame.init()
    pygame.mixer.init() 

    CURRENT_DIR = os.path.dirname(os.path.abspath(__file__))
    IMG_DIR = os.path.join(CURRENT_DIR, "images")
    MUSIC_DIR = os.path.join(CURRENT_DIR, "music")

    SCREEN_WIDTH = 400
    SCREEN_HEIGHT = 600
    screen = pygame.display.set_mode((SCREEN_WIDTH, SCREEN_HEIGHT))
    pygame.display.set_caption("Racer - Practice 11")

    BLACK = (0, 0, 0)
    RED = (255, 0, 0)
    font = pygame.font.SysFont("Verdana", 20)

    
    pygame.mixer.music.load(os.path.join(MUSIC_DIR, "background.wav"))
    pygame.mixer.music.play(-1) 
    crash_sound = pygame.mixer.Sound(os.path.join(MUSIC_DIR, "crash.wav"))

    
    bg_img = pygame.image.load(os.path.join(IMG_DIR, "AnimatedStreet.png"))
    bg_img = pygame.transform.scale(bg_img, (SCREEN_WIDTH, SCREEN_HEIGHT))
    player_img = pygame.image.load(os.path.join(IMG_DIR, "Player.png"))
    enemy_img = pygame.image.load(os.path.join(IMG_DIR, "Enemy.png"))

    
    try:
        base_coin = pygame.image.load(os.path.join(IMG_DIR, "coin.png"))
        coin_img_normal = pygame.transform.scale(base_coin, (30, 30))
        coin_img_mega = pygame.transform.scale(base_coin, (45, 45)) 
    except FileNotFoundError:
        coin_img_normal = pygame.Surface((30, 30)); coin_img_normal.fill((255, 255, 0))
        coin_img_mega = pygame.Surface((45, 45)); coin_img_mega.fill((255, 165, 0)) 

    class Player(pygame.sprite.Sprite):
        def __init__(self):
            super().__init__()
            self.image = player_img
            self.rect = self.image.get_rect()
            self.rect.center = (200, SCREEN_HEIGHT - 100)

        def update(self):
            keys = pygame.key.get_pressed()
            if keys[pygame.K_LEFT] and self.rect.centerx > 60:
                self.rect.move_ip(-5, 0)
            if keys[pygame.K_RIGHT] and self.rect.centerx < 340:
                self.rect.move_ip(5, 0)

    class Enemy(pygame.sprite.Sprite):
        def __init__(self):
            super().__init__()
            self.image = enemy_img
            self.rect = self.image.get_rect()
            self.lanes = [90, 200, 310]
            self.rect.center = (random.choice(self.lanes), 0)
            self.speed = 5 

        def update(self):
            self.rect.move_ip(0, self.speed) 
            if self.rect.top > SCREEN_HEIGHT:
                self.rect.top = 0
                self.rect.center = (random.choice(self.lanes), 0)

    class Coin(pygame.sprite.Sprite):
        def __init__(self):
            super().__init__()
           
            self.weight = random.choice([1, 1, 1, 3]) 
            
            if self.weight == 1:
                self.image = coin_img_normal
            else:
                self.image = coin_img_mega

            self.rect = self.image.get_rect()
            self.lanes = [90, 200, 310]
            self.rect.center = (random.choice(self.lanes), 0)

        def update(self):
            self.rect.move_ip(0, 4) 
            if self.rect.top > SCREEN_HEIGHT:
                self.rect.top = 0
                self.rect.center = (random.choice(self.lanes), 0)

    P1 = Player()
    E1 = Enemy()
    C1 = Coin()

    enemies = pygame.sprite.Group()
    enemies.add(E1)
    coins = pygame.sprite.Group()
    coins.add(C1)
    all_sprites = pygame.sprite.Group()
    all_sprites.add(P1, E1, C1)

    score = 0
    clock = pygame.time.Clock()

    while True:
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                pygame.quit()
                sys.exit()

        screen.blit(bg_img, (0, 0))

        new_enemy_speed = 5 + (score // 5)
        for e in enemies:
            e.speed = new_enemy_speed

        for entity in all_sprites:
            entity.update()
            screen.blit(entity.image, entity.rect)

        
        collided_coins = pygame.sprite.spritecollide(P1, coins, True)
        for coin in collided_coins:
            score += coin.weight 
            new_coin = Coin()
            coins.add(new_coin)
            all_sprites.add(new_coin)

        if pygame.sprite.spritecollideany(P1, enemies):
            pygame.mixer.music.stop() 
            pygame.mixer.Sound.play(crash_sound) 
            screen.fill(RED)
            game_over_text = font.render("GAME OVER", True, BLACK)
            screen.blit(game_over_text, (SCREEN_WIDTH//2 - 60, SCREEN_HEIGHT//2))
            pygame.display.update()
            pygame.time.delay(2000) 
            pygame.quit()
            sys.exit()

        score_text = font.render(f"Score: {score} | Enemy Speed: {new_enemy_speed}", True, BLACK)
        screen.blit(score_text, (10, 10))

        pygame.display.update()
        clock.tick(60)