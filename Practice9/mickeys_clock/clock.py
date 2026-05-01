import pygame
import pygame.freetype
import datetime
import math


class MickeysClock:
    """
    Clock class that uses Mickey Mouse hands as clock hands.
    Right hand = minutes hand
    Left hand  = seconds hand
    """

    def __init__(self, screen_width=600, screen_height=600):
        self.screen_width = screen_width
        self.screen_height = screen_height
        self.center = (screen_width // 2, screen_height // 2)

        # Load mickey hand image (used for both hands)
        self.hand_image = pygame.image.load("images/mickey_hand.png").convert_alpha()
        # Scale hand to a reasonable size
        self.hand_image = pygame.transform.scale(self.hand_image, (60, 160))

    def get_current_time(self):
        """Return current minutes and seconds from system clock."""
        now = datetime.datetime.now()
        return now.minute, now.second

    def get_angle(self, value, max_value):
        """
        Convert time value to rotation angle in degrees.
        0 = pointing up (12 o'clock), clockwise = positive.
        pygame.transform.rotate() rotates counter-clockwise, so we negate.
        """
        angle = (value / max_value) * 360
        return -angle

    def draw_hand(self, surface, image, angle):
        """
        Rotate and draw a hand centered on the clock center.
        Uses the technique from StackOverflow #54714144.
        """
        rotated = pygame.transform.rotate(image, angle)
        rect = rotated.get_rect(center=self.center)
        surface.blit(rotated, rect)

    def draw(self, surface):
        """Draw both clock hands for current time."""
        minutes, seconds = self.get_current_time()

        # Calculate angles (right hand = minutes, left hand = seconds)
        minute_angle = self.get_angle(minutes, 60)
        second_angle = self.get_angle(seconds, 60)

        # Draw minutes hand (right hand)
        minute_hand = pygame.transform.scale(self.hand_image, (55, 150))
        self.draw_hand(surface, minute_hand, minute_angle)

        # Draw seconds hand (left hand) - flip horizontally for "left" hand look
        second_hand = pygame.transform.scale(self.hand_image, (45, 130))
        second_hand = pygame.transform.flip(second_hand, True, False)
        self.draw_hand(surface, second_hand, second_angle)

    def draw_clock_face(self, surface):
        """Draw clock face with hour tick marks."""
        pygame.draw.circle(surface, (200, 200, 200), self.center, 240, 4)

        for i in range(12):
            angle_rad = math.radians(i * 30 - 90)
            outer_x = self.center[0] + int(220 * math.cos(angle_rad))
            outer_y = self.center[1] + int(220 * math.sin(angle_rad))
            inner_x = self.center[0] + int(200 * math.cos(angle_rad))
            inner_y = self.center[1] + int(200 * math.sin(angle_rad))
            pygame.draw.line(surface, (80, 80, 80), (inner_x, inner_y), (outer_x, outer_y), 4)

        # Center dot
        pygame.draw.circle(surface, (50, 50, 50), self.center, 8)

    def draw_time_text(self, surface, ft_font):
        """Display current time MM:SS using freetype font."""
        minutes, seconds = self.get_current_time()
        time_str = f"{minutes:02d}:{seconds:02d}"
        # freetype.render_to(surface, dest, text, fgcolor)
        text_surf, rect = ft_font.render(time_str, (50, 50, 50))
        dest_x = self.screen_width // 2 - rect.width // 2
        dest_y = self.screen_height - 55
        ft_font.render_to(surface, (dest_x, dest_y), time_str, (50, 50, 50))
