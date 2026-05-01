import pygame
import sys
import math

def run_game():
    pygame.init()
    
    WIDTH, HEIGHT = 800, 600
    screen = pygame.display.set_mode((WIDTH, HEIGHT))
    pygame.display.set_caption("Paint - Practice 10")

    WHITE = (255, 255, 255)
    GRAY = (220, 220, 220)
    DARK_GRAY = (150, 150, 150)
    BLACK = (0, 0, 0)
    RED = (255, 0, 0)
    GREEN = (0, 255, 0)
    BLUE = (0, 0, 255)
    
    COLORS = [BLACK, RED, GREEN, BLUE]
    COLOR_NAMES = ['Черный', 'Красный', 'Зеленый', 'Синий'] 
    color_index = 0

    TOOL_NAMES = {
        'brush': '1 - кисть',
        'rect': '2 - квадрат',
        'circle': '3 - круг',
        'eraser': '4 - ластик'
    }

    font = pygame.font.SysFont(None, 24)

    canvas = pygame.Surface((WIDTH, HEIGHT))
    canvas.fill(WHITE)

    drawing = False
    tool = 'brush'
    current_color = COLORS[color_index]
    start_pos = (0, 0)
    brush_size = 5

    clear_button = pygame.Rect(WIDTH - 130, 5, 120, 25)

    clock = pygame.time.Clock()

    while True:
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                pygame.quit()
                sys.exit()

            if event.type == pygame.KEYDOWN:
                if event.key == pygame.K_1: tool = 'brush'
                if event.key == pygame.K_2: tool = 'rect'
                if event.key == pygame.K_3: tool = 'circle'
                if event.key == pygame.K_4: tool = 'eraser'
                if event.key == pygame.K_c:
                    color_index = (color_index + 1) % len(COLORS)
                    current_color = COLORS[color_index]

            if event.type == pygame.MOUSEBUTTONDOWN:
                if event.button == 1: 
                    if clear_button.collidepoint(event.pos):
                        canvas.fill(WHITE) 
                    else:
                        if event.pos[1] > 35:
                            drawing = True
                            start_pos = event.pos

            if event.type == pygame.MOUSEBUTTONUP:
                if event.button == 1 and drawing:
                    drawing = False
                    end_pos = event.pos
                    if tool == 'rect':
                        x = min(start_pos[0], end_pos[0])
                        y = min(start_pos[1], end_pos[1])
                        w = abs(start_pos[0] - end_pos[0])
                        h = abs(start_pos[1] - end_pos[1])
                        pygame.draw.rect(canvas, current_color, (x, y, w, h), brush_size)
                    elif tool == 'circle':
                        radius = int(math.hypot(end_pos[0] - start_pos[0], end_pos[1] - start_pos[1]))
                        pygame.draw.circle(canvas, current_color, start_pos, radius, brush_size)

            if event.type == pygame.MOUSEMOTION:
                if drawing:
                    if tool == 'brush':
                        pygame.draw.circle(canvas, current_color, event.pos, brush_size)
                    elif tool == 'eraser':
                        pygame.draw.circle(canvas, WHITE, event.pos, brush_size * 5)

        screen.blit(canvas, (0, 0))
        
        pygame.draw.rect(screen, GRAY, (0, 0, WIDTH, 35))
        
        ui_text = f"Инструмент: {TOOL_NAMES[tool]}   |   Цвет (C): {COLOR_NAMES[color_index]}"
        text_surface = font.render(ui_text, True, BLACK)
        screen.blit(text_surface, (15, 6))

        pygame.draw.rect(screen, DARK_GRAY, clear_button) 
        pygame.draw.rect(screen, BLACK, clear_button, 2)  
        clear_text = font.render("ОЧИСТИТЬ", True, WHITE)
        screen.blit(clear_text, (clear_button.x + 12, clear_button.y + 2))

        if drawing and tool in ['rect', 'circle']:
            mouse_pos = pygame.mouse.get_pos()
            if tool == 'rect':
                x = min(start_pos[0], mouse_pos[0])
                y = min(start_pos[1], mouse_pos[1])
                w = abs(start_pos[0] - mouse_pos[0])
                h = abs(start_pos[1] - mouse_pos[1])
                pygame.draw.rect(screen, current_color, (x, y, w, h), brush_size)
            elif tool == 'circle':
                radius = int(math.hypot(mouse_pos[0] - start_pos[0], mouse_pos[1] - start_pos[1]))
                pygame.draw.circle(screen, current_color, start_pos, radius, brush_size)

        pygame.display.flip()
        clock.tick(120)
