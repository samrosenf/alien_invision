import sys
from time import sleep

import pygame

from settings import Settings
from game_stats import GameStats
from scoreboard import Scoreboard
from levels import load_level_data
from sound import Sound
from button import Button
from ship import Ship
from bullet import Bullet
from alien import Alien


class AlienInvasion:
    """Overall class to manage game assets and behaviour."""

    def __init__(self):
        """Initialize the game, and create game resources."""
        pygame.init()
        self.settings = Settings()

        self.screen = pygame.display.set_mode((
            self.settings.screen_width, self.settings.screen_height))
        pygame.display.set_caption('Alien Invasion')
        self.settings.load_bg()

        # Make the play button
        self.play_button = Button(self, "Play")

        # Create an instance to store the game statistics & a scoreboard.
        self.stats = GameStats(self)
        self.sb = Scoreboard(self)

        self.ship = Ship(self)
        self.bullets = pygame.sprite.Group()
        self.aliens = pygame.sprite.Group()

        # Add music to the game.
        self.sound = Sound()

        self._create_fleet()

    def run_game(self):
        """Start the main loop for the game."""
        clock = pygame.time.Clock()
        while True:
            clock.tick(self.settings.FPS)
            self._check_events()
            if self.stats.game_active:
                self.ship.update()
                self._update_bullets()
                self._update_aliens()

            self._update_screen()

    def _start_game(self):
        # Reset the game statistics.
        self.settings.initialize_dynamic_settings()
        self.stats.reset_stats()
        self.stats.game_active = True
        self.sb.prep_images()

        # Get rid of any remaining aliens and bullets.
        self.aliens.empty()
        self.bullets.empty()

        # Create a new fleet and center the ship.
        self._create_fleet()
        self.ship.center_ship()

        # Hide the mouse cursor.
        pygame.mouse.set_visible(False)

    def _start_new_level(self):
        """Setup the new level."""
        # Increase level.
        self.stats.level += 1
        self.sb.prep_level()
        # self.settings.increase_speed()
        # Play level up sound
        self.sound.play_levelup_sound()
        if self.stats.level <= self.settings.MAX_LEVEL:
            self._setup_level()
        else:
            self.stats.win_game = True
            self.stats.game_active = False

    def _setup_level(self):
        # Get rid of any remaining aliens and bullets.
        self.aliens.empty()
        self.bullets.empty()

        # Create a new fleet and center the ship.
        self._create_fleet()
        self.ship.center_ship()

    def _create_fleet(self):
        """Create the fleet of aliens."""
        # Create an alien and find the number of aliens in a row.
        # Spacing between each alien is equal to one alien width.
        level_data = load_level_data(self.stats.level)

        # Create the full fleet of aliens
        for y_idx, row in enumerate(level_data):
            for x_idx, level in enumerate(row):
                if level:
                    self._create_alien(x_idx, y_idx, level)

    def _create_alien(self, x_idx, y_idx, level):
        # Create an alien and place it in the row.
        alien = Alien(self, level)
        alien_width, alien_height = alien.rect.size
        # Place the alien in the right position
        alien.x = alien_width + 1.5 * alien_width * x_idx
        alien.y = self.settings.fleet_y_start + alien_height * y_idx
        alien.rect.y = alien.y
        alien.rect.x = alien.x
        self.aliens.add(alien)

    def _update_bullets(self):
        """Update position of bullets and get rid of old bullets"""
        # Update bullet positions.
        self.bullets.update()

        # Get rid of bullets that have disappeared.
        for bullet in self.bullets.copy():
            if bullet.rect.bottom <= 0:
                self.bullets.remove(bullet)
        if self.aliens:
            self._check_bullet_alien_collisions()
        else:
            self._start_new_level()

    def _check_bullet_alien_collisions(self):
        # Check for any bullets that have hit aliens.
        #   If so, get rid of the bullet and the alien.
        collisions = pygame.sprite.groupcollide(
            self.bullets, self.aliens, True, False, pygame.sprite.collide_mask)

        if collisions:
            self.sound.play_boom_sound()
            for aliens in collisions.values():
                # Every shot gain points.
                self.stats.score += self.settings.hit_points * len(aliens)
                for alien in aliens:
                    # Alien has been hit, decreas one life of the alien
                    alien.life -= 1
                    if alien.life <= 0:
                        # Update score and remove the alien
                        self.stats.score += self.settings.kill_points * alien.level
                        self.aliens.remove(alien) 
                    # Update the image according to the alien's life
                    else:
                        alien.load_image()
            self.sb.prep_score()
            self.sb.check_high_score()

    def _check_aliens_at_bottom(self):
        """Check if any aliens have reached the bottom of the screen."""
        screen_rect = self.screen.get_rect()
        for alien in self.aliens.sprites():
            if alien.rect.bottom >= screen_rect.bottom:
                # Treat this the same as if the ship got hit.
                self._ship_hit()
                break

    def _ship_hit(self):
        """Respond to the ship being hit by an alien 
            or aliens reached the bottom of the screen."""
        if self.stats.ships_left > 1:
            self._lose_ship()
            self._setup_level()
            # Pause.
            sleep(0.5)
        else:
            self._lose_ship()
            self.stats.game_active = False
            pygame.mouse.set_visible(True)

    def _lose_ship(self):
        """Update Ship when losing a ship"""
        # Decrement ships left.
        self.stats.ships_left -= 1
        self.sb.prep_ships()
        self.sound.play_ship_hit_sound()

    def _update_aliens(self):
        """
        Check if the fleet is at an edge,
         then update the positions of all aliens in the fleet.
        """
        self._check_fleet_edges()
        self.aliens.update()

        # Look for alien-ship collisions.
        if pygame.sprite.spritecollideany(self.ship, self.aliens,
                                          pygame.sprite.collide_mask):
            self._ship_hit()

        # Look for aliens hitting the bottom of the screen.
        self._check_aliens_at_bottom()

    def _update_screen(self):
        """Update images on the screen, and flip to the new screen"""
        self.screen.blit(self.settings.bg, (0, 0))
        self.ship.blitme()
        for bullet in self.bullets.sprites():
            bullet.draw_bullet()
        self.aliens.draw(self.screen)

        # Draw the score information.
        self.sb.show_score()

        # Draw the play button if the game is inactive.
        if not self.stats.game_active:
            self.play_button.draw_button()
            # Draw winning
            if self.stats.win_game:
                self.sb.show_winning_text()

        pygame.display.flip()

    def _save_high_score_and_exit(self):
        filename = self.settings.highscore_file
        with open(filename, 'w') as file_object:
            file_object.write(str(self.stats.high_score))
        pygame.quit()
        sys.exit()

    def _check_play_button(self, mouse_pos):
        """Start a new game when the player clicks Play."""
        button_clicked = self.play_button.rect.collidepoint(mouse_pos)
        if button_clicked and not self.stats.game_active:
            # Reset the game settings.

            self._start_game()

    def _check_events(self):
        """Respond to keypresses and mouse events"""
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                self._save_high_score_and_exit()

            elif event.type == pygame.KEYDOWN:
                self._check_keydown_events(event)

            elif event.type == pygame.KEYUP:
                self._check_keyup_events(event)

            elif event.type == pygame.MOUSEBUTTONDOWN:
                mouse_pos = pygame.mouse.get_pos()
                self._check_play_button(mouse_pos)

    def _check_keyup_events(self, event):
        if event.key == pygame.K_RIGHT:
            self.ship.moving_right = False
        elif event.key == pygame.K_LEFT:
            self.ship.moving_left = False
        elif event.key == pygame.K_UP:
            self.ship.moving_up = False
        elif event.key == pygame.K_DOWN:
            self.ship.moving_down = False

    def _check_keydown_events(self, event):
        if event.key == pygame.K_RIGHT:
            self.ship.moving_right = True
        elif event.key == pygame.K_LEFT:
            self.ship.moving_left = True
        elif event.key == pygame.K_UP:
            self.ship.moving_up = True
        elif event.key == pygame.K_DOWN:
            self.ship.moving_down = True
        elif event.key == pygame.K_q:
            self._save_high_score_and_exit()
        elif event.key == pygame.K_SPACE:
            self._fire_bullet()
        elif event.key == pygame.K_p and not self.stats.game_active:
            self._start_game()

    def _fire_bullet(self):
        """Create a new bullet and add it to the bullets group."""
        bullets_available = len(self.bullets) < self.settings.bullets_allowed
        if bullets_available and self.stats.game_active:
            new_bullet = Bullet(self)
            self.bullets.add(new_bullet)

    def _check_fleet_edges(self):
        """Respond appropriately if any aliens have reached an edge."""
        for alien in self.aliens.sprites():
            if alien.check_edges():
                self._change_fleet_direction()
                break

    def _change_fleet_direction(self):
        """Drop the entire fleet and change the fleet's direction."""
        for alien in self.aliens.sprites():
            alien.y += self.settings.fleet_drop_speed
        self.settings.fleet_direction *= -1


if __name__ == '__main__':
    # Make a game instance, and run the game.
    ai = AlienInvasion()
    ai.run_game()
