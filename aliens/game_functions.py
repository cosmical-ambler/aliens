import sys
import pygame
from bullet import Bullet
from alien import Alien
from time import sleep
def check_keydown_events(event,ai_settings,screen,ship,bullets):
	if event.key ==pygame.K_RIGHT:
		ship.moving_right = True
	elif event.key ==pygame.K_LEFT:
		ship.moving_left = True
	elif event.key ==pygame.K_UP:
		ship.moving_up = True
	elif event.key ==pygame.K_DOWN:
		ship.moving_down = True
	elif event.key == pygame.K_SPACE:
		fire_bullet(ai_settings,screen,ship,bullets)
	elif event.key == pygame.K_q:
		sys.exit()
def check_keyup_events(event,ship):
	if event.key ==pygame.K_RIGHT:
		ship.moving_right = False
	if event.key ==pygame.K_LEFT:
		ship.moving_left = False
	if event.key ==pygame.K_UP:
		ship.moving_up = False
	if event.key ==pygame.K_DOWN:
		ship.moving_down = False
def check_events(ai_settings,screen,sb,stats,play_button,ship,aliens,bullets):
	for event in pygame.event.get():
			if event.type == pygame.QUIT:
				sys.exit()
			elif event.type == pygame.KEYDOWN:
				check_keydown_events(event,ai_settings,screen,ship,bullets)
			elif event.type == pygame.KEYUP:
				check_keyup_events(event,ship)
			elif event.type == pygame.MOUSEBUTTONDOWN:
				mouse_x,mouse_y = pygame.mouse.get_pos()
				check_play_button(ai_settings,screen,stats,play_button,sb,ship,aliens,bullets,mouse_x,mouse_y)
def check_play_button(ai_settings,screen,stats,play_button,sb,ship,aliens,bullets,mouse_x,mouse_y):
	button_clicked= play_button.rect.collidepoint(mouse_x,mouse_y)
	if button_clicked and not stats.game_active:
		pygame.mouse.set_visible(False)
		stats.reset_stats()
		stats.game_active= True
		sb.prep_score()
		sb.prep_level()
		sb.prep_ships()
		aliens.empty()
		bullets.empty()
		create_fleet(ai_settings,screen,ship,aliens)
		ship.center_ship()
def update_screen(ai_settings,screen,stats,ship,aliens,bullets,play_button,sb):
	screen.fill(ai_settings.bg_color)
	ship.blitme()
	aliens.draw(screen)
	sb.show_score()
	if not stats.game_active:
		play_button.draw_button()
	for bullet in bullets.sprites():
		bullet.draw_bullet()
	pygame.display.flip()
def check_high_score(stats,sb):
	if stats.score>stats.high_score:
		stats.high_score = stats.score
		sb.prep_high_score()
def check_bullet_aliens(ai_settings,screen,ship,aliens,bullets,sb,stats):
	collisions =pygame.sprite.groupcollide(bullets,aliens,True,True)
	if collisions:
		for aliens in collisions.values():
			stats.score += ai_settings.alien_point*len(aliens)
			sb.prep_score()
		check_high_score(stats,sb)
	if len(aliens)==0:
		ai_settings.increase_speed()
		bullets.empty()
		stats.level +=1
		sb.prep_level()
		create_fleet(ai_settings,screen,ship,aliens)
def update_bullets(ai_settings,screen,ship,aliens,bullets,sb,stats):
	bullets.update()
	check_bullet_aliens(ai_settings,screen,ship,aliens,bullets,sb,stats)
	for bullet in bullets.copy():
		if bullet.rect.bottom <=0:
			bullets.remove(bullet)
def fire_bullet(ai_settings,screen,ship,bullets):
	if len(bullets) < ai_settings.bullets_allowed:
			new_bullet =Bullet(ai_settings,screen,ship)
			bullets.add(new_bullet)
def get_number_aliens_x(ai_settings,alien_width):
	ava_space_x = ai_settings.screen_width - 2*alien_width
	number_alien_x=int(ava_space_x/(2*alien_width))
	return number_alien_x
def get_number_aliens_y(ai_settings,ship_height,alien_height):
	ava_space_y=(ai_settings.screen_height-(3*alien_height)-ship_height)
	number_rows =int(ava_space_y/(2*alien_height))
	return number_rows
def create_alien(ai_settings,screen,aliens,alien_number,row_number):
	alien =Alien(ai_settings,screen)
	alien_width =alien.rect.width
	alien.x =alien_width+2*alien_width*alien_number
	alien.rect.y = alien.rect.height+2*alien.rect.height*row_number
	alien.rect.x=alien.x
	aliens.add(alien)
def check_fleet_edges(ai_settings,aliens):
	for alien in aliens.sprites():
		if alien.check_edges():
			change_fleet_dir(ai_settings,aliens)
			break
def change_fleet_dir(ai_settings,aliens):
	for alien in aliens:
		alien.rect.y +=ai_settings.fleet_drop_speed 
	ai_settings.fleet_dir *= -1
def ship_hit(ai_settings,stats,screen,ship,sb,aliens,bullets):
	if stats.ships_left>0:
		stats.ships_left -=1
		sb.prep_ships()
		aliens.empty()
		bullets.empty()
		create_fleet(ai_settings,screen,ship,aliens)
		ship.center_ship()
		sleep(0.5)
	else:
		ai_settings.initialize_dynamic_settings()
		stats.game_active = False
		pygame.mouse.set_visible(True)
		
def check_aliens_bottom(ai_settings,stats,screen,ship,sb,aliens,bullets):
	screen_rect = screen.get_rect()
	for alien in aliens.sprites():
		if alien.rect.bottom >= screen_rect.bottom:
			ship_hit(ai_settings,stats,screen,ship,sb,aliens,bullets)
			break
def update_aliens(ai_settings,stats,screen,ship,sb,aliens,bullets):
	check_fleet_edges(ai_settings,aliens)
	aliens.update()
	if pygame.sprite.spritecollideany(ship,aliens):
		ship_hit(ai_settings,stats,screen,ship,sb,aliens,bullets)
	check_aliens_bottom(ai_settings,stats,screen,ship,sb,aliens,bullets)
def  create_fleet(ai_settings,screen,ship,aliens):
	alien =Alien(ai_settings,screen)
	number_alien_x =get_number_aliens_x(ai_settings,alien.rect.width)
	number_rows =get_number_aliens_y(ai_settings,ship.rect.height,alien.rect.height)
	for row_number in range(number_rows):
		for alien_number in range(number_alien_x):
			create_alien(ai_settings,screen,aliens,alien_number,row_number)
