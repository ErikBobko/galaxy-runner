import pygame

# SCREEN
width = 1200
height = 800
screen = pygame.display.set_mode((width, height))
pygame.display.set_caption("Space Ship Game")

# MAIN OPTIONS
fps = 60
clock = pygame.time.Clock()


# ASTEROID AND STAR LISTS
asteroid_images = [
    "../assets/img/asteroid.png",
    "../assets/img/blue-meteor.png",
    "../assets/img/shooting-star.png"
]
stars_list = [
    "../assets/img/star.png",
    "../assets/img/star_plus_lives.png",
    "../assets/img/star-blue.png"
]