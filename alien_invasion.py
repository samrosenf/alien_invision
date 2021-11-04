import sys
from time import sleep
import random

import pygame

from settings import Settings
from game_stats import GameStats
from scoreboard import Scoreboard
from events import Events
from levels import load_level_data
from sound import Sound
from button import Button
from ship import Ship
from bullet import PlayerBullet, EnemyBullet
from powerup import LifePowerUp, WeaponPowerUp, ShieldPowerUp
from enemy import Enemy


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
        self.events = Events(self)

        self.ship = Ship(self)
        self.ship_bullets = pygame.sprite.Group()
        self.enemies = pygame.sprite.Group()
        self.enemies_bullets = pygame.sprite.Group()
        self.powerups = pygame.sprite.Group()

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
                self._update_enemies()
                self._update_powerups()

            self._update_screen()

    def _start_game(self):
        # Reset the game statistics.
        self.settings.initialize_dynamic_settings()
        self.stats.reset_stats()
        self.stats.game_active = True
        self.sb.prep_images()
        self._setup_level()
        # Remove old powerups only with new game
        self.powerups.empty()

        # Hide the mouse cursor.
        pygame.mouse.set_visible(False)

    def _start_new_level(self):
        """Setup the new level."""
        # Increase level.
        self.stats.level += 1
        if self.stats.level <= self.settings.MAX_LEVEL:
            self._setup_level()
            # self.settings.increase_speed()
            self.sb.prep_level()
            self.sound.play_levelup_sound()
        else:
            self.stats.win_game = True
            self.stats.game_active = False
            # Play win sound TODO

    def _setup_level(self):
        # Get rid of any remaining enemies, bullets.
        self.enemies.empty()
        self.ship_bullets.empty()
        self.enemies_bullets.empty()

        # Create a new fleet and center the ship.
        self._create_fleet()
        self.ship.center_ship()

    def _create_fleet(self):
        """Create the fleet of enemies."""
        # Create an enemy according the the level map.
        # Spacing between each enemy is equal to half an enemy width.
        level_data = load_level_data(self.stats.level)

        # Create the full fleet of enemies
        for y_idx, row in enumerate(level_data):
            for x_idx, level in enumerate(row):
                if level:
                    self._create_enemy(x_idx, y_idx, level)

    def _create_enemy(self, x_idx, y_idx, level):
        """Create an enemy and place it in the right position in the grid."""
        enemy = Enemy(self, level)
        enemy_width, enemy_height = enemy.rect.size
        enemy.x = enemy_width + 1.5 * enemy_width * x_idx
        enemy.y = self.settings.fleet_y_start + enemy_height * y_idx
        enemy.rect.y = enemy.y
        enemy.rect.x = enemy.x
        self.enemies.add(enemy)

    def _update_powerups(self):
        """Update the powerups location and if they were taken by the player."""
        self.powerups.update()
        collisions = pygame.sprite.spritecollide(self.ship, self.powerups,
                                                 False, pygame.sprite.collide_mask)
        for powerup in collisions:
            if isinstance(powerup, LifePowerUp):
                if self.stats.ships_left < self.settings.max_ships:
                    self.stats.ships_left += 1
                    self.sb.prep_ships()
            elif isinstance(powerup, WeaponPowerUp):
                self.stats.weapon_power += 1
            elif isinstance(powerup, ShieldPowerUp):
                self.ship.create_shield()
            self.powerups.remove(powerup)

        # Remove powerups that are out of the screen.
        for powerup in self.powerups.copy():
            if powerup.rect.top >= self.settings.screen_height:
                self.powerups.remove(powerup)

    def _update_bullets(self):
        """Update position of bullets and get rid of old bullets"""
        # Update bullet positions.
        self.ship_bullets.update()
        self.enemies_bullets.update()

        # Get rid of enemy bullets that have disappeared.
        for bullet in self.enemies_bullets.copy():
            if bullet.rect.top >= self.settings.screen_height:
                self.enemies_bullets.remove(bullet)
        self._check_enemy_bullets_ship_collisions()
        # Get rid of player bullets that have disappeared.
        for bullet in self.ship_bullets.copy():
            if bullet.rect.bottom <= 0:
                self.ship_bullets.remove(bullet)

        if self.enemies:
            self._check_player_bullets_enemy_collisions()
        else:
            self._start_new_level()

    def _check_enemy_bullets_ship_collisions(self):
        """Check if enemy bullets hit the ship"""
        bullet_hit = pygame.sprite.spritecollideany(self.ship, self.enemies_bullets,
                                                    pygame.sprite.collide_mask)
        if bullet_hit:
            if self.ship.shield:
                # Remove Shield
                self.ship.remove_shield()
                # Remove the bullet
                self.enemies_bullets.remove(bullet_hit)
            else:
                self._ship_hit()

    def _check_player_bullets_enemy_collisions(self):
        """"Check for any bullets that have hit enemies.
           If so, update enemy life, and remove if dead."""
        collisions = pygame.sprite.groupcollide(
            self.ship_bullets, self.enemies, False, False, pygame.sprite.collide_mask)

        if collisions:
            self.sound.play_boom_sound()
            for bullet, enemies in collisions.items():
                # Every shot gain points.
                self.stats.score += self.settings.hit_points * len(enemies)
                for enemy in enemies:
                    # Enemy has been hit, decreas one life of the enemy
                    enemy.life -= bullet.power
                    if enemy.life <= 0:
                        # Update score and remove the enemy
                        self.stats.score += self.settings.kill_points * enemy.level
                        self.enemies.remove(enemy)
                    # Update the image according to the enemy's life
                    else:
                        enemy.update_image()
                self.ship_bullets.remove(bullet)
            self.sb.prep_score()
            self.sb.check_high_score()

    def _check_enemies_at_bottom(self):
        """Check if any enemies have reached the bottom of the screen."""
        screen_rect = self.screen.get_rect()
        for enemy in self.enemies.sprites():
            if enemy.rect.bottom >= screen_rect.bottom:
                # Treat this the same as if the ship got hit.
                self._ship_hit()
                break

    def _ship_hit(self):
        """Respond to the ship being hit by an enemy 
            or enemies reached the bottom of the screen."""
        if self.stats.ships_left > 1:
            self._lose_ship()
            self._setup_level()
            # Pause.
            sleep(0.5)
        else:
            self._lose_ship()
            self.stats.game_active = False

    def _lose_ship(self):
        """Update Ship when losing a ship"""
        # Decrement ships left.
        self.stats.ships_left -= 1
        self.sb.prep_ships()
        self.sound.play_ship_hit_sound()

    def _update_enemies(self):
        """
        Check if the fleet is at an edge,
         then update the positions of all enemies in the fleet.
        """
        self._check_fleet_edges()
        self.enemies.update()

        # Look for enemy-ship collisions.
        enemy_collided = pygame.sprite.spritecollideany(self.ship, self.enemies,
                                          pygame.sprite.collide_mask)
        if enemy_collided:
            if self.ship.shield:
                # Remove shield
                self.ship.remove_shield()
                # Remove enemy
                self.enemies.remove(enemy_collided)
            else:
                self._ship_hit()

        # Look for enemies hitting the bottom of the screen.
        self._check_enemies_at_bottom()

    def _update_screen(self):
        """Update images on the screen, and flip to the new screen"""
        self.screen.blit(self.settings.bg, (0, 0))
        self.ship.blitme()
        for bullet in self.ship_bullets.sprites():
            bullet.draw_bullet()
        for bullet in self.enemies_bullets.sprites():
            bullet.draw_bullet()
        self.powerups.draw(self.screen)
        self.enemies.draw(self.screen)

        # Draw the score information.
        self.sb.show_score()

        # Draw the play button if the game is inactive.
        if not self.stats.game_active:
            pygame.mouse.set_visible(True)
            self.play_button.draw_button()
            # Draw winning if won the game
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
        game_active = self.stats.game_active
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
            elif event.type == self.events.enemy_shooting.id and game_active:
                self._enemy_shoots()
            elif event.type == self.events.powerup_drop.id and game_active:
                power = random.choice([LifePowerUp, ShieldPowerUp, WeaponPowerUp])
                self.powerups.add(power(self))

    def _enemy_shoots(self):
        selected_alien = random.choice(self.enemies.sprites())
        new_bullet = EnemyBullet(self, selected_alien)
        self.enemies_bullets.add(new_bullet)

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
        bullets_available = len(
            self.ship_bullets) < self.settings.bullets_allowed
        if bullets_available and self.stats.game_active:
            new_bullet = PlayerBullet(self)
            self.ship_bullets.add(new_bullet)

    def _check_fleet_edges(self):
        """Respond appropriately if any enemies have reached an edge."""
        for enemy in self.enemies.sprites():
            if enemy.check_edges():
                self._change_fleet_direction()
                break

    def _change_fleet_direction(self):
        """Drop the entire fleet and change the fleet's direction."""
        for enemy in self.enemies.sprites():
            enemy.drop_verticaly()
        self.settings.fleet_direction *= -1


if __name__ == '__main__':
    # Make a game instance, and run the game.
    ai = AlienInvasion()
    ai.run_game()
