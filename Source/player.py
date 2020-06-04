import pygame
from laser import *

class Player:
    def __init__(self, width, height, x, y):
        self.width = width
        self.height = height
        self.x = x
        self.y = y
        self.rightOffset = 5
        self.velocity = 2
        self.hitbox = (self.x, self.y + 32, 64, 32)

    def draw(self, screen, image):
        screen.blit(image, (self.x, self.y))
        self.hitbox = (self.x, self.y + 32, 64, 32)
        #pygame.draw.rect(screen, (255, 0 ,0), self.hitbox, 2)

    def controller(self, screenWidth, keys):
        #checking for player input
        if keys[pygame.K_RIGHT] and self.x < (screenWidth - self.velocity - self.width + self.rightOffset):
            self.x += self.velocity
        if keys[pygame.K_LEFT] and self.x > 0:
            self.x -= self.velocity

    def shoot(self, keys, lasers, sound):
        if keys[pygame.K_SPACE] and len(lasers) < 3:
            lasers.append(Laser(32, 32, int(self.x + self.width // 4), int(self.y + self.height // 6)))
            sound.play()
