import sys
from time import sleep
import json
from pathlib import Path
import pygame
from settings import Settings
from game_stats import GameStats
from laserfier import Laserfier
from bullet import Bullet
from brown_indian import Indian
from button import Button
from scoreboard import Scoreboard

#Sound Effects
pygame.mixer.init()
bullet_sound = pygame.mixer.Sound('sounds\laser1.wav')
brown_indian_sound = pygame.mixer.Sound('sounds\mixkit-arcade-game-explosion-2759.wav')      

class AlienInvasion:
    """Overall class to manage game assets and behaviour."""
    
    def __init__(self):
          pygame.init()
          self.clock = pygame.time.Clock()
          self.settings = Settings()
          self.screen = pygame.display.set_mode((0,0), pygame.FULLSCREEN)
          self.settings.screen_width = self.screen.get_rect().width
          self.settings.screen_height = self.screen.get_rect().height
          pygame.display.set_caption("Alien Invasion")
          self.stats = GameStats(self) 
          self.sb = Scoreboard(self)
          self.laserfier = Laserfier(self)
          self.bullets = pygame.sprite.Group()
          self.brown_indians = pygame.sprite.Group()
          self._create_fleet()
          self.play_button = Button(self, "Play")
          self.game_active = False
    def run_game(self):
          while True:
             self._check_events()
             if self.game_active:
                 self.laserfier.update()
                 self._update_bullets()
                 self._update_brown_indians()       
             self._update_screen()
             self.clock.tick(60)    
    def _check_events(self):
          for event in pygame.event.get():
              if event.type == pygame.QUIT:
                  sys.exit()
              elif event.type == pygame.KEYDOWN:
                  self._check_keydown_events(event)
              elif event.type == pygame.KEYUP:
                  self._check_keyup_events(event)
    def _start_game(self):
          if self.play_button:
               self.settings.intialize_dynamic_settings()
               self.stats.reset_stats()
               self.sb.prep_score()
               self.sb.prep_level()
               self.sb.prep_laserfiers()
               self.game_active = True
               self.bullets.empty()
               self.brown_indians.empty()
               self._create_fleet()
               self.laserfier.center_laserfier()
               pygame.mouse.set_visible(False)
    def _check_keydown_events(self,event):                
          if event.key == pygame.K_RIGHT:
               self.laserfier.moving_right = True
          elif event.key == pygame.K_LEFT:
               self.laserfier.moving_left = True
          elif event.key == pygame.K_UP:
               self.laserfier.moving_up = True
          elif event.key == pygame.K_DOWN:
               self.laserfier.moving_down = True
          elif event.key == pygame.K_q:
                sys.exit()    
          elif event.key == pygame.K_f:
               self._fire_bullet()
          elif event.key == pygame.K_p:
               self._start_game()
    def _check_keyup_events(self,event):                      
          if event.key == pygame.K_RIGHT:
               self.laserfier.moving_right = False    
          elif event.key == pygame.K_LEFT:
               self.laserfier.moving_left = False    
          elif event.key == pygame.K_UP:
               self.laserfier.moving_up = False    
          elif event.key == pygame.K_DOWN:
               self.laserfier.moving_down = False    
    def _fire_bullet(self):
         if len(self.bullets) < self.settings.bullets_allowed:
            new_bullet = Bullet(self)
            self.bullets.add(new_bullet)
            bullet_sound.play()       
    def _update_bullets(self):       
          self.bullets.update()
          for bullet in self.bullets.copy():
               if bullet.rect.bottom <= 0:
                  self.bullets.remove(bullet)
          self._check_collision()          
    def _check_collision(self):          
          collisions = pygame.sprite.groupcollide(self.bullets, self.brown_indians, True, True)
          if collisions:
               for brown_indians in collisions.values():
                   self.stats.score += self.settings.brown_indian_points * len(brown_indians)
                   self.sb.prep_score()
                   self.sb.check_high_score()
                   brown_indian_sound.play()
          if not self.brown_indians:
               self.bullets.empty
               self._create_fleet()
               self.settings.increase_speed()
               self.stats.level += 1
               self.sb.prep_level()
    def _laserfier_hit(self):
          if self.stats.laserfiers_left > 0:     
               self.stats.laserfiers_left -= 1
               self.sb.prep_laserfiers()
               self.bullets.empty()
               self.brown_indians.empty()
               self._create_fleet()
               self.laserfier.center_laserfier()
               sleep(1.0)
          else:
               self.game_active = False   
    def _check_bottom_reach(self):
          screen_rect = self.screen.get_rect()
          for brown_indian in self.brown_indians.sprites():
               if brown_indian.rect.bottom >= screen_rect.bottom:
                    self._laserfier_hit()
                    break 
    def _create_brown_indian(self,x_position,y_position):
          new_brown_indian = Indian(self)
          new_brown_indian.x = x_position
          new_brown_indian.rect.x = x_position
          new_brown_indian.rect.y  = y_position
          self.brown_indians.add(new_brown_indian) 
    def _check_fleet_edges(self):
          for brown_indian in self.brown_indians.sprites():
               if brown_indian.check_edges():
                    self._change_fleet_direction()
                    break
    def _change_fleet_direction(self):
          for brown_indian in self.brown_indians.sprites():
               brown_indian.rect.y += self.settings.fleet_drop_speed
          self.settings.fleet_direction *= -1                  
    def _create_fleet(self):
          brown_indian = Indian(self)
          brown_indian_width,brown_indian_height = brown_indian.rect.size
          current_x,current_y = brown_indian_width,brown_indian_height
          while current_y < (self.settings.screen_height - 3 * brown_indian_height):
               while current_x < (self.settings.screen_width - 2 * brown_indian_width):
                   self._create_brown_indian(current_x,current_y)
                   current_x += 2 * brown_indian_width  
               current_x = brown_indian_width 
               current_y += 2 * brown_indian_height  
    def _update_brown_indians(self):
          self._check_fleet_edges()
          self.brown_indians.update()
          if pygame.sprite.spritecollideany(self.laserfier, self.brown_indians):
               self._laserfier_hit()
          self._check_bottom_reach()      
    def _update_screen(self):
          self.screen.fill(self.settings.bg_color)
          for bullet in self.bullets.sprites():
             bullet.draw_bullets()
          self.laserfier.blitme()
          self.brown_indians.draw(self.screen)
          self.sb.show_score()
          if not self.game_active:
               self.play_button.draw_button()
          pygame.display.flip()     
    def _close_game(self):
         save_high_score = self.stats.saved_high_score()
         if self.stats.high_score > save_high_score:
              path = Path('high_score.json')
              contents = json.dumps(self.stats.high_score)
              path.write_text(contents)
              
         sys.exit() 
if __name__ == '__main__': 
    ai = AlienInvasion()
    ai.run_game()             
                            
































































































































































