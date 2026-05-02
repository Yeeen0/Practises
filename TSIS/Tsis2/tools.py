import pygame

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

def flood_fill(surface, x, y, target_color, fill_color):
    if target_color == fill_color:
        return
    
    width, height = surface.get_size()
    stack = [(x, y)]
    
    while stack:
        cx, cy = stack.pop()
        if 0 <= cx < width and 0 <= cy < height:
            if surface.get_at((cx, cy)) == target_color:
                surface.set_at((cx, cy), fill_color)
                stack.append((cx - 1, cy))
                stack.append((cx + 1, cy))
                stack.append((cx, cy - 1))
                stack.append((cx, cy + 1))