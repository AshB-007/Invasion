import pygame
from pygame.sprite import Sprite

class Indian(Sprite):
    "A class to represent a single brown indian in the fleet."

    def __init__(self, ai_game):
       super().__init__()
       self.screen = ai_game.screen
       self.settings = ai_game.settings
       self.image = pygame.image.load("images/indian.bmp")
       self.rect = self.image.get_rect()
       self.rect.x = self.rect.width
       self.rect.y = self.rect.height
       self.x = float(self.rect.x)
    def check_edges(self):
       screen_rect = self.screen.get_rect()
       return (self.rect.right >= screen_rect.right) or (self.rect.left <= 0)
    def update(self):
       self.x += self.settings.brown_indian_speed * self.settings.fleet_direction
       self.rect.x = self.x 









































