class Settings:
    """A class to store all settings for Alien Invasion."""

    def __init__(self):
       #Screen Settings
       self.height = 1200
       self.width =  800
       self.bg_color = (150,215,250)
       self.laserfier_limit = 2
       self.bullet_width = 3
       self.bullet_height = 30
       self.bullet_color = (250,50,50)
       self.bullets_allowed = 3
       self.fleet_drop_speed = 10
       self.speedup_scale = 1.1
       self.score_scale = 1.5
       self.intialize_dynamic_settings()
    def intialize_dynamic_settings(self):
       self.laserfier_speed = 2.0
       self.bullet_speed = 5.0
       self.brown_indian_speed = 1.0
       self.fleet_direction = 1
       self.brown_indian_points = 50      
    def increase_speed(self):
       self.laserfier_speed *= self.speedup_scale
       self.brown_indian_speed *= self.speedup_scale
       self.bullet_speed *= self.speedup_scale
       self.brown_indian_points = int(self.brown_indian_points * self.score_scale)  
       print("hi") 
 















































