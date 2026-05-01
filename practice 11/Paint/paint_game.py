import pygame
import sys

def run_game():
    pygame.init()
    
    WIDTH, HEIGHT = 800, 600
    screen = pygame.display.set_mode((WIDTH, HEIGHT))
    pygame.display.set_caption("Paint - Practice 11")

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
        'brush': '1-Кисть',
        'square': '2-Квадрат',
        'right_tri': '3-Прям. Треуг.',
        'eq_tri': '4-Равн. Треуг.',
        'rhombus': '5-Ромб',
        'eraser': '6-Ластик'
    }

    font = pygame.font.SysFont("Verdana", 14)
    canvas = pygame.Surface((WIDTH, HEIGHT))
    canvas.fill(WHITE)

    drawing = False
    tool = 'brush'
    current_color = COLORS[color_index]
    start_pos = (0, 0)
    brush_size = 3

    clear_button = pygame.Rect(WIDTH - 110, 5, 100, 25)
    clock = pygame.time.Clock()

    def get_shape_points(tool_type, start, end):
        if tool_type == 'square':
            side = max(abs(end[0] - start[0]), abs(end[1] - start[1]))
            dx = 1 if end[0] > start[0] else -1
            dy = 1 if end[1] > start[1] else -1
            return [
                start, 
                (start[0] + side*dx, start[1]), 
                (start[0] + side*dx, start[1] + side*dy), 
                (start[0], start[1] + side*dy)
            ]
        elif tool_type == 'right_tri':
            return [start, (start[0], end[1]), end]
        elif tool_type == 'eq_tri':
            mid_x = (start[0] + end[0]) // 2
            return [(mid_x, start[1]), (start[0], end[1]), end]
        elif tool_type == 'rhombus':
            mid_x = (start[0] + end[0]) // 2
            mid_y = (start[1] + end[1]) // 2
            return [(mid_x, start[1]), (end[0], mid_y), (mid_x, end[1]), (start[0], mid_y)]
        return []

    while True:
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                pygame.quit(); sys.exit()

            if event.type == pygame.KEYDOWN:
                if event.key == pygame.K_1: tool = 'brush'
                if event.key == pygame.K_2: tool = 'square'
                if event.key == pygame.K_3: tool = 'right_tri'
                if event.key == pygame.K_4: tool = 'eq_tri'
                if event.key == pygame.K_5: tool = 'rhombus'
                if event.key == pygame.K_6: tool = 'eraser'
                if event.key == pygame.K_c:
                    color_index = (color_index + 1) % len(COLORS)
                    current_color = COLORS[color_index]

            if event.type == pygame.MOUSEBUTTONDOWN:
                if event.button == 1:
                    if clear_button.collidepoint(event.pos):
                        canvas.fill(WHITE)
                    elif event.pos[1] > 35:
                        drawing = True
                        start_pos = event.pos

            if event.type == pygame.MOUSEBUTTONUP:
                if event.button == 1 and drawing:
                    drawing = False
                    end_pos = event.pos
                    points = get_shape_points(tool, start_pos, end_pos)
                    if points:
                        pygame.draw.polygon(canvas, current_color, points, brush_size)

            if event.type == pygame.MOUSEMOTION:
                if drawing:
                    if tool == 'brush':
                        pygame.draw.circle(canvas, current_color, event.pos, brush_size)
                    elif tool == 'eraser':
                        pygame.draw.circle(canvas, WHITE, event.pos, brush_size * 5)

        screen.blit(canvas, (0, 0))
        pygame.draw.rect(screen, GRAY, (0, 0, WIDTH, 35))
        
        ui_text = f"Инструмент: {TOOL_NAMES[tool]}   |   Цвет (C): {COLOR_NAMES[color_index]}"
        screen.blit(font.render(ui_text, True, BLACK), (10, 8))

        pygame.draw.rect(screen, DARK_GRAY, clear_button)
        pygame.draw.rect(screen, BLACK, clear_button, 2)
        screen.blit(font.render("ОЧИСТИТЬ", True, WHITE), (clear_button.x + 10, clear_button.y + 3))

        if drawing and tool not in ['brush', 'eraser']:
            mouse_pos = pygame.mouse.get_pos()
            points = get_shape_points(tool, start_pos, mouse_pos)
            if len(points) > 2: 
                pygame.draw.polygon(screen, current_color, points, brush_size)

        pygame.display.flip()
        clock.tick(120)