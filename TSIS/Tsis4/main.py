import pygame
import sys
import json
import os
import db
import game

pygame.init()
WIDTH, HEIGHT = 600, 400
screen = pygame.display.set_mode((WIDTH, HEIGHT))
pygame.display.set_caption("TSIS 4 - Database Snake")

font_main = pygame.font.SysFont("Verdana", 24)
font_small = pygame.font.SysFont("Verdana", 16)

def load_settings():
    if os.path.exists("settings.json"):
        with open("settings.json", "r") as f:
            return json.load(f)
    return {"snake_color": [0, 255, 0], "grid": False, "sound": True}

def save_settings(s):
    with open("settings.json", "w") as f:
        json.dump(s, f)

settings = load_settings()
player_name = ""

try:
    db.init_db()
    db_connected = True
except Exception as e:
    print(f"Ошибка БД: {e}")
    db_connected = False

def draw_text(surf, text, x, y, color=(255, 255, 255), center=False):
    t = font_main.render(text, True, color)
    r = t.get_rect(center=(x,y)) if center else t.get_rect(topleft=(x,y))
    surf.blit(t, r)

def main_menu():
    global player_name
    input_active = False
    
    while True:
        screen.fill((30, 30, 50))
        draw_text(screen, "TSIS 4: SNAKE DB", WIDTH//2, 50, center=True)
        draw_text(screen, "Enter Username:", WIDTH//2, 120, center=True)
        
        color = (100, 255, 100) if input_active else (255, 255, 255)
        pygame.draw.rect(screen, color, (150, 150, 300, 40), 2)
        draw_text(screen, player_name, 160, 155, color)

        draw_text(screen, "[ENTER] to Play", WIDTH//2, 230, center=True)
        draw_text(screen, "[L] Leaderboard  |  [S] Settings", WIDTH//2, 280, center=True)
        draw_text(screen, "DB Status: " + ("OK" if db_connected else "ERROR"), WIDTH//2, 350, (0, 255, 0) if db_connected else (255, 0, 0), True)

        for event in pygame.event.get():
            if event.type == pygame.QUIT: sys.exit()
            if event.type == pygame.MOUSEBUTTONDOWN:
                if 150 <= event.pos[0] <= 450 and 150 <= event.pos[1] <= 190:
                    input_active = True
                else:
                    input_active = False
            if event.type == pygame.KEYDOWN:
                if input_active:
                    if event.key == pygame.K_RETURN and player_name != "":
                        return "PLAY"
                    elif event.key == pygame.K_BACKSPACE:
                        player_name = player_name[:-1]
                    else:
                        player_name += event.unicode
                else:
                    if event.key == pygame.K_RETURN and player_name != "": return "PLAY"
                    if event.key == pygame.K_l: return "LEADERS"
                    if event.key == pygame.K_s: 
                        if not db_connected:
                            print("Предупреждение: Настройки открыты без БД")
                        return "SETTINGS"

        pygame.display.flip()

def leaderboard_menu():
    while True:
        screen.fill((30, 30, 50))
        draw_text(screen, "TOP 10 LEADERBOARD", WIDTH//2, 30, center=True)
        
        if db_connected:
            top = db.get_top_10()
            y = 80
            for i, r in enumerate(top):
                txt = f"{i+1}. {r[0][:10]} - Score: {r[1]} (Lvl {r[2]})"
                t_surf = font_small.render(txt, True, (255, 255, 255))
                screen.blit(t_surf, (50, y))
                y += 25
        else:
            draw_text(screen, "DATABASE NOT CONNECTED", WIDTH//2, 150, (255, 0, 0), center=True)

        draw_text(screen, "[ESC] Back", WIDTH//2, 350, center=True)

        for event in pygame.event.get():
            if event.type == pygame.QUIT: sys.exit()
            if event.type == pygame.KEYDOWN and event.key == pygame.K_ESCAPE:
                return "MENU"
        pygame.display.flip()

def settings_menu():
    global settings
    colors = [[0, 255, 0], [255, 255, 0], [0, 255, 255]]
    c_names = ["Green", "Yellow", "Cyan"]
    try:
        c_idx = colors.index(settings["snake_color"])
    except:
        c_idx = 0

    while True:
        screen.fill((30, 30, 50))
        draw_text(screen, "SETTINGS", WIDTH//2, 50, center=True)
        
        draw_text(screen, f"[C] Color: {c_names[c_idx]}", WIDTH//2, 150, center=True)
        draw_text(screen, f"[G] Grid: {'ON' if settings['grid'] else 'OFF'}", WIDTH//2, 200, center=True)
        draw_text(screen, "[ESC] Save & Back", WIDTH//2, 300, center=True)

        for event in pygame.event.get():
            if event.type == pygame.QUIT: sys.exit()
            if event.type == pygame.KEYDOWN:
                if event.key == pygame.K_c:
                    c_idx = (c_idx + 1) % len(colors)
                    settings["snake_color"] = colors[c_idx]
                if event.key == pygame.K_g:
                    settings["grid"] = not settings["grid"]
                if event.key == pygame.K_ESCAPE:
                    save_settings(settings)
                    return "MENU"
        pygame.display.flip()

def game_over_screen(result, pb):
    while True:
        screen.fill((50, 20, 20))
        draw_text(screen, "GAME OVER", WIDTH//2, 100, (255, 50, 50), center=True)
        draw_text(screen, f"Score: {result['score']} (Level {result['level']})", WIDTH//2, 160, center=True)
        draw_text(screen, f"Personal Best: {max(pb, result['score'])}", WIDTH//2, 200, (255, 215, 0), center=True)
        
        draw_text(screen, "[ENTER] Retry  |  [ESC] Menu", WIDTH//2, 300, center=True)

        for event in pygame.event.get():
            if event.type == pygame.QUIT: sys.exit()
            if event.type == pygame.KEYDOWN:
                if event.key == pygame.K_RETURN: return "PLAY"
                if event.key == pygame.K_ESCAPE: return "MENU"
        pygame.display.flip()

state = "MENU"
while True:
    if state == "MENU":
        state = main_menu()
    elif state == "LEADERS":
        state = leaderboard_menu()
    elif state == "SETTINGS":
        state = settings_menu()
    elif state == "PLAY":
        pb = db.get_personal_best(player_name) if db_connected else 0
        result = game.run_game(screen, settings, player_name, pb)
        if result:
            if db_connected:
                db.save_score(player_name, result["score"], result["level"])
            state = "GAME_OVER"
        else:
            sys.exit()
    elif state == "GAME_OVER":
        state = game_over_screen(result, pb)