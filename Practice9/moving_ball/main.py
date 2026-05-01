"""
Moving Ball Game
Move the red ball using arrow keys.
The ball cannot leave the screen boundaries.
"""

import pygame
import sys
from ball import Ball


def main():
    pygame.init()

    SCREEN_WIDTH = 800
    SCREEN_HEIGHT = 600
    FPS = 60
    BG_COLOR = (255, 255, 255)  # White background

    screen = pygame.display.set_mode((SCREEN_WIDTH, SCREEN_HEIGHT))
    pygame.display.set_caption("Moving Ball Game")
    clock = pygame.time.Clock()

    # Font for instructions
    font = pygame.font.SysFont("Arial", 20)

    # Create the ball at center of screen
    ball = Ball(SCREEN_WIDTH, SCREEN_HEIGHT)

    # Main game loop
    while True:
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                pygame.quit()
                sys.exit()

            # Move ball 20 pixels per arrow key press
            if event.type == pygame.KEYDOWN:
                if event.key == pygame.K_UP:
                    ball.move("up")
                elif event.key == pygame.K_DOWN:
                    ball.move("down")
                elif event.key == pygame.K_LEFT:
                    ball.move("left")
                elif event.key == pygame.K_RIGHT:
                    ball.move("right")
                elif event.key == pygame.K_ESCAPE:
                    pygame.quit()
                    sys.exit()

        # Draw white background
        screen.fill(BG_COLOR)

        # Draw the ball
        ball.draw(screen)

        # Draw instructions
        hint = font.render("Arrow keys to move  |  ESC to quit", True, (150, 150, 150))
        screen.blit(hint, (10, 10))

        pygame.display.flip()
        clock.tick(FPS)


if __name__ == "__main__":
    main()
