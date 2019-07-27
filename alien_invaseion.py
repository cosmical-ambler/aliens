import sys
import pygame
import game_functions as gf
from setting import Settings
from Ship import Ship
from alien import Alien
from pygame.sprite import Group
from game_stats import GameStats
from button import Button
from scoreboard import Scoreboard
def run_game():
	pygame.init()
	ai_settings= Settings()
	screen= pygame.display.set_mode((ai_settings.screen_width,ai_settings.screen_height))
	alien = Alien(ai_settings,screen)
	pygame.display.set_caption("Alien Invasion")
	ship=Ship(ai_settings,screen)
	bullets=Group()
	aliens=Group()
	stats = GameStats(ai_settings)
	sb = Scoreboard(ai_settings,screen,stats)
	gf.create_fleet(ai_settings,screen,ship,aliens)
	play_button = Button(ai_settings,screen,"Play")
	while True:
		gf.check_events(ai_settings,screen,sb,stats,play_button,ship,aliens,bullets)
		if stats.game_active:
			ship.update()
			gf.update_bullets(ai_settings,screen,ship,aliens,bullets,sb,stats)
			gf.update_aliens(ai_settings,stats,screen,ship,sb,aliens,bullets)
		gf.update_screen(ai_settings,screen,stats,ship,aliens,bullets,play_button,sb)
run_game()
