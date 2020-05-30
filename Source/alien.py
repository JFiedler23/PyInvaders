import pygame
from laser import *

class Alien:
    def __init__(self, width, height, x, y):
        self.width = width
        self.height = height
        self.x = x
        self.y = y
        self.moveDistance = 20
        self.hitbox = (self.x, self.y + 32, 64, 32)

    def draw(self, screen, image):
        self.hitbox = (self.x, self.y + 32, 64, 32)
        screen.blit(image, (self.x, self.y))
        #pygame.draw.rect(screen, (255, 0, 0), self.hitbox, 2)

    def shoot(self, lasers):
        lasers.append(Laser(32, 32, self.x + self.width // 4, self.y + self.height // 6))
