import pygame
import random
from config import width,height


# ASTEROID CLASS

class Asteroid(pygame.sprite.Sprite):
    def __init__(self, image, speed=1):
        super().__init__()
        self.image = pygame.image.load(image)
        self.rect = self.image.get_rect()
        self.rect.y = -50
        self.rect.x = random.randint(0, width - self.rect.width)
        self.speed = speed
    def move(self):
        self.rect.y += self.speed