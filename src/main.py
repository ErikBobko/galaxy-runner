import pygame
import random

from game import Game
from player import Player
from asteroid import Asteroid
from stars import Stars
from config import fps,width,height,clock
from config import asteroid_images,stars_list

# INIT
pygame.init()

# GROUPS
stars_group = pygame.sprite.Group()
stars_group.add(Stars(stars_list[0], "yellow"))

asteroid_group = pygame.sprite.Group()
asteroid_group.add(Asteroid(asteroid_images[0]))

player_group = pygame.sprite.Group()
player = Player()
player_group.add(player)

# GAME INSTANCE
game = Game(player, stars_group, asteroid_group)

# MAIN LOOP
lets_continue = True
while lets_continue:
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            lets_continue = False
        game.handle_events(event)

    game.update()
    game.draw()
    pygame.display.update()
    clock.tick(fps)

pygame.quit()
