import pygame
import sys
sys.path.append("./src")

from pygame.sprite import Group
from src.settings import Settings
from src.objects.vaccine import Vaccine
import src.functions as utility
from src.objects.corona import Corona
from src.gameStats import GameStats
from src.objects.button import Button
from src.scoreboard import ScoreBoard
from src.objects.background import Background


def run_game():

    pygame.init()  # Initialize game and create a screen object.

    game_settings = Settings()  # Make it constructor.Make an instance.

    

    screen = pygame.display.set_mode((game_settings.screen_width, game_settings.screen_height))  # Set screen size
    corona = Corona(game_settings, screen)  # Make Corona.
    pygame.display .set_caption("DEATH 2 CORONA")

    # Make the Play button.
    play_button = Button(game_settings, screen, "Play")  # Make Button.

    vaccine = Vaccine(screen, game_settings)  # Make a a vaccine.

    stats = GameStats(game_settings)  # Create an instance to store game statistics.

    sb = ScoreBoard(game_settings, screen, stats)
    bullets = Group()  # Make a group of bullets.
    coronas = Group()  # # Make a group of coronas.

    # Create the fleet of coronas.
    utility.create_fleet(game_settings, screen, coronas, vaccine)

    # Start main loop for the game.
    while True:
        # Watch Keyboard and Mouse events.
        utility.check_events(vaccine, game_settings, screen, bullets, play_button, stats, coronas, sb)
        if stats.game_active:
            vaccine.update()
            utility.update_bullets(bullets, coronas, game_settings, screen, vaccine, stats, sb)  # Updating bullets.
            utility.update_coronas(game_settings, coronas, vaccine, stats, screen, bullets, sb)  # Update coronas.
        # Updating or loading the screen.
        utility.update_screen(game_settings, screen, vaccine, bullets, coronas, play_button, stats, sb)


if __name__ == '__main__':
    run_game()

