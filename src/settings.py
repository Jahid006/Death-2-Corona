# Game Settings below.


class Settings:

    def __init__(self):
        """Initialize games static settings"""
        """Screen settings"""
        self.screen_width = 900
        self.screen_height = 600
        self.bg_color = (81, 164, 189)#(230, 230, 230)  # Background color.

        """ Bullet settings """
        #self.bullet_speed_factor = 3
        self.bullet_width = 3
        self.bullet_height = 15
        self.bullet_color = (60, 60, 60)
        self.bullets_allowed = 3

        """ Vaccine Settings """

        self.vaccine_limit = 3

        """Corona Settings"""

        self.fleet_drop_speed = 10

        # How quickly the game speeds up
        self.speedup_scale = 2

        self.dynamic_settings()

        # Scoring
        self.corona_points = 1
        # How quickly the corona point values increase
        self.score_scale = 2

    def dynamic_settings(self):
        self.vaccine_speed_factor = .2
        self.bullet_speed_factor = 3
        self.corona_speed_factor = 0.1
        self.fleet_direction = 1  # fleet_direction of 1 represents right; -1 represents left.

    def increase_speed(self):
        """Increase speeds settings"""
        self.vaccine_speed_factor *= self.speedup_scale
        self.bullet_speed_factor += self.speedup_scale
        self.corona_speed_factor *= self.speedup_scale
        self.corona_points = int(self.corona_points * self.score_scale)
        #print(self.corona_points)


if __name__ == '__main__':
    print("Go to main file and run from there.")