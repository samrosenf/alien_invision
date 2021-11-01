import os


class GameStats:
    """Track statistics for Alien Invasion."""

    def __init__(self, ai_game):
        """Initialize statistics."""
        self.settings = ai_game.settings
        self.reset_stats()

        # Start Alien Invasion in an inactive state.
        self.game_active = False

        # High score should never be reset.
        self.load_high_score_from_file()

    def reset_stats(self):
        """Initialize statistics that can change during the game."""
        self.ships_left = self.settings.ship_limit
        self.score = 0
        self.level = 1

    def load_high_score_from_file(self):
        filename = self.settings.highscore_file
        # Check if high score file exist
        if os.path.isfile(filename):
            try:
                with open(filename) as file_object:
                    # read only the first line
                    txt = file_object.readline()
                    self.high_score = int(txt)
            except:
                print("high score file is incorrect.")
                self.high_score = 0
