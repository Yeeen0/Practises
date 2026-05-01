import pygame


class Ball:
    """
    A red ball (radius 25, so 50x50 pixels) that moves by 20 pixels
    per arrow key press and cannot leave the screen boundaries.
    """

    RADIUS = 25       # Ball radius (50x50 effective size)
    STEP = 20         # Pixels per key press
    COLOR = (220, 30, 30)  # Red

    def __init__(self, screen_width, screen_height):
        self.screen_width = screen_width
        self.screen_height = screen_height
        # Start ball at the center of the screen
        self.x = screen_width // 2
        self.y = screen_height // 2

    def move(self, direction):
        """
        Move ball in the given direction by STEP pixels.
        Ignores input that would move the ball off-screen.
        direction: "up" | "down" | "left" | "right"
        """
        new_x, new_y = self.x, self.y

        if direction == "up":
            new_y -= self.STEP
        elif direction == "down":
            new_y += self.STEP
        elif direction == "left":
            new_x -= self.STEP
        elif direction == "right":
            new_x += self.STEP

        # Only apply move if the ball stays fully within the screen
        if self._is_within_bounds(new_x, new_y):
            self.x = new_x
            self.y = new_y
        # If out of bounds, ignore the input (do nothing)

    def _is_within_bounds(self, x, y):
        """Check that the ball (with radius) stays inside the screen."""
        return (
            self.RADIUS <= x <= self.screen_width - self.RADIUS and
            self.RADIUS <= y <= self.screen_height - self.RADIUS
        )

    def draw(self, surface):
        """Draw the red ball on the given surface."""
        pygame.draw.circle(surface, self.COLOR, (self.x, self.y), self.RADIUS)
