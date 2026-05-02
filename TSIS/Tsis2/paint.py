import pygame
import sys
import math
import datetime
import os
from tools import get_shape_points, flood_fill

def run_app():
    pygame.init()
    
    WIDTH, HEIGHT = 900, 700
    screen = pygame.display.set_mode((WIDTH, HEIGHT))
    pygame.display.set_caption("TSIS 2 - Advanced Paint")

    WHITE = (255, 255, 255)
    GRAY = (220, 220, 220)
    BLACK = (0, 0, 0)
    RED = (255, 0, 0)
    GREEN = (0, 255, 0)
    BLUE = (0, 0, 255)
    
    COLORS = [BLACK, RED, GREEN, BLUE]
    COLOR_NAMES = ['Black', 'Red', 'Green', 'Blue']
    color_idx = 0

    tool = 'pencil'
    TOOL_NAMES = {
        'pencil': 'Pencil', 'line': 'Line', 'rect': 'Rectangle', 
        'circle': 'Circle', 'square': 'Square', 'right_tri': 'R. Triangle',
        'eq_tri': 'Eq. Triangle', 'rhombus': 'Rhombus', 'eraser': 'Eraser',
        'fill': 'Fill', 'text': 'Text'
    }

    SIZES = {pygame.K_1: 2, pygame.K_2: 5, pygame.K_3: 10}
    brush_size = 5

    ui_font = pygame.font.SysFont("Verdana", 14)
    text_tool_font = pygame.font.SysFont("Verdana", 24)
    
    canvas = pygame.Surface((WIDTH, HEIGHT))
    canvas.fill(WHITE)

    drawing = False
    typing_text = False
    text_input = ""
    text_pos = (0, 0)
    start_pos = (0, 0)
    last_pos = (0, 0)

    clock = pygame.time.Clock()

    while True:
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                pygame.quit(); sys.exit()

            mods = pygame.key.get_mods()

            if event.type == pygame.KEYDOWN:
                if typing_text:
                    if event.key == pygame.K_RETURN:
                        txt_surface = text_tool_font.render(text_input, True, COLORS[color_idx])
                        canvas.blit(txt_surface, text_pos)
                        typing_text = False
                    elif event.key == pygame.K_ESCAPE:
                        typing_text = False
                    elif event.key == pygame.K_BACKSPACE:
                        text_input = text_input[:-1]
                    else:
                        text_input += event.unicode
                    continue

                if event.key == pygame.K_s and (mods & pygame.KMOD_CTRL or mods & pygame.KMOD_META):
                    timestamp = datetime.datetime.now().strftime("%Y-%m-%d_%H-%M-%S")
                    filename = f"canvas_{timestamp}.png"
                    pygame.image.save(canvas, filename)
                    continue

                if event.key in SIZES:
                    brush_size = SIZES[event.key]
                
                if event.key == pygame.K_SPACE:
                    color_idx = (color_idx + 1) % len(COLORS)
                
                if event.key == pygame.K_p: tool = 'pencil'
                if event.key == pygame.K_l: tool = 'line'
                if event.key == pygame.K_r: tool = 'rect'
                if event.key == pygame.K_c: tool = 'circle'
                if event.key == pygame.K_s and not (mods & pygame.KMOD_CTRL or mods & pygame.KMOD_META): tool = 'square'
                if event.key == pygame.K_t: tool = 'right_tri'
                if event.key == pygame.K_y: tool = 'eq_tri'
                if event.key == pygame.K_h: tool = 'rhombus'
                if event.key == pygame.K_e: tool = 'eraser'
                if event.key == pygame.K_f: tool = 'fill'
                if event.key == pygame.K_x: tool = 'text'

            if event.type == pygame.MOUSEBUTTONDOWN:
                if event.button == 1 and event.pos[1] > 40:
                    if tool == 'fill':
                        target_color = canvas.get_at(event.pos)
                        fill_color = COLORS[color_idx]
                        flood_fill(canvas, event.pos[0], event.pos[1], target_color, fill_color)
                    elif tool == 'text':
                        typing_text = True
                        text_pos = event.pos
                        text_input = ""
                    else:
                        drawing = True
                        start_pos = event.pos
                        last_pos = event.pos

            if event.type == pygame.MOUSEBUTTONUP:
                if event.button == 1 and drawing:
                    drawing = False
                    end_pos = event.pos
                    current_color = COLORS[color_idx]
                    
                    if tool == 'line':
                        pygame.draw.line(canvas, current_color, start_pos, end_pos, brush_size)
                    elif tool == 'rect':
                        w, h = abs(start_pos[0] - end_pos[0]), abs(start_pos[1] - end_pos[1])
                        pygame.draw.rect(canvas, current_color, (min(start_pos[0], end_pos[0]), min(start_pos[1], end_pos[1]), w, h), brush_size)
                    elif tool == 'circle':
                        radius = int(math.hypot(end_pos[0] - start_pos[0], end_pos[1] - start_pos[1]))
                        pygame.draw.circle(canvas, current_color, start_pos, radius, brush_size)
                    elif tool in ['square', 'right_tri', 'eq_tri', 'rhombus']:
                        points = get_shape_points(tool, start_pos, end_pos)
                        if points: pygame.draw.polygon(canvas, current_color, points, brush_size)

            if event.type == pygame.MOUSEMOTION:
                if drawing:
                    if tool == 'pencil':
                        pygame.draw.line(canvas, COLORS[color_idx], last_pos, event.pos, brush_size)
                        last_pos = event.pos
                    elif tool == 'eraser':
                        pygame.draw.circle(canvas, WHITE, event.pos, brush_size * 3)

        screen.blit(canvas, (0, 0))
        pygame.draw.rect(screen, GRAY, (0, 0, WIDTH, 40))
        
        if drawing and tool not in ['pencil', 'eraser', 'fill', 'text']:
            mouse_pos = pygame.mouse.get_pos()
            current_color = COLORS[color_idx]
            if tool == 'line':
                pygame.draw.line(screen, current_color, start_pos, mouse_pos, brush_size)
            elif tool == 'rect':
                w, h = abs(start_pos[0] - mouse_pos[0]), abs(start_pos[1] - mouse_pos[1])
                pygame.draw.rect(screen, current_color, (min(start_pos[0], mouse_pos[0]), min(start_pos[1], mouse_pos[1]), w, h), brush_size)
            elif tool == 'circle':
                radius = int(math.hypot(mouse_pos[0] - start_pos[0], mouse_pos[1] - start_pos[1]))
                pygame.draw.circle(screen, current_color, start_pos, radius, brush_size)
            elif tool in ['square', 'right_tri', 'eq_tri', 'rhombus']:
                points = get_shape_points(tool, start_pos, mouse_pos)
                if len(points) > 2: pygame.draw.polygon(screen, current_color, points, brush_size)

        if typing_text:
            txt_surface = text_tool_font.render(text_input + "|", True, COLORS[color_idx])
            screen.blit(txt_surface, text_pos)

        ui_t1 = f"Tool: {TOOL_NAMES[tool]} | Size: {brush_size}px (1,2,3) | Color: {COLOR_NAMES[color_idx]} (Space) | Save: Ctrl+S"
        ui_t2 = "Keys: P(Pencil) L(Line) R(Rect) C(Circ) S(Square) T(R.Tri) Y(Eq.Tri) H(Rhombus) E(Eraser) F(Fill) X(Text)"
        screen.blit(ui_font.render(ui_t1, True, BLACK), (10, 2))
        screen.blit(ui_font.render(ui_t2, True, BLACK), (10, 20))

        pygame.display.flip()
        clock.tick(120)

if __name__== '__main__':
    run_app()