import pygame.font
from objects.vaccine import Vaccine
from pygame.sprite import Group


class ScoreBoard:
    def __init__(self, game_settings, screen, stats):
        self.screen = screen
        self.screen_rect = screen.get_rect()
        self.game_settings = game_settings
        self.stats = stats

        # Font settings for scoring information.
        self.text_color = (0, 0, 0)
        self.font = pygame.font.Font('./src/resource/BRLNSR.ttf', 20)

        # Prepare the initial score, level, high score and vaccines images.
        self.prep_score()
        self.prep_high_score()
        self.prep_level()
        self.prep_vaccines()

    def prep_score(self):
        """Turn the score into a rendered image."""
        rounded_score = int(round(self.stats.score, -1))
        score_str = "Score: " + "{:,}".format(rounded_score)

        self.score_image = self.font.render(score_str, True, self.text_color, self.game_settings.bg_color)
        # Display the score at the top right of the screen.
        self.score_rect = self.score_image.get_rect()
        self.score_rect.right = self.screen_rect.right - 20
        self.score_rect.top = 20

    def prep_high_score(self):
        """Turning high score into a rendered image"""
        high_score = int(round(self.stats.high_score, -1))
        high_score_str = "High Score: " + "{:,}".format(high_score)

        self.high_score_image = self.font.render(high_score_str, True, self.text_color,
                                                 self.game_settings.bg_color)
        # Display the score at the top center of the screen.
        self.high_score_rect = self.high_score_image.get_rect()
        self.high_score_rect.centerx = self.screen_rect.centerx
        self.high_score_rect.top = self.score_rect.top

    def show_score(self):
        """Draw score to the screen."""
        self.screen.blit(self.score_image, self.score_rect)
        self.screen.blit(self.high_score_image, self.high_score_rect)
        self.screen.blit(self.level_image, self.level_rect)
        self.vaccines.draw(self.screen)

    def prep_level(self):
        """Turn the level into a rendered image."""

        self.level_image = self.font.render("Level: " + str(self.stats.level), True,
                                            self.text_color, self.game_settings.bg_color)
        # Position the level below the score.
        self.level_rect = self.level_image.get_rect()

        self.level_rect.right = self.score_rect.right

        self.level_rect.top = self.score_rect.bottom + 10

    def prep_vaccines(self):
        """Show how many vaccines are left."""
        self.vaccines = Group()
        for vaccine_number in range(self.stats.vaccines_left):
            vaccine = Vaccine(self.screen, self.game_settings)

            vaccine.rect.x = 10 + vaccine_number * vaccine.rect.width

            vaccine.rect.y = 10

            self.vaccines.add(vaccine)


if __name__ == '__main__':
    print("Go to main file and run from there.")