import pygame
import sys
from persistence import load_settings, save_settings, load_leaderboard, save_leaderboard
from ui import Button, draw_text
import racer

pygame.init()
WIDTH, HEIGHT = 400, 600
screen = pygame.display.set_mode((WIDTH, HEIGHT))
pygame.display.set_caption("TSIS 3 - Advanced Racer")

settings = load_settings()
leaderboard = load_leaderboard()
player_name = "Player" 

def main_menu():
    btn_play = Button(100, 200, 200, 50, "PLAY")
    btn_lb = Button(100, 280, 200, 50, "LEADERBOARD")
    btn_set = Button(100, 360, 200, 50, "SETTINGS")
    btn_quit = Button(100, 440, 200, 50, "QUIT")
    buttons = [btn_play, btn_lb, btn_set, btn_quit]

    while True:
        mouse_pos = pygame.mouse.get_pos()
        screen.fill((200, 220, 250))
        draw_text(screen, "RACER GAME", WIDTH//2, 100, center=True)

        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                sys.exit()
            if btn_play.is_clicked(event): return "PLAY"
            if btn_lb.is_clicked(event): return "LEADERBOARD"
            if btn_set.is_clicked(event): return "SETTINGS"
            if btn_quit.is_clicked(event): sys.exit()

        for btn in buttons:
            btn.check_hover(mouse_pos)
            btn.draw(screen)

        pygame.display.flip()

def settings_menu():
    global settings
    btn_color = Button(100, 200, 200, 50, f"Color: {settings['car_color']}")
    btn_diff = Button(100, 280, 200, 50, f"Diff: {settings['difficulty']}")
    btn_back = Button(100, 400, 200, 50, "BACK")

    colors = ["Red", "Blue", "Green"]
    diffs = ["Easy", "Normal", "Hard"]

    while True:
        mouse_pos = pygame.mouse.get_pos()
        screen.fill((200, 220, 250))
        draw_text(screen, "SETTINGS", WIDTH//2, 100, center=True)

        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                sys.exit()
            if btn_color.is_clicked(event):
                idx = (colors.index(settings['car_color']) + 1) % len(colors)
                settings['car_color'] = colors[idx]
                btn_color.text = f"Color: {settings['car_color']}"
            if btn_diff.is_clicked(event):
                idx = (diffs.index(settings['difficulty']) + 1) % len(diffs)
                settings['difficulty'] = diffs[idx]
                btn_diff.text = f"Diff: {settings['difficulty']}"
            if btn_back.is_clicked(event):
                save_settings(settings)
                return "MENU"

        for btn in [btn_color, btn_diff, btn_back]:
            btn.check_hover(mouse_pos)
            btn.draw(screen)

        pygame.display.flip()

def leaderboard_menu():
    btn_back = Button(100, 500, 200, 50, "BACK")
    
    while True:
        mouse_pos = pygame.mouse.get_pos()
        screen.fill((200, 220, 250))
        draw_text(screen, "TOP SCORES", WIDTH//2, 50, center=True)

        y = 120
        for i, entry in enumerate(leaderboard[:10]):
            txt = f"{i+1}. {entry['name']} - {entry['score']} (Dist: {entry['distance']})"
            draw_text(screen, txt, 50, y)
            y += 35

        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                sys.exit()
            if btn_back.is_clicked(event):
                return "MENU"

        btn_back.check_hover(mouse_pos)
        btn_back.draw(screen)
        pygame.display.flip()

def game_over_screen(result):
    btn_retry = Button(100, 300, 200, 50, "RETRY")
    btn_menu = Button(100, 380, 200, 50, "MAIN MENU")
    
    while True:
        mouse_pos = pygame.mouse.get_pos()
        screen.fill((250, 200, 200))
        draw_text(screen, "GAME OVER", WIDTH//2, 100, center=True)
        draw_text(screen, f"Score: {result['score']}", WIDTH//2, 160, center=True)
        draw_text(screen, f"Distance: {result['distance']}", WIDTH//2, 200, center=True)

        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                sys.exit()
            if btn_retry.is_clicked(event): return "PLAY"
            if btn_menu.is_clicked(event): return "MENU"

        for btn in [btn_retry, btn_menu]:
            btn.check_hover(mouse_pos)
            btn.draw(screen)

        pygame.display.flip()


state = "MENU"
while True:
    if state == "MENU":
        state = main_menu()
    elif state == "SETTINGS":
        state = settings_menu()
    elif state == "LEADERBOARD":
        state = leaderboard_menu()
    elif state == "PLAY":
        result = racer.run_game(screen, settings, player_name)
        if result:
            leaderboard.append(result)
            save_leaderboard(leaderboard)
            state = "GAME_OVER"
        else:
            sys.exit()
    elif state == "GAME_OVER":
        state = game_over_screen(result)