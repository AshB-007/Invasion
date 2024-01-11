import json
from pathlib import Path

class GameStats:
    "Track statistics for Alien Invasion."

    def __init__(self,ai_game):
        self.settings = ai_game.settings
        self.reset_stats()
        self.high_score = self.saved_high_score()
    def saved_high_score(self):
        path = Path('high_score.json')
        try:
            contents = path.read_text()
            high_score = json.loads(contents)    
            return high_score
        except FileNotFoundError:
            return 0 
    def reset_stats(self):
        self.laserfiers_left = self.settings.laserfier_limit
        self.score = 0
        self.level = 1


































































