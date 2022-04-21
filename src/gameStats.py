import json

class GameStats():
    """Track statistics for corona Invasion."""
    def __init__(self, game_settings):
        """Initialize statistics."""
        self.game_settings = game_settings
        self.high_score = json.load(open('./src/resource/data.json',))["high"]
        #self.high_score = int()  # High Scores should never be reset.
        self.level = 1  # Game level.
        self.reset_stats()

        # Start corona Shooter in an active state.
        self.game_active = False


    def reset_stats(self):
        """Initialize statistics that can change during the game."""
        self.vaccines_left = self.game_settings.vaccine_limit
        self.score = 0
        self.level = 1


if __name__ == '__main__':
    print("Go to main file and run from there.")
