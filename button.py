import pygame.font

class Button:
    "A class to build buttons for this game."

    def __init__(self,ai_game,msg):
        self.screen = ai_game.screen
        self.screen_rect = self.screen.get_rect()
        self.height, self.width = 50, 200
        self.button_color = (180,50,50)
        self.text_color = (0,0,0)
        self.font = pygame.font.SysFont(None, 48)
        self.rect = pygame.Rect(0,0,self.width,self.height)
        self.rect.center = self.screen_rect.center
        self._prep_msg(msg)
    def _prep_msg(self,msg):
        self.msg_image = self.font.render(msg, True, self.text_color, self.button_color)
        self.msg_image_rect = self.msg_image.get_rect()
        self.msg_image_rect.center = self.rect.center
    def draw_button(self):
        self.screen.fill(self.button_color, self.rect)
        self.screen.blit(self.msg_image, self.msg_image_rect)    















































