import pygame
import random

from config import width,height

# STAR CLASS

class Stars(pygame.sprite.Sprite):
    def __init__(self, image, star_type):
        super().__init__()
        self.image = pygame.image.load(image)
        self.rect = self.image.get_rect()
        self.rect.x = random.randint(0, width - self.rect.width)
        self.rect.y = random.randint(90, height - self.rect.height)
        self.alive = True
        self.type = star_type