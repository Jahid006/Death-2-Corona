import pygame
from pygame.sprite import Sprite
import numpy as np


class Corona(Sprite):
    def __init__(self, game_settings, screen):

        super().__init__()
        self.screen = screen
        self.game_settings = game_settings

        self.image = pygame.image.load('./src/resource/corona.bmp')
        self.rect = self.image.get_rect()

        # Start each new corona near the top left of the screen.
        self.rect.x = self.rect.width
        self.rect.y = self.rect.height

        # Store the corona's exact position.
        self.x = float(self.rect.x)

    def blitme(self):
        self.screen.blit(self.image, self.rect)  # Draw the corona at its current location.

    def update(self):
        """Move the corona right or left."""

        self.x += (self.game_settings.corona_speed_factor * self.game_settings.fleet_direction)# * np.random.choice([1,1,1,1,1,-1])
        self.rect.x = self.x  

    def check_edges(self):
        """Return True if corona is at edge of screen."""
        screen_rect = self.screen.get_rect()

        if self.rect.right >= screen_rect.width:
            return True
        elif self.rect.left <= 0:
            return True


if __name__ == '__main__':
    print("Go to main file and run from there.")
