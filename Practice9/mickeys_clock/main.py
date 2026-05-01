"""
Mickey's Clock Application
Displays current time (minutes and seconds) using Mickey Mouse hands.
Right hand = minutes, Left hand = seconds.
"""

import pygame
import pygame.freetype   # Use freetype instead of font (fixes Python 3.14 bug)
import sys
from clock import MickeysClock


def main():
    pygame.init()
    pygame.freetype.init()

    # Screen settings
    SCREEN_WIDTH = 600
    SCREEN_HEIGHT = 600
    FPS = 1  # Update every second (synced to clock)

    screen = pygame.display.set_mode((SCREEN_WIDTH, SCREEN_HEIGHT))
    pygame.display.set_caption("Mickey's Clock")
    clock_tick = pygame.time.Clock()

    # Background color (cream, like the Mickey clock face)
    BG_COLOR = (255, 248, 220)

    # Font via freetype (avoids circular import on Python 3.14)
    ft_font = pygame.freetype.SysFont("Arial", 40, bold=True)

    # Create clock object
    mickey_clock = MickeysClock(SCREEN_WIDTH, SCREEN_HEIGHT)

    # Main loop
    while True:
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                pygame.quit()
                sys.exit()
            if event.type == pygame.KEYDOWN:
                if event.key == pygame.K_ESCAPE:
                    pygame.quit()
                    sys.exit()

        # Draw background
        screen.fill(BG_COLOR)

        # Draw clock face (tick marks, outline)
        mickey_clock.draw_clock_face(screen)

        # Draw Mickey's hands (minutes + seconds)
        mickey_clock.draw(screen)

        # Draw time as text (MM:SS)
        mickey_clock.draw_time_text(screen, ft_font)

        pygame.display.flip()

        # Sync to ~1 FPS so we update every second
        clock_tick.tick(FPS)


if __name__ == "__main__":
    main()
