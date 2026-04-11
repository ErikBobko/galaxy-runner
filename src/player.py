import pygame

from config import width,height

# PLAYER CLASS

class Player(pygame.sprite.Sprite):
    def __init__(self):
        super().__init__()
        self.original_image = pygame.image.load("../assets/img/space-ship.png")
        self.image = self.original_image
        self.rect = self.image.get_rect(center=(width // 2, height // 2))
        self.lives = 3
        self.speed = 5
        self.direction = None
        self.alive = True

    def draw(self, screen):
        if self.alive:
            screen.blit(self.image, self.rect)
    def update(self):
        self.move()

    def move(self):
        if self.direction == "left" and self.rect.left > 0:
            self.rect.x -= self.speed
            self.image = pygame.transform.rotate(self.original_image, 90)
        elif self.direction == "right" and self.rect.right < width:
            self.rect.x += self.speed
            self.image = pygame.transform.rotate(self.original_image, -90)
        elif self.direction == "up" and self.rect.top > 90:
            self.rect.y -= self.speed
            self.image = pygame.transform.rotate(self.original_image, 0)
        elif self.direction == "down" and self.rect.bottom < height:
            self.rect.y += self.speed
            self.image = pygame.transform.rotate(self.original_image, 180)