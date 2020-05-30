import pygame

class Laser:
    def __init__(self, width, height, x, y):
        self.width = width
        self.height = height
        self.x = x
        self.y = y
        self.velocity = 5
        self.hitbox = (self.x + 9, self.y, 8, 32)

    def draw(self, screen, image):
        self.hitbox = (self.x + 9, self.y, 8, 32)
        screen.blit(image, (self.x, self.y))
        #pygame.draw.rect(screen, (255, 0, 0), self.hitbox, 2)
