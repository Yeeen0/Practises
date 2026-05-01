"""
Music Player with Keyboard Controller
Controls:
  P - Play
  S - Stop
  N - Next track
  B - Previous (Back) track
  Q - Quit
"""

import pygame
import sys
from player import MusicPlayer


def draw_ui(screen, player, fonts):
    """Draw the player UI: title, track info, status, controls."""
    screen.fill((30, 30, 30))  # Dark background

    title_font, info_font, control_font = fonts

    # ----- Title -----
    title = title_font.render("Music Player", True, (255, 220, 50))
    screen.blit(title, (screen.get_width() // 2 - title.get_width() // 2, 40))

    # ----- Track info -----
    track_label = info_font.render("Now Playing:", True, (180, 180, 180))
    screen.blit(track_label, (60, 130))

    track_name = info_font.render(player.get_track_name(), True, (255, 255, 255))
    screen.blit(track_name, (60, 165))

    # Track index / total
    if player.track_count() > 0:
        index_str = f"Track {player.current_index + 1} / {player.track_count()}"
    else:
        index_str = "No tracks loaded"
    index_text = info_font.render(index_str, True, (150, 150, 150))
    screen.blit(index_text, (60, 205))

    # ----- Status -----
    status_color = (80, 220, 80) if player.is_playing else (220, 80, 80)
    status_text = info_font.render(f"Status: {player.get_status()}", True, status_color)
    screen.blit(status_text, (60, 255))

    # Playback position
    pos_text = info_font.render(f"Position: {player.get_position()}s", True, (180, 180, 180))
    screen.blit(pos_text, (60, 295))

    # ----- Separator -----
    pygame.draw.line(screen, (80, 80, 80), (40, 340), (760, 340), 2)

    # ----- Keyboard controls -----
    controls = [
        ("[P] Play", (80, 200, 80)),
        ("[S] Stop", (200, 80, 80)),
        ("[N] Next", (80, 150, 220)),
        ("[B] Back", (220, 150, 80)),
        ("[Q] Quit", (180, 80, 180)),
    ]
    cx = 60
    for label, color in controls:
        ctrl = control_font.render(label, True, color)
        screen.blit(ctrl, (cx, 370))
        cx += 150


def main():
    pygame.init()

    SCREEN_WIDTH = 800
    SCREEN_HEIGHT = 500
    FPS = 30

    screen = pygame.display.set_mode((SCREEN_WIDTH, SCREEN_HEIGHT))
    pygame.display.set_caption("Music Player")
    clock = pygame.time.Clock()

    # Fonts
    title_font = pygame.font.SysFont("Arial", 48, bold=True)
    info_font = pygame.font.SysFont("Arial", 28)
    control_font = pygame.font.SysFont("Arial", 22)
    fonts = (title_font, info_font, control_font)

    # Create player
    player = MusicPlayer(music_folder="music")

    # Main loop
    while True:
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                player.stop()
                pygame.quit()
                sys.exit()

            if event.type == pygame.KEYDOWN:
                if event.key == pygame.K_p:      # Play
                    player.play()
                elif event.key == pygame.K_s:    # Stop
                    player.stop()
                elif event.key == pygame.K_n:    # Next track
                    player.next_track()
                elif event.key == pygame.K_b:    # Previous (Back)
                    player.previous_track()
                elif event.key == pygame.K_q:    # Quit
                    player.stop()
                    pygame.quit()
                    sys.exit()

        draw_ui(screen, player, fonts)
        pygame.display.flip()
        clock.tick(FPS)


if __name__ == "__main__":
    main()
