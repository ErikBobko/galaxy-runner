import pygame
import random

from config import *
from asteroid import Asteroid
from stars import Stars
from network import send_score, get_leaderboard


class Game:
    def __init__(self, player, star, asteroid):
        self.player = player
        self.asteroid = asteroid
        self.star = star
        self.score = 0
        self.leaderboard = []

        self.round_time = 0
        self.slow_down_cycle = 0

        self.red_star_dur = 4
        self.red_star_timer = 0
        self.blue_star_dur = 4
        self.blue_star_timer = 0
        self.shield_dur = 20

        self.score_sent = False
        self.game_over = False
        self.game_start = False
        self.exploding = False
        self.final_game_over = False
        self.red_star_spawned = False
        self.blue_star_spawned = False
        self.shield_activate = False
        self.shield_start_time = 0

        self.enter_name = True
        self.input_text = ""
        self.player_name = ""
        self.player_country = ""
        self.input_stage = "name"

        self.countries = ["Slovakia", "Czech Republic", "Germany", "Austria", "Poland", "Hungary"]
        self.country_index = 0


        # FONTS
        self.my_font = pygame.font.Font("../assets/fonts/space-font.ttf", 25)

        # BACKGROUND IMAGE
        self.background_image = pygame.image.load("../assets/img/backround2.png").convert()
        self.background_image_rect = self.background_image.get_rect()
        self.background_image_rect.topleft = (0, 0)

        # EXPLOSION IMAGES
        self.explosion_frames = [pygame.image.load(f"../assets/img/game-over/E000{i}.png") for i in range(1, 10)]

        # MUSIC / SOUND
        pygame.mixer.music.load("../assets/media/backround-music.wav")
        pygame.mixer.music.play(-1)
        pygame.mixer.music.set_volume(0.3)
        self.crash = pygame.mixer.Sound("../assets/media/boom2.wav")
        self.crash.set_volume(0.3)
        self.collect_star = pygame.mixer.Sound("../assets/media/colect-star.wav")
        self.collect_star.set_volume(0.3)
        self.collect_red_star = pygame.mixer.Sound("../assets/media/star_plus_lives_sound.wav")
        self.collect_red_star.set_volume(0.3)
        self.collect_blue_star = pygame.mixer.Sound("../assets/media/space-shield-activate.wav")
        self.collect_blue_star.set_volume(0.3)

        #SHIELD - DEFAULT
        self.shield = pygame.image.load("../assets/img/space-ship-shield.png")
        self.player_default_image = self.player.original_image.copy()

    # HANDLE INPUT
    def handle_events(self, event):
        if event.type == pygame.KEYDOWN:
            if self.enter_name:

                if event.key == pygame.K_RETURN:

                    if self.input_stage == "name":
                        self.player_name = self.input_text
                        self.input_text = ""
                        self.input_stage = "country"

                    else:
                        self.player_country = self.countries[self.country_index]
                        self.enter_name = False

                elif self.input_stage == "country":


                    if event.key == pygame.K_UP:
                        self.country_index = (self.country_index - 1) % len(self.countries)

                    elif event.key == pygame.K_DOWN:
                        self.country_index = (self.country_index + 1) % len(self.countries)

                elif event.key == pygame.K_BACKSPACE and self.input_stage == "name":
                    self.input_text = self.input_text[:-1]

                elif self.input_stage == "name":
                    self.input_text += event.unicode

                return

            if event.key == pygame.K_r and self.game_over:
                self.reset_game()
            if not self.game_start:
                self.game_start = True
            if event.key == pygame.K_LEFT:
                self.player.direction = "left"
            elif event.key == pygame.K_RIGHT:
                self.player.direction = "right"
            elif event.key == pygame.K_UP:
                self.player.direction = "up"
            elif event.key == pygame.K_DOWN:
                self.player.direction = "down"

    # UPDATE GAME STATE
    def update(self):
        if not self.game_over:
            self.star.update()
            self.asteroid.update()
            self.player.update()
            self.collision_checker()
            self.activation_items()


            # Round timer
            self.slow_down_cycle += 1
            if self.slow_down_cycle == 60:
                self.round_time += 1
                self.slow_down_cycle = 0
                

            # RED STAR SPAWN
            if self.round_time % 25 == 0 and not self.red_star_spawned and self.score > 10:
                red_star = Stars(stars_list[1], "red")
                self.star.add(red_star)
                self.red_star_spawned = True
                self.red_star_timer = self.round_time
            if self.red_star_spawned:
                if self.round_time - self.red_star_timer >= self.red_star_dur:
                    for star in self.star:
                        if star.type == "red":
                            star.kill()
                    self.red_star_spawned = False

            # BLUE STAR SPAWN
            if self.round_time % 35 == 0 and not self.blue_star_spawned and self.score > 10:
                blue_star = Stars(stars_list[2], "blue")
                self.star.add(blue_star)
                self.blue_star_spawned = True
                self.blue_star_timer = self.round_time
            if self.blue_star_spawned:
                if self.round_time - self.blue_star_timer >= self.blue_star_dur:
                    for star in self.star:
                        if star.type == "blue":
                            star.kill()
                    self.blue_star_spawned = False

        # SHIELD TIMER
        if self.shield_activate:
            if self.round_time - self.shield_start_time >= self.shield_dur:
                self.shield_activate = False
                self.player.original_image = self.player_default_image

        # Fix: prevent player death when shield expires near screen edge

                if self.player.rect.left < 0:
                    self.player.rect.left = 0
                if self.player.rect.right > width:
                    self.player.rect.right = width
                if self.player.rect.top < 90:
                    self.player.rect.top = 90
                if self.player.rect.bottom > height:
                    self.player.rect.bottom = height

    # DRAW EVERYTHING
    def draw(self):
        white = pygame.Color(255, 255, 255)
        red = pygame.Color(255, 0, 0)
        dark_blue = pygame.Color(0, 100, 255)

        screen.blit(self.background_image, (0, 0))
        self.star.draw(screen)
        self.asteroid.draw(screen)

        # Player explosion or draw
        if self.exploding and self.explosion_target:
            if self.explosion_index < len(self.explosion_frames):
                screen.blit(self.explosion_frames[self.explosion_index], self.explosion_target.rect)
                self.explosion_index += 1
            else:
                self.exploding = False
                self.game_over = True
        else:
                self.player.draw(screen)
        if self.enter_name:
            screen.fill((0, 0, 0))
            label = "ENTER NAME:" if self.input_stage == "name" else "ENTER COUNTRY:"
            if self.input_stage == "country":
                for i, country in enumerate(self.countries):
                    color = (0, 255, 0) if i == self.country_index else (255, 255, 255)

                    text = self.my_font.render(country, True, color)
                    text_rect = text.get_rect(center=(width // 2, 350 + i * 30))
                    screen.blit(text, text_rect)

                return
            text = self.my_font.render(label, True, (255, 255, 255))
            text_rect = text.get_rect(center=(width // 2, 300))
            screen.blit(text, text_rect)

            name_text = self.my_font.render(self.input_text, True, (0, 255, 0))
            name_text_rect = name_text.get_rect(center=(width // 2, 350))
            screen.blit(name_text, name_text_rect)

            return

        # TEXT HUD
        main_text = self.my_font.render("GALAXY RUNNER", True, white)
        main_text_rect = main_text.get_rect(center=(width // 2, 50))
        score_text = self.my_font.render(f"SCORE: {self.score}", True, white)
        score_text_rect = score_text.get_rect(center=(100, 50))
        lives_text = self.my_font.render(f"LIVES: {self.player.lives}", True, white)
        lives_text_rect = lives_text.get_rect(center=(1100, 50))
        restart_text = self.my_font.render("Press R to restart", True, white)
        restart_text_rect = restart_text.get_rect(center=(600, 200))
        game_over_text = self.my_font.render(f"GAME OVER your final score is {self.score}", True, red)
        game_over_text_rect = game_over_text.get_rect(center=(600, 300))
        start_game_text = self.my_font.render("Press arrow key to start", True, white)
        start_game_text_rect = start_game_text.get_rect(center=(600, 300))

        # Draw texts
        screen.blit(main_text, main_text_rect)
        screen.blit(score_text, score_text_rect)
        screen.blit(lives_text, lives_text_rect)
        if self.final_game_over:

            # BACKGROUND BOX

            overlay = pygame.Surface((500, 250))
            overlay.set_alpha(180)
            overlay.fill((0, 0, 0))
            screen.blit(overlay, (350, 350))

            screen.blit(restart_text, restart_text_rect)
            screen.blit(game_over_text, game_over_text_rect)
            pygame.draw.rect(screen, red, (0, 80, 1200, 720), 2)

        elif self.game_over:
            screen.blit(restart_text, restart_text_rect)

        elif not self.game_start:
            screen.blit(start_game_text, start_game_text_rect)

        if not self.final_game_over:
            pygame.draw.rect(screen, dark_blue, (0, 80, 1200, 720), 2)

            # LEADERBOARD (TOP 3)

        if self.final_game_over:
            lb_title = self.my_font.render("TOP 3 PLAYERS", True, (255, 255, 0))
            lb_title_rect = lb_title.get_rect(center=(600, 400))
            screen.blit(lb_title, lb_title_rect)

        # SCORES

            for i, entry in enumerate(self.leaderboard[:3]):
                color = (255, 215, 0) if i == 0 else (255, 255, 255)
                text = self.my_font.render(
                    f"{i + 1}. {entry['name']} ({entry['country']}) - {entry['score']}",
                    True,
                    color)

                text_rect = text.get_rect(topleft=(450, 450 + i * 40))
                screen.blit(text, text_rect)


    # COLLISION CHECKER
    def collision_checker(self):
        # PLAYER - STAR
        hits = pygame.sprite.spritecollide(self.player, self.star, False)
        for star in hits:
            if star.type == "yellow":
                star.rect.x = random.randint(0, width - star.rect.width)
                star.rect.y = random.randint(90, height - star.rect.height)
                self.collect_star.play()
                self.score += 1
                self.player.speed += 0.1
            elif star.type == "red":
                self.collect_red_star.play()
                self.score += 5
                star.kill()
            elif star.type == "blue":
                self.collect_blue_star.play()
                self.shield_activate = True
                self.shield_start_time = self.round_time
                self.player.original_image = self.shield
                star.kill()

        # PLAYER - ASTEROID / SCREEN COLLISION
        hits = pygame.sprite.spritecollide(self.player, self.asteroid, False)
        if not self.shield_activate:
            out_of_bounds = (
                    self.player.rect.left < 0 or
                    self.player.rect.right > width or
                    self.player.rect.top < 90 or
                    self.player.rect.bottom > height
            )

            if not self.shield_activate and (hit_asteroid or out_of_bounds):
                self.player.lives -= 1
                self.crash.play()
                if self.player.lives <= 0:
                    self.exploding = True
                    self.explosion_index = 0

                    self.final_game_over = True
                    self.player.alive = False
                    self.game_over = True
                    self.explosion_target_rect = self.player.rect.copy()
                    self.player.speed = 5
                    pygame.mixer_music.stop()

                    if not self.score_sent:
                        send_score(
                            self.player_name,
                            self.player_country,
                            self.score
                        )
                        self.score_sent = True
                        self.leaderboard = get_leaderboard()
                else:
                    self.game_over = True
                    self.exploding = True
                    self.explosion_index = 0
                    self.explosion_target = self.player
                    self.player.alive = False


    # ACTIVATION ITEMS
    def activation_items(self):
        if self.score >= 20 and len(self.asteroid) < 2 and self.player.direction:
            self.asteroid.add(Asteroid(asteroid_images[1], speed=2))
        elif self.score >= 30 and len(self.asteroid) < 3 and self.player.direction:
            self.asteroid.add(Asteroid(asteroid_images[2], speed=3))

        if self.score >= 10 and self.player.direction:
            for asteroid in self.asteroid:
                asteroid.move()
                asteroid.rect.y += 5
                if asteroid.rect.y > height:
                    asteroid.rect.y = 20
                    asteroid.rect.x = random.randint(0, width - asteroid.rect.width)

    # RESET GAME
    def reset_game(self):
        self.score_sent = False
        if self.final_game_over:
            self.score = 0
            self.player.lives = 3
            self.final_game_over = False
            pygame.mixer_music.play(-1)
        self.game_over = False
        self.exploding = False
        self.player.rect.center = (width // 2, height // 2)
        self.player.alive = True
        self.player.direction = None
        self.asteroid.empty()
        self.asteroid.add(Asteroid(asteroid_images[0], speed=1))
        self.leaderboard = get_leaderboard()

